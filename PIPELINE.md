# PIPELINE — estrarre target da Vulhub (ripristinabile in una nuova sessione)

Come portare nuovi target da Vulhub nel dojo, in modo ripetibile e verificato. Pensata per
**riprendere da zero in un'altra sessione**: assume che scratchpad/tmp siano stati cancellati.

> Filosofia: la macchina fa la parte meccanica (pull/pin/compose/ispezione/healthcheck); l'umano
> mette solo **class/stack/split** e il giudizio sul `flag_user`. Chi non passa il gate **si
> auto-elimina** → niente debito. Vedi anche `ONBOARDING.md` (checklist manuale, singolo target).

## 0. Prerequisiti (una volta)

```bash
# 1) checkout di Vulhub (NON è vendorizzato qui: è la sorgente dei target)
git clone https://github.com/vulhub/vulhub ~/workspace/vulhub

# 2) variabili d'ambiente (mettile nel tuo profilo)
export VULHUB_DIR=~/workspace/vulhub
export KALITHOS_DOJO=~/workspace/kalithos-dojo
# harness kalithos-cybersec: default = repo fratello di questo; override se altrove:
# export KALITHOS_HARNESS=~/workspace/kalithos-cybersec/recipes/grpo-rt/env
```

- **Python**: serve **python3.12** (usa `tomllib`). `python3` di sistema (3.9) NON basta.
- **Dipendenze python**: `pyyaml` (per `tools/onboard.py` e `tools/survey.py`). `pip install pyyaml`.
- **Docker** attivo. Immagine attaccante `grpo-rt/kali-lite:latest` disponibile in locale.

## 1. Scegliere i candidati

```bash
python3.12 tools/survey.py --tag RCE --limit 40
```
Elenca i target Vulhub **taggati RCE**, di **app non ancora importate** (le esclude leggendo i
`target.toml` esistenti), ordinati per facilità (**image-based + single-service** prima). Ogni riga:
`path | app | kind | #svc | port | tags`. I `build`-based richiedono copiare il build-context a mano
(vedi `ONBOARDING.md`); `onboard.py` gestisce gli **image-based**.

## 2. Preparare la lista da onboardare

Un file di testo, una riga per target — decidi tu **class/stack/split** e la **porta interna**
(dalla colonna `port` del survey). Formato:

```
# id|vpath|class|stack|split|port|healthpath
fastjson-1-2-47-rce|fastjson/1.2.47-rce|deserialization|java|train|8090|/
nacos-cve-2021-29442|nacos/CVE-2021-29442|auth-bypass|java|train|8848|/nacos/
```
Regola **anti-leakage**: un `held-out` deve avere la sua classe coperta in `train` da un'**app diversa**
(coppia near-transfer). Se non esiste un gemello onesto, tienilo `train` (no coppie forzate).

## 3. Onboardare in batch

```bash
bash tools/onboard_batch.sh mylist.txt
```
Per ogni target: pull+**pin del digest**, genera compose isolato (**no ports**, rete `lab` internal,
attacker kali-lite), avvia, **ispeziona `flag_user` via /proc**, scrive `target.toml`, lancia
l'healthcheck, teardown. I falliti (health muto o healthcheck rosso) vengono **rimossi in automatico**.
Log per target in `/tmp/ob_<id>.log`.

> ⚠️ `flag_user` è **ispezionato** (euristica /proc + trappola apache master=root/worker=www-data),
> non è la conferma definitiva. Quella è il **solve-gate** (un exploit di riferimento che legge la
> flag) — offensivo, lo esegui tu; non è parte di questa pipeline.

## 4. Verificare tutto il pool

```bash
bash tools/verify_all.sh          # healthcheck fresco su OGNI target; exit!=0 se qualcuno fallisce
```

## 5. Rigenerare gli indici e committare

```bash
python3.12 tools/inventory.py     # rigenera IMPORTED.md + manifest.toml dai target.toml
git add -A && git commit -m "pool: onboard <...>" && git push
```
`IMPORTED.md` e `manifest.toml` sono **generati** — non modificarli a mano. `inventory.py --check`
fallisce se sono stale (aggancialo a un pre-commit se vuoi).

## Riassunto del flusso

```
survey.py  ->  scrivi lista  ->  onboard_batch.sh  ->  verify_all.sh  ->  inventory.py  ->  commit
(scegli)       (giudizio)        (meccanico+gate)      (certifica)        (indici)         (durevole)
```

## Note / trappole
- **Digest pinnato** sempre (immune a re-tag upstream) — lo fa `onboard.py`.
- **`build`-based** (compose con `build:` invece di `image:`): non gestiti da `onboard.py`; copia il
  build-context in `targets/<id>/build/` e pinna il `FROM` (vedi tomcat/struts2 come esempi).
- **Servizi non-HTTP** (RMI/SSH/DB puri): l'health via curl fallisce → si auto-eliminano. Se li vuoi,
  scrivi un `health_cmd` custom nel `target.toml` (es. `nc -z host porta`) e valida a mano.
- **Niente pipe** sul comando `onboard.py` in script custom: `... | tail` maschera l'exit code e
  segna PASS i FAIL. `onboard_batch.sh` è già corretto.
