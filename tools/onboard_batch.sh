#!/bin/bash
# Batch onboarding: esegue tools/onboard.py per ogni riga di un file-lista.
# Chi non passa (health o healthcheck) si AUTO-ELIMINA: la sua dir viene rimossa, niente debito.
#
# Uso:  bash tools/onboard_batch.sh <lista.txt> [python]
#   lista.txt: una riga per target, formato:
#     id|vpath|class|stack|split|port|healthpath[|scheme|codes|cmd]
#   es:        fastjson-1-2-47-rce|fastjson/1.2.47-rce|deserialization|java|train|8090|/
#   Colonne 8-10 opzionali (default: http | 200|30[0-9]|401|403 | vuoto=usa curl HTTP):
#     scheme = http|https  (https -> curl -k)
#     codes  = regex ERE dei codici HTTP accettati (es. '200|30[0-9]|401|403|404' per h2)
#     cmd    = comando health custom (bypassa curl; es. "nc -z {tname} {port}" per non-HTTP)
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
while IFS='|' read -r id vpath cls stack split port hp scheme codes hcmd; do
  [ -z "${id:-}" ] && continue
  case "$id" in \#*) continue;; esac
  hp="${hp:-/}"; scheme="${scheme:-http}"; codes="${codes:-200|30[0-9]|401|403}"
  extra=(--health-scheme "$scheme" --health-codes "$codes")
  [ -n "${hcmd:-}" ] && extra+=(--health-cmd "$hcmd")
  echo "### ONBOARD $id ($vpath) port=$port scheme=$scheme"
  # NB: `< /dev/null` sul child. Senza, i `docker compose exec -T` interni a
  # onboard.py ereditano lo stdin del padre (il file-lista) e mangiano la riga
  # successiva -> la 2ª voce del batch veniva sistematicamente saltata.
  "$PY" tools/onboard.py --vpath "$vpath" --id "$id" --class "$cls" \
        --stack "$stack" --split "$split" --port "$port" --health-path "$hp" \
        "${extra[@]}" \
        > "/tmp/ob_$id.log" 2>&1 < /dev/null
  rc=$?                                   # exit-code diretto, NIENTE pipe
  if [ $rc -eq 0 ]; then
    PASS+=("$id"); echo "  PASS $(grep -o 'user=[^ )]*' "/tmp/ob_$id.log" | tail -1)"
  else
    FAIL+=("$id"); rm -rf "targets/$id"
    echo "  FAIL($rc) $(grep -E 'HEALTH KO|FAIL ❌|Traceback' "/tmp/ob_$id.log" | head -1)"
  fi
done < "$LIST"

echo "===== RIEPILOGO ====="
echo "PASS (${#PASS[@]}): ${PASS[*]:-}"
echo "FAIL (${#FAIL[@]}): ${FAIL[*]:-}"
echo "Ora rigenera gli indici:  python3.12 tools/inventory.py"
