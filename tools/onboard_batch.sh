#!/bin/bash
# Batch onboarding: esegue tools/onboard.py per ogni riga di un file-lista.
# Chi non passa (health o healthcheck) si AUTO-ELIMINA: la sua dir viene rimossa, niente debito.
#
# Uso:  bash tools/onboard_batch.sh <lista.txt> [python]
#   lista.txt: una riga per target, formato:  id|vpath|class|stack|split|port|healthpath
#   es:        fastjson-1-2-47-rce|fastjson/1.2.47-rce|deserialization|java|train|8090|/
#   healthpath opzionale (default /). Righe vuote o con # iniziale ignorate.
#
# Prerequisiti: VULHUB_DIR e KALITHOS_DOJO impostati (vedi PIPELINE.md), Docker attivo,
# python3.12 con pyyaml. NB: NON usare pipe sul comando onboard (maschera l'exit code).
set -u
HERE="$(cd "$(dirname "$0")/.." && pwd)"
LIST="${1:?serve un file-lista: id|vpath|class|stack|split|port|healthpath}"
PY="${2:-python3.12}"
cd "$HERE"

PASS=(); FAIL=()
while IFS='|' read -r id vpath cls stack split port hp; do
  [ -z "${id:-}" ] && continue
  case "$id" in \#*) continue;; esac
  hp="${hp:-/}"
  echo "### ONBOARD $id ($vpath) port=$port"
  "$PY" tools/onboard.py --vpath "$vpath" --id "$id" --class "$cls" \
        --stack "$stack" --split "$split" --port "$port" --health-path "$hp" \
        > "/tmp/ob_$id.log" 2>&1
  rc=$?                                   # exit-code diretto, NIENTE pipe
  if [ $rc -eq 0 ]; then
    PASS+=("$id"); echo "  PASS $(grep -o 'user=[^ )]*' "/tmp/ob_$id.log" | tail -1)"
  else
    FAIL+=("$id"); rm -rf "targets/$id"
    echo "  FAIL($rc) $(grep -E 'HEALTH KO|FAIL ❌|Traceback' "/tmp/ob_$id.log" | head -1)"
  fi
done < "$LIST"

echo "===== RIEPILOGO ====="
echo "PASS (${#PASS[@]}): ${PASS[*]}"
echo "FAIL (${#FAIL[@]}): ${FAIL[*]}"
echo "Ora rigenera gli indici:  python3.12 tools/inventory.py"
