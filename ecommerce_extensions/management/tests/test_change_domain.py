"""This module include a class that checks the commands.

Classes:
    ChangeDomainTestCase: Test command change_domain.py.
"""
from urllib.parse import urlparse

from django.contrib.sites.models import Site
from django.core.management import call_command
from django.test import TestCase
from mock import Mock, patch


class ChangeDomainTestCase(TestCase):
    """ This class checks the command change_domain.py"""

    def setUp(self):
        """This method creates a Site object in database."""
        self.site = Site.objects.create(
            domain="ecommerce.test.prod.edunext.co:8000",
            name="ecommerce.test.prod.edunext.co",
        )
        self.site.siteconfiguration = self._get_fake_site_configuration(self.site.domain)

    def test_domain_can_change(self):
        """Subdomain has been changed by the command

        Expected behavior:
            - siteconfiguration save method is called.
            - siteconfiguration lms_url_root is the expected value.
            - siteconfiguration oauth_settings is the expected value.
            - Site domain has been updated.
        """
        sites = [self.site]
        expected_domain = "http://ecommerce-test-prod-edunext-co-stage.edunext.co:8000"

        with patch.object(Site, "objects") as site_objects_mock:
            site_objects_mock.all.return_value = sites
            call_command('change_domain')

            siteconfiguration = site_objects_mock.all()[0].siteconfiguration
            siteconfiguration.save.assert_called_once()
            self.assertEqual(expected_domain, siteconfiguration.lms_url_root)
            self.assertEqual(expected_domain, siteconfiguration.oauth_settings["SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT"])

        self.assertEqual(urlparse(expected_domain).netloc, Site.objects.get(id=self.site.id).domain)

    def test_domain_with_same_suffix(self):
        """Subdomain is the same when the domain ends with the suffix.

        Expected behavior:
            - siteconfiguration lms_url_root is the expected value.
            - siteconfiguration oauth_settings is the expected value.
            - Site domain has not been changed.
        """
        sites = [self.site]
        expected_domain = "http://ecommerce.test.prod.edunext.co:8000"

        with patch.object(Site, "objects") as site_objects_mock:
            site_objects_mock.all.return_value = sites
            call_command(
                "change_domain",
                suffix_domain="ecommerce.test.prod.edunext.co",
                suffix_lms_domain="ecommerce.test.prod.edunext.co"
            )

            siteconfiguration = site_objects_mock.all()[0].siteconfiguration
            self.assertEqual(expected_domain, siteconfiguration.lms_url_root)
            self.assertEqual(expected_domain, siteconfiguration.oauth_settings["SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT"])

        self.assertEqual(urlparse(expected_domain).netloc, Site.objects.get(id=self.site.id).domain)

    def test_suffix_starts_with_period(self):
        """Suffix starts with a period.

        Expected behavior:
            - siteconfiguration lms_url_root is the expected value.
            - siteconfiguration oauth_settings is the expected value.
            - Site domain has not been changed.
        """
        sites = [self.site]
        expected_domain = "http://ecommerce-test-prod-edunext-co.suffix.com:8000"

        with patch.object(Site, "objects") as site_objects_mock:
            site_objects_mock.all.return_value = sites
            call_command(
                "change_domain",
                suffix_domain=".suffix.com",
                suffix_lms_domain=".suffix.com"
            )

            siteconfiguration = site_objects_mock.all()[0].siteconfiguration
            self.assertEqual(expected_domain, siteconfiguration.lms_url_root)
            self.assertEqual(expected_domain, siteconfiguration.oauth_settings["SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT"])

        self.assertEqual(urlparse(expected_domain).netloc, Site.objects.get(id=self.site.id).domain)

    def _get_fake_site_configuration(self, domain):
        """Return a siteconfiguration mock since this models is not available in test environments."""
        siteconfiguration = Mock()
        siteconfiguration.lms_url_root = "http://{}".format(domain)
        siteconfiguration.oauth_settings = {
            "SOCIAL_AUTH_EDX_OAUTH2_KEY": "ashdsgafghsdfgsdahfjk",
            "SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT": "http://{}".format(domain),
            "BACKEND_SERVICE_EDX_OAUTH2_KEY": "asdasdasdgerg",
            "SOCIAL_AUTH_EDX_OAUTH2_SECRET": "erwtewrter",
            "BACKEND_SERVICE_EDX_OAUTH2_SECRET": "ewrtewrtwe",
            "SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL": "http://{}/logout".format(domain),
            "SOCIAL_AUTH_EDX_OAUTH2_ISSUER": "http://{}".format(domain),
        }

        return siteconfiguration
