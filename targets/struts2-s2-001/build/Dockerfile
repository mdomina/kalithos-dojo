# Base PINNATA a digest (Vulhub tomcat 8.5). Struts2 S2-001 = OGNL injection nel form di login.
FROM vulhub/tomcat@sha256:9b0989a0ac483d2ce309427123b44d21fddcad48159960064b5c6695270ef2ac

RUN set -ex \
    && rm -rf /usr/local/tomcat/webapps/* \
    && chmod a+x /usr/local/tomcat/bin/*.sh

COPY S2-001.war /usr/local/tomcat/webapps/ROOT.war
EXPOSE 8080
