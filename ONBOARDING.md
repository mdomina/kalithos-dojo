# Onboarding di un target (checklist fissa)

Procedura **ripetibile e verificata**. Un target **non entra nel pool** finché non passa tutti
gli step. Niente auto-generazione cieca: il `flag_user`/privilegio/solvibilità richiedono giudizio
+ validazione (per questo il range è *purpose-built*, non generato).

## Passi
1. **Scegli dal catalogo Vulhub** (`environments.toml`, filtra per `tags`). Preferisci **image-based**
   (un solo servizio + immagine); i **build-based** richiedono copiare il build-context.

2. **Compose** → copia il compose Vulhub in `targets/<id>/docker-compose.yml` e:
   - **pinna il digest**: `docker inspect --format '{{index .RepoDigests 0}}' <image:tag>` →
     usa `image: repo@sha256:...` (stabilità: immune a re-tag upstream);
   - **togli `ports:`** (isolamento);
   - aggiungi rete `lab: { internal: true }` (zero-egress) + servizio `attacker` (kali-lite).

3. **Determina `flag_user` ISPEZIONANDO** (non indovinare) — l'RCE gira come l'utente che
   **gestisce le richieste**, non necessariamente il master del processo:
   ```bash
   docker compose -f targets/<id>/docker-compose.yml up -d
   docker compose exec <svc> ps -o user= -o comm= | sort -u
   ```
   ⚠️ **Trappola apache/nginx**: il **master** gira come **root**, i **worker** come **www-data**.
   Il codice (PHP/app) esegue nel **worker** → `flag_user = www-data`, NON root. Un `ps` ingenuo
   mostra il master root e ti inganna. Regola: prendi l'utente **non-root** che gestisce le richieste.
   `flag_path` in una dir che lui legge (es. `/tmp/flag.txt`).
   👉 **La conferma DEFINITIVA di `flag_user` è il solve-gate (step 7)**: se un solve di riferimento
   legge la flag, l'utente è giusto. Il `ps` è solo un indizio.

4. **`target.toml`** → scrivi la spec dichiarativa: `target_service`, `flag_path`, `flag_user`,
   `max_turns`, `exec_timeout`, `health_cmd`, + `[classification]` (class/stack/split) +
   `[provenance]` (source, image-digest, licenza).

5. **Milestone** (opz., raccomandato) → `milestones.py` con oracoli **evidence-based** per la classe
   (reward shaped, non binario). Es. RCE: "processo estraneo comparso".

6. **VALIDA** → `healthcheck` deve dare PASS su: build+avvio · servizio risponde · flag piazzata al
   privilegio giusto (owner+600) · zero-egress · teardown pulito. **FAIL = non entra.**

7. **(Opz.) solve-gate** → un tentativo di riferimento cattura la flag = conferma solvibilità
   (difficulty-filter). Se nessuno la cattura → droppato.

8. **Manifest** → aggiungi la riga in `manifest.toml` con lo **split** (train | held-out).
   L'held-out è **congelato**: mai in training.

## Regole d'oro
- **Ispeziona, non indovinare** il `flag_user` (step 3).
- **Digest pinnato** sempre (step 2).
- **Held-out per app intera**, con la classe coperta altrove in train (no leakage).
- Un'ipotesi sbagliata **si auto-elimina** al gate healthcheck/solve — non avvelena il pool.
