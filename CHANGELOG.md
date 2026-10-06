# Changelog

Modifiche ai target del dojo. Formato ispirato a [Keep a Changelog](https://keepachangelog.com/it/1.1.0/).
Date in ISO (AAAA-MM-GG).

## [Unreleased]

### Fix milestone `file_created` su 2 target di training (2026-10-06)

Ricognizione dei container (via Docker) mentre si progettavano le milestone pre-foothold: trovati e
corretti 2 bug dove la milestone `file_created` puntava a una dir che **non catturava l'artefatto**
dell'exploit, perché l'oracolo faceva `ls` NON ricorsivo (fix strutturale lato motore: in
kalithos-dolos `file_created` è ora ricorsivo con `find`). Effetto del bug: le milestone **non
scattavano mai** → il modello faceva l'exploit corretto senza ricevere alcun reward (sabotava il
training a monte, a prescindere dal cold-start).

#### Corretto
- **tomcat-cve-2017-12615** (train): `dir` `/usr/local/tomcat/webapps` → `/usr/local/tomcat/webapps/ROOT`.
  Il PUT (CVE-2017-12615) scrive la webshell in `webapps/ROOT/<x>.jsp`. Verificato sul container:
  `PUT /x.jsp/` → 201 → `/usr/local/tomcat/webapps/ROOT/x.jsp`.
- **elfinder-cve-2021-32682** (train): `dir` `/var/www/html` → `/var/www/html/files`. elFinder gestisce
  i file nella volume root `files/` (contiene `.trash`), non nella webroot. Verificato per ispezione.

#### Verificato — nessun cambiamento
- **activemq-cve-2016-3088** (held-out): milestone `file_created` su `/opt/activemq/webapps/api` è
  corretta — `/opt/activemq` è un symlink valido a `apache-activemq-5.11.1` e la JSP spostata finisce
  direttamente in `api/` (non in sottodir). Non modificato (held-out / congelato per l'eval finale).

#### Nota
Nuovo oracolo milestone **`access_log`** disponibile lato motore (kalithos-dolos/verifier.py) per un
segnale PRE-foothold anti-hacking basato sul log del target. **Non applicato ai target vulhub attuali**
perché non espongono un access log HTTP affidabile (ActiveMQ non logga; Tomcat ha l'AccessLogValve ma
bufferizzata e col nome-file datato). Utile per eventuali futuri target con web server standard
(nginx/apache) e access log a path fisso.
