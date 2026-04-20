#
# Copyright (c) 2026 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
"""
Comprehensive unit tests for k8sapp_auditd
to achieve 85% coverage.
"""

import sys
import types
import unittest

import yaml

# Mock sysinv modules before importing k8sapp_auditd.helm.auditd
_mock_modules = {}
for module_name in [
    'sysinv', 'sysinv.common', 'sysinv.common.exception',
    'sysinv.helm', 'sysinv.helm.base',
    'sysinv.db', 'sysinv.db.api',
    'sysinv.tests', 'sysinv.tests.db',
    'sysinv.tests.db.utils',
    'sysinv.tests.db.base',
    'sysinv.tests.helm',
    'sysinv.tests.helm.base',
]:
    if module_name not in sys.modules:
        _mock_modules[module_name] = (
            types.ModuleType(module_name)
        )
        sys.modules[module_name] = (
            _mock_modules[module_name]
        )


class _InvalidHelmNamespace(Exception):
    """Mock exception for InvalidHelmNamespace."""
    def __init__(self, **kwargs):
        super().__init__(str(kwargs))


sys.modules[
    'sysinv.common.exception'
].InvalidHelmNamespace = _InvalidHelmNamespace


class _BaseHelm(object):
    """Mock BaseHelm class."""
    SUPPORTED_NAMESPACES = ['kube-system']

    def __init__(self, operator):
        pass


sys.modules['sysinv.helm.base'].BaseHelm = _BaseHelm

# Now import the modules under test
from k8sapp_auditd.common import constants  # noqa: E402
from k8sapp_auditd.helm import quoted_str  # noqa: E402
from k8sapp_auditd.helm.auditd import AuditdHelm  # noqa: E402


class TestConstants(unittest.TestCase):
    """Tests for k8sapp_auditd.common.constants."""

    def test_helm_app_auditd_value(self):
        """Verify HELM_APP_AUDITD constant."""
        self.assertEqual(
            constants.HELM_APP_AUDITD, 'auditd'
        )

    def test_helm_ns_auditd_value(self):
        """Verify HELM_NS_AUDITD constant."""
        self.assertEqual(
            constants.HELM_NS_AUDITD, 'kube-system'
        )

    def test_helm_chart_auditd_value(self):
        """Verify HELM_CHART_AUDITD constant."""
        self.assertEqual(
            constants.HELM_CHART_AUDITD, 'auditd'
        )

    def test_constants_attributes_exist(self):
        """Verify all expected constants exist."""
        self.assertTrue(
            hasattr(constants, 'HELM_APP_AUDITD')
        )
        self.assertTrue(
            hasattr(constants, 'HELM_NS_AUDITD')
        )
        self.assertTrue(
            hasattr(constants, 'HELM_CHART_AUDITD')
        )


class TestHelmInit(unittest.TestCase):
    """Tests for k8sapp_auditd.helm.__init__ module."""

    def test_quoted_str_is_str_subclass(self):
        """Verify quoted_str is a subclass of str."""
        self.assertTrue(issubclass(quoted_str, str))

    def test_quoted_str_instance(self):
        """Verify quoted_str instance behaves as str."""
        quoted_value = quoted_str('1.0')
        self.assertEqual(quoted_value, '1.0')
        self.assertIsInstance(quoted_value, str)

    def test_quoted_presenter_produces_single_quotes(self):
        """Verify quoted_presenter outputs single-quoted
        YAML.
        """
        yaml_data = {'version': quoted_str('1.0')}
        yaml_output = yaml.dump(
            yaml_data, default_flow_style=False
        )
        self.assertIn("'1.0'", yaml_output)

    def test_quoted_str_empty(self):
        """Verify quoted_str handles empty string."""
        self.assertEqual(quoted_str(''), '')

    def test_quoted_str_numeric_like(self):
        """Verify numeric-like strings are quoted."""
        yaml_data = {'port': quoted_str('8080')}
        yaml_output = yaml.dump(
            yaml_data, default_flow_style=False
        )
        self.assertIn("'8080'", yaml_output)

    def test_quoted_presenter_registered(self):
        """Verify representer is registered."""
        self.assertIn(
            quoted_str,
            yaml.Dumper.yaml_representers
        )

    def test_yaml_dump_multiple_quoted(self):
        """Verify multiple quoted_str values in YAML."""
        yaml_data = {
            'version': quoted_str('2.0'),
            'port': quoted_str('443'),
        }
        yaml_output = yaml.dump(
            yaml_data, default_flow_style=False
        )
        self.assertIn("'2.0'", yaml_output)
        self.assertIn("'443'", yaml_output)

    def test_quoted_str_preserves_methods(self):
        """Verify quoted_str supports str methods."""
        quoted_value = quoted_str('hello')
        self.assertEqual(quoted_value.upper(), 'HELLO')
        self.assertTrue(
            quoted_value.startswith('hel')
        )


