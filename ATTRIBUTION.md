# Attribution

I bersagli di questo range derivano da **Vulhub** (https://github.com/vulhub/vulhub),
licenza **MIT**. I `docker-compose.yml` qui sono copie/adattamenti dei compose Vulhub, con
l'immagine **pinnata a digest** e la rete resa isolata (zero-egress) + attaccante aggiunto.

Vulhub — Copyright (c) Vulhub contributors — MIT License.
Il testo MIT di Vulhub si applica alle porzioni derivate; vedi il loro repository.

## Provenienza per target
| target dir | fonte Vulhub | immagine (pinnata) | licenza |
|---|---|---|---|
| thinkphp-5-rce | vulhub/thinkphp/5-rce | vulhub/thinkphp@sha256:aa12db1b…56c | MIT |
| drupal-cve-2018-7600 | vulhub/drupal/CVE-2018-7600 | vulhub/drupal@sha256:fa3e60bf…662 | MIT |

Ogni `target.toml` riporta la `source` e l'`image` (digest) nella sezione `[provenance]`.

L'immagine attaccante (`kali-lite`) è parte dell'harness, non di Vulhub: vedi il repo dell'harness.
