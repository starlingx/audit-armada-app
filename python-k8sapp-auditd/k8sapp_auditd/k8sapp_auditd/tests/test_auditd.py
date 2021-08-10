# Copyright (c) 2021 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from k8sapp_auditd.tests import test_plugins

from sysinv.db import api as dbapi
from sysinv.tests.db import utils as dbutils
from sysinv.tests.helm import base


class AuditdTestCase(test_plugins.K8SAppAuditdAppMixin,
                     base.HelmTestCaseMixin):

    def setUp(self):
        super(AuditdTestCase, self).setUp()
        self.app = dbutils.create_test_app(name='auditd')
        self.dbapi = dbapi.get_instance()
