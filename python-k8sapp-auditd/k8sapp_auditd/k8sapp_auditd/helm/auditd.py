#
# Copyright (c) 2021 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from sysinv.common import exception
from sysinv.helm import base

from k8sapp_auditd.common import constants as app_constants


class AuditdHelm(base.BaseHelm):
    """Class to encapsulate helm operations for the auditd chart"""

    SUPPORTED_NAMESPACES = base.BaseHelm.SUPPORTED_NAMESPACES + \
        [app_constants.HELM_NS_AUDITD]
    SUPPORTED_APP_NAMESPACES = {
        app_constants.HELM_APP_AUDITD:
            base.BaseHelm.SUPPORTED_NAMESPACES + [app_constants.HELM_NS_AUDITD],
    }

    CHART = app_constants.HELM_CHART_AUDITD

    SERVICE_NAME = app_constants.HELM_CHART_AUDITD

    def get_namespaces(self):
        return self.SUPPORTED_NAMESPACES

    def get_overrides(self, namespace=None):
        overrides = {
            app_constants.HELM_NS_AUDITD: {}
        }

        if namespace in self.SUPPORTED_NAMESPACES:
            return overrides[namespace]
        elif namespace:
            raise exception.InvalidHelmNamespace(chart=self.CHART,
                                                 namespace=namespace)
        else:
            return overrides
