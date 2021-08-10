#
# Copyright (c) 2021 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
# All Rights Reserved.
#

""" System inventory Armada manifest operator."""

from k8sapp_auditd.common import constants as app_constants
from k8sapp_auditd.helm.auditd import AuditdHelm

from sysinv.helm import manifest_base as base


class AuditdArmadaManifestOperator(base.ArmadaManifestOperator):

    APP = app_constants.HELM_APP_AUDITD
    ARMADA_MANIFEST = 'armada-manifest'

    CHART_GROUP_AUDITD = 'auditd'
    CHART_GROUPS_LUT = {
        AuditdHelm.CHART: 'kube-system-auditd',
    }

    def platform_mode_manifest_updates(self, dbapi, mode):
        """ Update the application manifest based on the platform

      :param dbapi: DB api object
      :param mode: mode to control how to apply the application manifest
    """
