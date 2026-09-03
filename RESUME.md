# RESUME — riprendere la migrazione del dojo

Prompt autosufficiente da incollare in una sessione nuova per continuare a portare target
Vulhub nel pool. Dettaglio operativo completo in [PIPELINE.md](PIPELINE.md).

```
Riprendiamo la migrazione dei target Vulhub nel cyber-range kalithos-dojo
(~/workspace/kalithos-dojo, repo github.com/mdomina/kalithos-dojo).

STATO ATTUALE
- Pool a 34 target (26 train + 8 held-out), tutti healthcheck 4/4, digest-pinnati,
  zero-egress, attaccante kali-lite. Registro in IMPORTED.md, indici in manifest.toml
  (entrambi GENERATI dai target.toml, non a mano).
- La pipeline completa e ripristinabile è documentata in kalithos-dojo/PIPELINE.md.
- 7 classi con coppia misurabile: deserialization, ognl, upload-webshell,
  command-injection, ssti, auth-bypass, cgi-rce. Classi train-only (unicum onesti):
  form-rce, unauth-rce, code-injection, expression-injection, file-inclusion, rce.

OBIETTIVO
Continuare ad ampliare il pool RCE con altri target Vulhub, seguendo PIPELINE.md.
Priorità: chiudere coppie train/held-out ONESTE (stessa classe, app diversa =
near-transfer), NON coppie forzate. Diversificare stack (java/php/python/other).

SETUP (i file effimeri di /tmp vanno persi tra sessioni)
  git clone https://github.com/vulhub/vulhub ~/workspace/vulhub   # se assente
  export VULHUB_DIR=~/workspace/vulhub
  export KALITHOS_DOJO=~/workspace/kalithos-dojo
  export KALITHOS_HARNESS=~/workspace/kalithos-cybersec/recipes/grpo-rt/env
  # serve python3.12 (tomllib) + pyyaml; python con pyarrow = ~/workspace/redteamLLM/venv

FLUSSO (da PIPELINE.md)
  1) python3.12 tools/survey.py --tag RCE --limit 40   # candidati app-nuove
  2) scrivi una lista  id|vpath|class|stack|split|port|healthpath
  3) bash tools/onboard_batch.sh lista.txt             # batch, auto-elimina i falliti
  4) bash tools/verify_all.sh                          # healthcheck su tutto il pool
  5) python3.12 tools/inventory.py                     # rigenera IMPORTED.md + manifest.toml
  6) git add -A && commit + push

REGOLE FISSE (memoria)
- Rispondi in italiano, conciso, una decisione per volta.
- Mai installare software/modelli né avviare servizi senza mio ok esplicito
  (pull di immagini docker per l'onboarding = ok, è il lavoro del pool).
- flag_user va ISPEZIONATO, non indovinato (trappola apache master=root/worker=www-data).
  La conferma definitiva è il solve-gate, che è offensivo e lo eseguo io, non tu.
- Niente exploit scritti a mano committati nei repo.
- build-based (compose con build:) non gestiti da onboard.py: copia il build-context
  e pinna il FROM (vedi tomcat/struts2 come esempio).

Comincia proponendomi ~1 batch di candidati (con classe/split motivati), poi aspetta
il mio ok prima di lanciare l'onboarding.
```
