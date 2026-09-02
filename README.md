# kalithos-dojo

**Cyber range** curato per il training agentico di penetration testing: una collezione di
**bersagli vulnerabili dockerizzati**, ognuno verificato a mano e pronto a dare un **reward
verificabile** (flag + milestone) a un agente RL.

- **Range, non gym**: qui stanno i *bersagli* (il contenuto). L'*interfaccia RL* (reset/step/reward)
  la dà l'harness (`kalithos-cybersec/recipes/grpo-rt`) o `verifiers`/`prime-rl`. Strati separati.
- **Licenza pulita**: i target derivano da **Vulhub (MIT)**, copiati con attribuzione (vedi
  [ATTRIBUTION.md](ATTRIBUTION.md)). Codice di questo repo: MIT. → **usabile commercialmente**.
- **Purpose-built, non auto-generato**: ogni target è **curato e validato** a mano (il `flag_user`,
  il privilegio, la solvibilità non si inferiscono in modo affidabile — vedi [ONBOARDING.md](ONBOARDING.md)).

## Struttura
```
targets/<id>/
  docker-compose.yml   # compose Vulhub, immagine PINNATA a digest (stabilità)
  target.toml          # spec DICHIARATIVA (target_service, flag_path, flag_user, classe, split, provenienza)
  milestones.py        # (opz.) oracoli evidence-based per il reward shaped
manifest.toml          # indice: classe / stack / split (train | held-out)
ONBOARDING.md          # la checklist fissa per aggiungere un target
ATTRIBUTION.md         # provenienza Vulhub + licenze
```

## Come si usa
L'harness legge `targets/<id>/target.toml` e costruisce l'ambiente (`docker compose up` isolato,
inietta flag random, verifica). Aggiungere un target = seguire [ONBOARDING.md](ONBOARDING.md).

## Requisiti di stabilità (perché non è fragile)
1. **Digest pinning**: le immagini sono fissate a `@sha256:...` → immuni a re-tag/rimozioni upstream.
2. **Checklist di curazione**: ogni target passa gli stessi step, verificato (non "a naso").
3. **Gate di validazione**: nessun target entra nel pool senza `healthcheck` PASS.

## Split train / held-out
Il manifest divide i target per **classe** (RCE/SQLi/…) e **stack** (java/php/…), con uno split
**train / held-out**. L'held-out è **congelato**: mai usato in training, solo per misurare la
*generalizzazione* (comportamento appreso, non exploit memorizzato).
