#!/bin/bash
# Ricontrollo completo: healthcheck fresco su OGNI target del pool (avvio->flag->isolamento->teardown).
# NON esegue exploit/LLM/crediti — certifica solo la PALESTRA. Da lanciare dopo un batch o prima di un commit.
#
# Uso:  bash tools/verify_all.sh [python]
# Prerequisiti: KALITHOS_DOJO impostato (o repo in ~/workspace/kalithos-dojo), harness kalithos-cybersec
# raggiungibile (env KALITHOS_HARNESS o repo fratello), Docker attivo, python3.12.
set -u
DOJO="${KALITHOS_DOJO:-$(cd "$(dirname "$0")/.." && pwd)}"
PY="${2:-python3.12}"
HARNESS="${KALITHOS_HARNESS:-$(cd "$DOJO/.." && pwd)/kalithos-cybersec/recipes/grpo-rt/env}"
export KALITHOS_DOJO="$DOJO"
cd "$HARNESS" || { echo "harness non trovato: $HARNESS (imposta KALITHOS_HARNESS)"; exit 2; }

PASS=(); FAIL=()
for d in "$DOJO"/targets/*/; do
  id=$(basename "$d"); [ -f "$d/target.toml" ] || continue
  out=$("$PY" healthcheck.py --target "$id" --wait 35 2>&1)
  if echo "$out" | grep -q "AMBIENTE OK"; then PASS+=("$id"); echo "PASS  $id"
  else FAIL+=("$id"); echo "FAIL  $id"; echo "$out" | grep -E '\[FAIL|\[SKIP' | sed 's/^/      /'; fi
done
echo "===== VERIFY ALL ====="
echo "PASS: ${#PASS[@]}  |  FAIL: ${#FAIL[@]}  ${FAIL[*]}"
[ "${#FAIL[@]}" -eq 0 ]
