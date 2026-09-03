#!/usr/bin/env python3.12
"""Survey dei candidati Vulhub da onboardare: RCE, app NON già importate, ordinati per facilità.

Legge VULHUB_DIR/environments.toml (tag/app/path) + i docker-compose per capire
image-based vs build, n. servizi, porta interna del target. Esclude le app già nel pool
(derivate da targets/*/target.toml). Stampa una riga pronta per la lista di onboard_batch.sh.

Uso:  python3.12 tools/survey.py [--limit 40] [--tag RCE]
Env:  VULHUB_DIR (default ~/workspace/vulhub). Richiede pyyaml + py3.11+ (tomllib).
"""
from __future__ import annotations

import argparse
import os
import re
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VULHUB = Path(os.environ.get("VULHUB_DIR", str(Path.home() / "workspace" / "vulhub")))


def imported_apps() -> set[str]:
    apps = set()
    for tt in (ROOT / "targets").glob("*/target.toml"):
        d = tomllib.load(open(tt, "rb"))
        p = d.get("vulhub", {}).get("path", "")
        if "/" in p:
            apps.add(p.split("/")[0])
    return apps


def compose_info(cf: Path):
    try:
        d = yaml.safe_load(open(cf))
    except Exception:
        return None
    svcs = (d or {}).get("services", {})
    if not svcs:
        return None
    tname = next((n for n, s in svcs.items() if s and "ports" in s), list(svcs)[0])
    s = svcs[tname] or {}
    kind = "build" if "build" in s else ("image" if "image" in s else "?")
    port = None
    if s.get("ports"):
        port = str(s["ports"][0]).split(":")[-1].strip().strip('"').split("/")[0]
    return kind, len(svcs), port


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--tag", default="RCE", help="tag Vulhub da filtrare (default RCE)")
    a = ap.parse_args()

    env = VULHUB / "environments.toml"
    if not env.exists():
        print(f"environments.toml non trovato in {VULHUB} — imposta VULHUB_DIR o clona vulhub "
              f"(git clone https://github.com/vulhub/vulhub)")
        return 2

    txt = env.read_text()
    meta = {}
    for b in re.split(r'\n\[\[environment\]\]', txt):
        mp = re.search(r'path = "([^"]+)"', b)
        mt = re.search(r'tags = (\[[^\]]*\])', b)
        ma = re.search(r'app = "([^"]+)"', b)
        if mp:
            meta[mp.group(1)] = {"tags": mt.group(1) if mt else "[]",
                                 "app": ma.group(1) if ma else "?"}

    used = imported_apps()
    rows = []
    for cf in VULHUB.glob("*/*/docker-compose.yml"):
        p = str(cf.parent.relative_to(VULHUB))
        if p.startswith("base/") or p.split("/")[0] in used:
            continue
        m = meta.get(p)
        if not m or a.tag not in m["tags"]:
            continue
        ci = compose_info(cf)
        if not ci:
            continue
        rows.append((p, m["app"], ci[0], ci[1], ci[2], m["tags"]))

    rows.sort(key=lambda r: (r[2] != "image", r[3]))   # image-based e single-service prima
    print(f"# candidati Vulhub tag={a.tag}, app nuove (escluse {len(used)} già importate): {len(rows)}")
    print(f"# colonne: path | app | kind | #svc | port | tags   (i build-based richiedono copiare il build-context)")
    for p, app, kind, n, port, tags in rows[:a.limit]:
        print(f"{p:36} {app:16} {kind:6} svc={n} port={port or '?':6} {tags}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
