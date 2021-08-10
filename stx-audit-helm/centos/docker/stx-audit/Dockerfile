ARG BASE
FROM ${BASE} AS stx
RUN yum -y update
RUN yum -y install\
           audit

COPY startAuditd.sh .

RUN mkdir -p /etc/audit
RUN touch /etc/audit/audit.rules
RUN chmod 600 /etc/audit/audit.rules

RUN chmod 755 startAuditd.sh
ENTRYPOINT ["./startAuditd.sh"]