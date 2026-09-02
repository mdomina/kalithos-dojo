# Target importati (registro)

**GENERATO** da `tools/inventory.py` a partire dai `target.toml` — non modificare a mano.
Rigenera con: `python3.12 tools/inventory.py`.

Totale: **14** target — 8 train + 6 held-out. Stack: java, other, php, python.

Classi misurabili (coppia train+held-out): **command-injection, deserialization, ognl, ssti, upload-webshell**.  
Classi train-only (unicum onesti): form-rce, unauth-rce.

| split | classe | stack | target (dojo) | origine vulhub | CVE | flag_user |
|---|---|---|---|---|---|---|
| train | command-injection | php | `thinkphp-5-rce` | `thinkphp/5-rce` | — | www-data |
| train | deserialization | php | `joomla-cve-2015-8562` | `joomla/CVE-2015-8562` | CVE-2015-8562 | www-data |
| train | deserialization | java | `weblogic-cve-2017-10271` | `weblogic/CVE-2017-10271` | CVE-2017-10271 | root |
| train | form-rce | php | `drupal-cve-2018-7600` | `drupal/CVE-2018-7600` | CVE-2018-7600 | www-data |
| train | ognl | java | `struts2-s2-001` | `struts2/s2-001` | — | root |
| train | ssti | python | `flask-ssti` | `flask/ssti` | — | www-data |
| train | unauth-rce | other | `redis-4-unacc` | `redis/4-unacc` | — | redis |
| train | upload-webshell | java | `tomcat-cve-2017-12615` | `tomcat/CVE-2017-12615` | CVE-2017-12615 | root |
| held-out | command-injection | php | `cacti-cve-2022-46169` | `cacti/CVE-2022-46169` | CVE-2022-46169 | www-data |
| held-out | deserialization | php | `phpmyadmin-wooyun-2016-199433` | `phpmyadmin/WooYun-2016-199433` | — | www-data |
| held-out | deserialization | java | `shiro-cve-2016-4437` | `shiro/CVE-2016-4437` | CVE-2016-4437 | root |
| held-out | ognl | java | `confluence-cve-2022-26134` | `confluence/CVE-2022-26134` | CVE-2022-26134 | confluence |
| held-out | ssti | java | `solr-cve-2019-17558` | `solr/CVE-2019-17558` | CVE-2019-17558 | root |
| held-out | upload-webshell | java | `activemq-cve-2016-3088` | `activemq/CVE-2016-3088` | CVE-2016-3088 | root |
