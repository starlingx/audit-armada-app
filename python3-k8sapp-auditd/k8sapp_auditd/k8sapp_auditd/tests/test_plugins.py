#
# Copyright (c) 2021 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from k8sapp_auditd.common import constants as app_constants

from sysinv.tests.db import base as dbbase


class K8SAppAuditdAppMixin(object):
    app_name = app_constants.HELM_APP_AUDITD
    path_name = app_name + '.tgz'

    def setUp(self):
        super(K8SAppAuditdAppMixin, self).setUp()

    # Dummy test. Zuul fails without it.
    def test_audit(self):
        pass


# Test Configuration:
# - Controller
# - IPv6
# - Ceph Storage
# - auditd app
class K8SAppAuditdControllerTestCase(K8SAppAuditdAppMixin,
                                     dbbase.BaseIPv6Mixin,
                                     dbbase.BaseCephStorageBackendMixin,
                                     dbbase.ControllerHostTestCase):
    pass


# Test Configuration:
# - AIO
# - IPv4
# - Ceph Storage
# - auditd app
class K8SAppAuditdAIOTestCase(K8SAppAuditdAppMixin,
                              dbbase.BaseCephStorageBackendMixin,
                              dbbase.AIOSimplexHostTestCase):
    pass
