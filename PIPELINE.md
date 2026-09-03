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
(dalla colonna `port` del survey). Formato base:

```
# id|vpath|class|stack|split|port|healthpath
fastjson-1-2-47-rce|fastjson/1.2.47-rce|deserialization|java|train|8090|/
nacos-cve-2021-29442|nacos/CVE-2021-29442|auth-bypass|java|train|8848|/nacos/
```

Regola **anti-leakage**: un `held-out` deve avere la sua classe coperta in `train` da un'**app diversa**
(coppia near-transfer). Se non esiste un gemello onesto, tienilo `train` (no coppie forzate).

**Colonne extra opzionali** (8-10) per servizi che non rispondono al default `curl http://` con
codici `200|30[0-9]|401|403`:

```
# id|vpath|class|stack|split|port|healthpath|scheme|codes|cmd
h2database-cve-2018-10054|h2database/CVE-2018-10054|code-injection|java|held-out|8080|/||200|30[0-9]|401|403|404|
saltstack-cve-2020-16846|saltstack/CVE-2020-16846|unauth-rce|python|held-out|8000|/|https||
samba-cve-2017-7494|samba/CVE-2017-7494|unauth-rce|other|held-out|445|/|||nc -z {tname} {port}
```

- `scheme` = `http`|`https`. `https` invoca `curl -k` (accetta cert self-signed).
- `codes` = regex ERE dei codici HTTP accettati. Serve p.es. per app che rispondono **404 su `/`**
  (h2database, spring senza root handler): aggiungi `|404` al default.
- `cmd` = comando health custom (bypassa curl). Usalo per **servizi non-HTTP** (SMB/SMTP/RMI puri):
  `nc -z {tname} {port}` verifica il TCP-connect. `{tname}`/`{port}` vengono sostituiti.
  Con `cmd` presente, `scheme` e `codes` sono ignorati.

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
- **Servizi non-HTTP / HTTPS-only / codici non standard**: NON scartarli — usa le colonne extra
  (`scheme`/`codes`/`cmd`) documentate al passo 2. Non serve più editare a mano `target.toml`.
- **Niente pipe** sul comando `onboard.py` in script custom: `... | tail` maschera l'exit code e
  segna PASS i FAIL. `onboard_batch.sh` è già corretto.
- **Baco stdin risolto**: `onboard.py` chiamato da uno script che legge un file va invocato con
  `< /dev/null` — senza, i `docker compose exec -T` interni ereditano lo stdin del padre e
  "mangiano" bytes del file-lista (fix già applicato in `onboard_batch.sh`).
