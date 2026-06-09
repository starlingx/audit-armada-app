ARG BASE
FROM ${BASE} AS stx

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && \
    apt-get -y install --no-install-recommends auditd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY startAuditd.sh .

RUN mkdir -p /etc/audit && \
    touch /etc/audit/audit.rules && \
    chmod 600 /etc/audit/audit.rules

RUN chmod 755 startAuditd.sh
ENTRYPOINT ["./startAuditd.sh"]
