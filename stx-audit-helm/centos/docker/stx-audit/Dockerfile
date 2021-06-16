ARG BASE
FROM ${BASE} AS stx
RUN yum -y update
RUN yum -y install\
           audit

ENTRYPOINT ["/sbin/auditd", "-f", "-l"]
