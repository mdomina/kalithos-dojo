# Target importati (registro)

**GENERATO** da `tools/inventory.py` a partire dai `target.toml` — non modificare a mano.
Rigenera con: `python3.12 tools/inventory.py`.

Totale: **79** target — 66 train + 13 held-out. Stack: go, java, js, other, perl, php, python.

Classi misurabili (coppia train+held-out): **arbitrary-file-read, auth-bypass, cgi-rce, code-injection, command-injection, deserialization, expression-injection, file-inclusion, ognl, ssti, unauth-rce, upload-webshell**.  
Classi train-only (unicum onesti): form-rce, rce.

| split | classe | stack | target (dojo) | origine vulhub | CVE | flag_user |
|---|---|---|---|---|---|---|
| train | arbitrary-file-read | java | `apache-cxf-cve-2024-28752` | `apache-cxf/CVE-2024-28752` | — | root |
| train | arbitrary-file-read | go | `grafana-cve-2021-43798` | `grafana/CVE-2021-43798` | — | grafana |
| train | auth-bypass | java | `nacos-cve-2021-29442` | `nacos/CVE-2021-29442` | — | root |
| train | auth-bypass | java | `ofbiz-cve-2023-51467` | `ofbiz/CVE-2023-51467` | — | root |
| train | cgi-rce | php | `php-cve-2012-1823` | `php/CVE-2012-1823` | — | www-data |
| train | code-injection | java | `apache-druid-cve-2021-25646` | `apache-druid/CVE-2021-25646` | — | root |
| train | code-injection | java | `elasticsearch-cve-2014-3120` | `elasticsearch/CVE-2014-3120` | — | root |
| train | code-injection | java | `geoserver-cve-2022-24816` | `geoserver/CVE-2022-24816` | — | root |
| train | code-injection | java | `jenkins-cve-2018-1000861` | `jenkins/CVE-2018-1000861` | — | jenkins |
| train | code-injection | java | `metabase-cve-2023-38646` | `metabase/CVE-2023-38646` | — | metabase |
| train | command-injection | java | `opentsdb-cve-2020-35476` | `opentsdb/CVE-2020-35476` | — | root |
| train | command-injection | java | `opentsdb-cve-2023-25826` | `opentsdb/CVE-2023-25826` | — | root |
| train | command-injection | other | `postgres-cve-2019-9193` | `postgres/CVE-2019-9193` | — | postgres |
| train | command-injection | php | `thinkphp-5-rce` | `thinkphp/5-rce` | — | www-data |
| train | command-injection | perl | `webmin-cve-2019-15107` | `webmin/CVE-2019-15107` | — | root |
| train | deserialization | java | `apereo-cas-4-1-rce` | `apereo-cas/4.1-rce` | — | root |
| train | deserialization | java | `coldfusion-cve-2017-3066` | `coldfusion/CVE-2017-3066` | — | coldfusion |
| train | deserialization | java | `coldfusion-cve-2023-26360` | `coldfusion/CVE-2023-26360` | — | cfuser |
| train | deserialization | java | `fastjson-1-2-24-rce` | `fastjson/1.2.24-rce` | — | root |
| train | deserialization | java | `fastjson-1-2-47-rce` | `fastjson/1.2.47-rce` | — | root |
| train | deserialization | java | `fastjson-1-2-83-rce` | `fastjson/1.2.83-rce` | — | root |
| train | deserialization | java | `hertzbeat-cve-2024-42323` | `hertzbeat/CVE-2024-42323` | — | root |
| train | deserialization | java | `jackson-cve-2017-7525` | `jackson/CVE-2017-7525` | — | root |
| train | deserialization | java | `jboss-cve-2017-12149` | `jboss/CVE-2017-12149` | — | root |
| train | deserialization | java | `jboss-cve-2017-7504` | `jboss/CVE-2017-7504` | — | root |
| train | deserialization | java | `jboss-jmxinvokerservlet` | `jboss/JMXInvokerServlet-deserialization` | — | root |
| train | deserialization | java | `jenkins-cve-2017-1000353` | `jenkins/CVE-2017-1000353` | — | jenkins |
| train | deserialization | php | `joomla-cve-2015-8562` | `joomla/CVE-2015-8562` | CVE-2015-8562 | www-data |
| train | deserialization | java | `kafka-cve-2023-25194` | `kafka/CVE-2023-25194` | — | root |
| train | deserialization | java | `neo4j-cve-2021-34371` | `neo4j/CVE-2021-34371` | — | neo4j |
| train | deserialization | python | `superset-cve-2023-37941` | `superset/CVE-2023-37941` | — | root |
| train | deserialization | java | `weblogic-cve-2017-10271` | `weblogic/CVE-2017-10271` | CVE-2017-10271 | root |
| train | deserialization | java | `xstream-cve-2021-21351` | `xstream/CVE-2021-21351` | — | root |
| train | deserialization | java | `xstream-cve-2021-29505` | `xstream/CVE-2021-29505` | — | root |
| train | expression-injection | java | `elasticsearch-cve-2015-1427` | `elasticsearch/CVE-2015-1427` | — | root |
| train | expression-injection | java | `geoserver-cve-2024-36401` | `geoserver/CVE-2024-36401` | — | root |
| train | expression-injection | java | `hugegraph-cve-2024-27348` | `hugegraph/CVE-2024-27348` | — | root |
| train | expression-injection | java | `log4j-cve-2021-44228` | `log4j/CVE-2021-44228` | — | root |
| train | expression-injection | java | `spring-cve-2016-4977` | `spring/CVE-2016-4977` | — | root |
| train | expression-injection | java | `spring-cve-2017-4971` | `spring/CVE-2017-4971` | — | root |
| train | expression-injection | java | `spring-cve-2017-8046` | `spring/CVE-2017-8046` | — | root |
| train | expression-injection | java | `spring-cve-2018-1270` | `spring/CVE-2018-1270` | — | root |
| train | expression-injection | java | `spring-cve-2018-1273` | `spring/CVE-2018-1273` | — | root |
| train | expression-injection | java | `spring-cve-2022-22947` | `spring/CVE-2022-22947` | — | root |
| train | expression-injection | java | `spring-cve-2022-22963` | `spring/CVE-2022-22963` | — | root |
| train | file-inclusion | php | `php-inclusion` | `php/inclusion` | — | www-data |
| train | form-rce | php | `drupal-cve-2018-7600` | `drupal/CVE-2018-7600` | CVE-2018-7600 | www-data |
| train | ognl | java | `struts2-s2-001` | `struts2/s2-001` | — | root |
| train | rce | python | `comfyui-cve-2025-67303` | `comfyui/CVE-2025-67303` | — | root |
| train | rce | python | `comfyui-cve-2026-22777` | `comfyui/CVE-2026-22777` | — | root |
| train | rce | go | `gitea-1-4-rce` | `gitea/1.4-rce` | — | root |
| train | rce | java | `kkfileview-4-3-zipslip-rce` | `kkfileview/4.3-zipslip-rce` | — | root |
| train | rce | php | `laravel-cve-2021-3129` | `laravel/CVE-2021-3129` | — | www-data |
| train | rce | java | `nexus-cve-2019-7238` | `nexus/CVE-2019-7238` | — | root |
| train | rce | other | `openclaw-cve-2026-25253` | `openclaw/CVE-2026-25253` | — | root |
| train | rce | php | `phpunit-cve-2017-9841` | `phpunit/CVE-2017-9841` | — | www-data |
| train | rce | php | `showdoc-cnvd-2020-26585` | `showdoc/CNVD-2020-26585` | — | www-data |
| train | rce | java | `spring-cve-2022-22965` | `spring/CVE-2022-22965` | — | root |
| train | ssti | python | `flask-ssti` | `flask/ssti` | — | www-data |
| train | unauth-rce | other | `couchdb-cve-2017-12636` | `couchdb/CVE-2017-12636` | — | couchdb |
| train | unauth-rce | other | `couchdb-cve-2022-24706` | `couchdb/CVE-2022-24706` | — | root |
| train | unauth-rce | other | `redis-4-unacc` | `redis/4-unacc` | — | redis |
| train | unauth-rce | python | `saltstack-cve-2020-16846` | `saltstack/CVE-2020-16846` | — | root |
| train | unauth-rce | python | `supervisor-cve-2017-11610` | `supervisor/CVE-2017-11610` | — | root |
| train | upload-webshell | php | `elfinder-cve-2021-32682` | `elfinder/CVE-2021-32682` | — | www-data |
| train | upload-webshell | java | `tomcat-cve-2017-12615` | `tomcat/CVE-2017-12615` | CVE-2017-12615 | root |
| held-out | arbitrary-file-read | java | `nexus-cve-2024-4956` | `nexus/CVE-2024-4956` | — | root |
| held-out | auth-bypass | java | `teamcity-cve-2023-42793` | `teamcity/CVE-2023-42793` | — | tcuser |
| held-out | cgi-rce | other | `bash-cve-2014-6271` | `bash/CVE-2014-6271` | — | www-data |
| held-out | code-injection | java | `h2database-cve-2018-10054` | `h2database/CVE-2018-10054` | — | root |
| held-out | command-injection | php | `cacti-cve-2022-46169` | `cacti/CVE-2022-46169` | CVE-2022-46169 | www-data |
| held-out | deserialization | php | `phpmyadmin-wooyun-2016-199433` | `phpmyadmin/WooYun-2016-199433` | — | www-data |
| held-out | deserialization | java | `shiro-cve-2016-4437` | `shiro/CVE-2016-4437` | CVE-2016-4437 | root |
| held-out | expression-injection | js | `n8n-cve-2025-68613` | `n8n/CVE-2025-68613` | — | root |
| held-out | file-inclusion | php | `phpmailer-cve-2017-5223` | `phpmailer/CVE-2017-5223` | — | www-data |
| held-out | ognl | java | `confluence-cve-2022-26134` | `confluence/CVE-2022-26134` | CVE-2022-26134 | confluence |
| held-out | ssti | java | `solr-cve-2019-17558` | `solr/CVE-2019-17558` | CVE-2019-17558 | root |
| held-out | unauth-rce | python | `scrapyd-unacc-rce` | `scrapy/scrapyd-unacc` | — | root |
| held-out | upload-webshell | java | `activemq-cve-2016-3088` | `activemq/CVE-2016-3088` | CVE-2016-3088 | root |
