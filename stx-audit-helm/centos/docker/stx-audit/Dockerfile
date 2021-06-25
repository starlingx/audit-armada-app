ARG BASE
FROM ${BASE} AS stx
RUN yum -y update
RUN yum -y install\
           audit

COPY startAuditd.sh .
RUN chmod 755 startAuditd.sh
ENTRYPOINT ["./startAuditd.sh"]