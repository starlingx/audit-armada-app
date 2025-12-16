ARG BASE
FROM ${BASE} AS stx

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && \
    apt-get -y install auditd python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install --no-cache-dir --upgrade \
        setuptools==78.1.1 \
        wheel==0.38.1

COPY startAuditd.sh .

RUN mkdir -p /etc/audit && \
    touch /etc/audit/audit.rules && \
    chmod 600 /etc/audit/audit.rules

RUN chmod 755 startAuditd.sh
ENTRYPOINT ["./startAuditd.sh"]