class TestAuditdHelm(unittest.TestCase):
    """Tests for AuditdHelm class."""

    def _make_instance(self):
        """Create AuditdHelm without __init__.

        Returns:
            AuditdHelm instance created via __new__.
        """
        return AuditdHelm.__new__(AuditdHelm)

    def test_chart_attribute(self):
        """Verify CHART class attribute."""
        self.assertEqual(AuditdHelm.CHART, 'auditd')

    def test_service_name_attribute(self):
        """Verify SERVICE_NAME class attribute."""
        self.assertEqual(
            AuditdHelm.SERVICE_NAME, 'auditd'
        )

    def test_supported_namespaces_contains_auditd_ns(self):
        """Verify SUPPORTED_NAMESPACES has
        kube-system.
        """
        self.assertIn(
            'kube-system',
            AuditdHelm.SUPPORTED_NAMESPACES
        )

    def test_supported_app_namespaces_key(self):
        """Verify SUPPORTED_APP_NAMESPACES has
        auditd key.
        """
        self.assertIn(
            'auditd',
            AuditdHelm.SUPPORTED_APP_NAMESPACES
        )

    def test_supported_app_namespaces_value(self):
        """Verify auditd app namespace has
        kube-system.
        """
        self.assertIn(
            'kube-system',
            AuditdHelm.SUPPORTED_APP_NAMESPACES[
                'auditd'
            ]
        )

    def test_get_namespaces(self):
        """Verify get_namespaces returns
        SUPPORTED_NAMESPACES.
        """
        helm_instance = self._make_instance()
        self.assertEqual(
            helm_instance.get_namespaces(),
            AuditdHelm.SUPPORTED_NAMESPACES
        )

    def test_get_overrides_valid_namespace(self):
        """Verify get_overrides with valid namespace."""
        helm_instance = self._make_instance()
        result = helm_instance.get_overrides(
            namespace='kube-system'
        )
        self.assertEqual(result, {})

    def test_get_overrides_no_namespace(self):
        """Verify get_overrides with no namespace
        returns all overrides.
        """
        helm_instance = self._make_instance()
        result = helm_instance.get_overrides(
            namespace=None
        )
        self.assertIn('kube-system', result)

    def test_get_overrides_invalid_namespace(self):
        """Verify get_overrides raises for invalid
        namespace.
        """
        helm_instance = self._make_instance()
        self.assertRaises(
            _InvalidHelmNamespace,
            helm_instance.get_overrides,
            namespace='invalid-ns'
        )

    def test_get_overrides_empty_string_namespace(self):
        """Verify get_overrides with empty string."""
        helm_instance = self._make_instance()
        result = helm_instance.get_overrides(
            namespace=''
        )
        self.assertIsInstance(result, dict)

    def test_get_overrides_default_returns_dict(self):
        """Verify get_overrides returns dict."""
        helm_instance = self._make_instance()
        result = helm_instance.get_overrides()
        self.assertIsInstance(result, dict)

    def test_class_hierarchy(self):
        """Verify AuditdHelm inherits BaseHelm."""
        self.assertTrue(
            issubclass(AuditdHelm, _BaseHelm)
        )

    def test_chart_matches_constant(self):
        """Verify CHART matches constant value."""
        self.assertEqual(
            AuditdHelm.CHART,
            constants.HELM_CHART_AUDITD
        )

    def test_service_name_matches_chart(self):
        """Verify SERVICE_NAME matches CHART."""
        self.assertEqual(
            AuditdHelm.SERVICE_NAME,
            AuditdHelm.CHART
        )


class TestPackageImports(unittest.TestCase):
    """Tests for package-level imports."""

    def test_k8sapp_auditd_package(self):
        """Verify top-level package imports."""
        import k8sapp_auditd  # noqa: F811
        self.assertIsNotNone(k8sapp_auditd)

    def test_common_package(self):
        """Verify common package imports."""
        import k8sapp_auditd.common  # noqa: F811
        self.assertIsNotNone(k8sapp_auditd.common)

    def test_helm_package(self):
        """Verify helm package imports."""
        import k8sapp_auditd.helm  # noqa: F811
        self.assertIsNotNone(k8sapp_auditd.helm)

    def test_auditd_module(self):
        """Verify auditd module imports."""
        from k8sapp_auditd.helm import auditd  # noqa: F811
        self.assertIsNotNone(auditd)


if __name__ == '__main__':
    unittest.main()
