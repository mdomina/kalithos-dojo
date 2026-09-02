#!/usr/bin/env python3.12
"""Genera IMPORTED.md dal contenuto dei target.toml (fonte unica).

Il registro dei target importati NON si scrive a mano: si rigenera da qui, così non va mai
fuori sync con le spec reali. Lega ogni target del dojo alla sua origine Vulhub (path/CVE),
alla classe/stack/split e al flag_user ispezionato.

Uso:  python3.12 tools/inventory.py        # riscrive IMPORTED.md
      python3.12 tools/inventory.py --check # esce 1 se IMPORTED.md è stale (per CI/pre-commit)

Richiede Python 3.11+ (tomllib).
"""
from __future__ import annotations

import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "IMPORTED.md"


def collect() -> list[dict]:
    rows = []
    for tt in sorted((ROOT / "targets").glob("*/target.toml")):
        d = tomllib.load(open(tt, "rb"))
        v = d.get("vulhub", {})
        c = d.get("classification", {})
        rows.append(
            dict(
                id=d["target_id"],
                path=v.get("path", "?"),
                cve=", ".join(v.get("cve", [])) or "—",
                app=v.get("app", "?"),
                cls=c.get("class", "?"),
                stack=c.get("stack", "?"),
                split=c.get("split", "?"),
                user=d.get("flag_user", "?"),
            )
        )
    rows.sort(key=lambda r: (r["split"] != "train", r["cls"], r["id"]))
    return rows


def render(rows: list[dict]) -> str:
    n_tr = sum(r["split"] == "train" for r in rows)
    n_ho = sum(r["split"] == "held-out" for r in rows)
    stacks = sorted({r["stack"] for r in rows})

    # classi misurabili = quelle con almeno un train E un held-out
    by_cls: dict[str, set] = {}
    for r in rows:
        by_cls.setdefault(r["cls"], set()).add(r["split"])
    measurable = sorted(c for c, s in by_cls.items() if {"train", "held-out"} <= s)
    train_only = sorted(c for c, s in by_cls.items() if s == {"train"})

    lines = [
        "# Target importati (registro)",
        "",
        "**GENERATO** da `tools/inventory.py` a partire dai `target.toml` — non modificare a mano.",
        "Rigenera con: `python3.12 tools/inventory.py`.",
        "",
        f"Totale: **{len(rows)}** target — {n_tr} train + {n_ho} held-out. Stack: {', '.join(stacks)}.",
        "",
        f"Classi misurabili (coppia train+held-out): **{', '.join(measurable)}**.  ",
        f"Classi train-only (unicum onesti): {', '.join(train_only) or '—'}.",
        "",
        "| split | classe | stack | target (dojo) | origine vulhub | CVE | flag_user |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['split']} | {r['cls']} | {r['stack']} | `{r['id']}` | "
            f"`{r['path']}` | {r['cve']} | {r['user']} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    content = render(collect())
    if "--check" in sys.argv:
        cur = OUT.read_text() if OUT.exists() else ""
        if cur != content:
            print("IMPORTED.md è STALE — rigenera con: python3.12 tools/inventory.py", file=sys.stderr)
            return 1
        print("IMPORTED.md aggiornato ✅")
        return 0
    OUT.write_text(content)
    print(f"scritto {OUT.relative_to(ROOT)} ({len(collect())} target)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
