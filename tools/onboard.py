#!/usr/bin/env python3.12
"""Onboard semi-automatico di un target Vulhub image-based single-service.

Fa la parte MECCANICA: pull+pin digest, genera compose isolato (no ports, rete lab internal,
attacker kali-lite), avvia, ISPEZIONA flag_user via /proc, scrive target.toml, healthcheck, teardown.
Il giudizio (class/stack/split) lo passi tu. Chi non risponde all'health si auto-elimina al gate.

Uso:
  python3.12 tools/onboard.py --vpath fastjson/1.2.47-rce --id fastjson-1-2-47-rce \
     --class deserialization --stack java --split train --port 8090

Opzioni:
  --health-path /   percorso HTTP per l'health (default /)
  --flag-user U     forza flag_user (salta l'ispezione)
  --vulhub DIR      root del checkout vulhub (default /private/tmp/kbsrc/vulhub)
Richiede Python 3.11+ e Docker.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def pin(image: str) -> str:
    sh(["docker", "pull", image])
    d = sh(["docker", "inspect", "--format", "{{index .RepoDigests 0}}", image]).stdout.strip()
    return d or image


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vpath", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--class", dest="cls", required=True)
    ap.add_argument("--stack", required=True)
    ap.add_argument("--split", required=True, choices=["train", "held-out"])
    ap.add_argument("--port", type=int, required=True, help="porta INTERNA del servizio target")
    ap.add_argument("--health-path", default="/")
    ap.add_argument("--flag-user", default=None)
    ap.add_argument("--vulhub", default="/private/tmp/kbsrc/vulhub")
    a = ap.parse_args()

    vdir = Path(a.vulhub) / a.vpath
    vc = yaml.safe_load(open(vdir / "docker-compose.yml"))
    svcs = vc["services"]
    # servizio target = quello con ports; altri = deps
    tname = next((n for n, s in svcs.items() if s and "ports" in s), list(svcs)[0])
    deps = {n: s for n, s in svcs.items() if n != tname and s}

    # pin immagini
    timg = pin(svcs[tname]["image"])
    dep_imgs = {n: pin(s["image"]) for n, s in deps.items() if "image" in s}

    # genera compose isolato
    lines = [f"# Target Vulhub {a.vpath} (MIT). Immagine pinnata, no ports, rete lab internal.",
             f"name: kalithos-dojo-{a.id}", "", "services:",
             f"  {tname}:", f"    image: {timg}", "    networks: [lab]"]
    if deps:
        lines.append(f"    depends_on: [{', '.join(deps)}]")
        # preserva environment del target se presente
    if svcs[tname].get("environment"):
        lines.append("    environment:")
        env = svcs[tname]["environment"]
        for e in (env if isinstance(env, list) else [f"{k}={v}" for k, v in env.items()]):
            lines.append(f"      - {e}")
    for n, s in deps.items():
        lines += ["", f"  {n}:", f"    image: {dep_imgs.get(n, s.get('image'))}", "    networks: [lab]"]
        if s.get("environment"):
            lines.append("    environment:")
            env = s["environment"]
            for e in (env if isinstance(env, list) else [f"{k}={v}" for k, v in env.items()]):
                lines.append(f"      - {e}")
    lines += ["", "  attacker:", "    image: grpo-rt/kali-lite:latest",
              "    networks: [lab]", "    command: sleep infinity",
              "", "networks:", "  lab:", "    internal: true", ""]
    tdir = ROOT / "targets" / a.id
    tdir.mkdir(parents=True, exist_ok=True)
    (tdir / "docker-compose.yml").write_text("\n".join(lines))

    proj = f"kalithos-dojo-{a.id}"
    cf = str(tdir / "docker-compose.yml")

    def compose(*args):
        return sh(["docker", "compose", "-p", proj, "-f", cf, *args])

    # avvio + poll health
    compose("up", "-d")
    hp = a.health_path
    health = (f"curl -s -o /dev/null -w '%{{http_code}}' --max-time 5 "
              f"http://{tname}:{a.port}{hp} | grep -qE '200|30[0-9]|401|403'")
    ok = False
    import time
    for _ in range(30):
        r = compose("exec", "-T", "attacker", "sh", "-c",
                    f"curl -s -o /dev/null -w '%{{http_code}}' --max-time 5 http://{tname}:{a.port}{hp}")
        code = r.stdout.strip()
        if code and code[0] in "2334":
            ok = True
            break
        time.sleep(5)
    if not ok:
        print(f"[{a.id}] HEALTH KO (porta {a.port}{hp} non risponde) -> SCARTO")
        compose("down", "-v")
        return 2

    # ispeziona flag_user (worker apache/nginx -> www-data; altrimenti uid del processo principale)
    fu = a.flag_user
    if not fu:
        probe = ('for d in /proc/[0-9]*; do c=$(cat $d/comm 2>/dev/null); u=$(awk "/^Uid:/{print \\$2}" $d/status 2>/dev/null); '
                 'echo "$u $c"; done | sort -u')
        out = compose("exec", "-T", tname, "sh", "-c", probe).stdout
        pairs = []  # (uid, comm)
        for l in out.splitlines():
            p = l.split(None, 1)
            if len(p) == 2 and p[0].isdigit():
                pairs.append((int(p[0]), p[1].strip()))
        SERVERS = ("apache", "httpd", "nginx", "php-fpm", "java", "beam", "erlang",
                   "python", "node", "couchdb", "neo4j", "gunicorn", "uwsgi", "ruby", "perl")
        # 1) worker web non-root gestisce le richieste (trappola master=root/worker=www-data)
        worker = next((u for u, c in pairs if u != 0 and any(k in c for k in
                       ("apache", "httpd", "nginx", "php-fpm", "gunicorn", "uwsgi"))), None)
        if worker is not None:
            uid = worker
        else:
            # 2) uid del processo server principale (preferisci non-root se il daemon gira de-privilegiato)
            srv = [(u, c) for u, c in pairs if any(k in c for k in SERVERS)]
            srv_nonroot = [u for u, c in srv if u != 0]
            uid = (srv_nonroot[0] if srv_nonroot else (srv[0][0] if srv else 0))
        # risolvi nome
        pw = compose("exec", "-T", tname, "sh", "-c", f"getent passwd {uid} 2>/dev/null || grep ':x:{uid}:' /etc/passwd").stdout
        fu = pw.split(":")[0] if ":" in pw else ("root" if uid == 0 else str(uid))
    print(f"[{a.id}] flag_user ISPEZIONATO = {fu}")
    compose("down", "-v")

    # scrivi target.toml
    fpath = "/root/flag.txt" if fu == "root" else "/tmp/flag.txt"
    toml = f'''target_id        = "{a.id}"

# --- harness ---
target_service   = "{tname}"
attacker_service = "attacker"
flag_path        = "{fpath}"
flag_user        = "{fu}"          # ISPEZIONATO via /proc
max_turns        = 40
exec_timeout     = 60
health_cmd       = "{health}"

[classification]
class = "{a.cls}"
stack = "{a.stack}"
split = "{a.split}"

[vulhub]
name  = "{a.vpath}"
path  = "{a.vpath}"
image = "{timg}"
license = "MIT (Vulhub)"
'''
    (tdir / "target.toml").write_text(toml)

    # healthcheck ufficiale
    env = {"KALITHOS_DOJO": str(ROOT)}
    import os
    hc = subprocess.run([sys.executable, str(ROOT.parent / "kalithos-cybersec/recipes/grpo-rt/env/healthcheck.py"),
                         "--target", a.id, "--wait", "30"],
                        env={**os.environ, **env}, capture_output=True, text=True)
    passed = "AMBIENTE OK" in hc.stdout
    print(hc.stdout.strip().splitlines()[-2] if hc.stdout else hc.stderr[-200:])
    print(f"[{a.id}] {'OK ✅' if passed else 'FAIL ❌'}  (class={a.cls} stack={a.stack} split={a.split} user={fu})")
    return 0 if passed else 3


if __name__ == "__main__":
    raise SystemExit(main())
