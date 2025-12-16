#!/bin/bash

#
# Copyright (c) 2022 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

set -u

echo "Starting auditd …"

# update /etc/audit/audit.rules with any changes made to
# /etc/audit/rules.d/audit.rules
augenrules --load

# start auditd with no fork to run in the background in the container
/sbin/auditd -n -l
EXIT_STATUS=$?

if [ "$EXIT_STATUS" -ne "0" ]; then
        echo "Error code: $EXIT_STATUS"
        echo "Could not start auditd" >&2
fi

exit ${EXIT_STATUS}
