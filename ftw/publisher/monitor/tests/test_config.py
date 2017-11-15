from ftw.publisher.monitor.interfaces import IMonitorConfigurationSchema
from ftw.publisher.monitor.testing import MONITOR_FUNCTIONAL_TESTING
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser
from unittest2 import TestCase
import os.path


class TestConfig(TestCase):

    layer = MONITOR_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestConfig, self).setUp()
        self.portal = self.layer['portal']
        self.app = self.layer['app']

        self.browser = Browser(self.app)
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
        self.browser.handleErrors = False
        self.portal_url = self.portal.portal_url()

        self.config_url = os.path.join(self.portal_url,
                                       '@@publisher-monitor-config')

    def test_link_is_in_controlpanel(self):
        self.browser.open('%s/@@publisher-config' % self.portal_url)

        link = self.browser.getLink('Monitor configuration')
        self.assertNotEqual(
            link, None,
            'Monitor configuration not found in control panel')

        link.click()
        self.assertEqual(self.browser.url, self.config_url,
                         'Monitor configuration link points to wrong URL')

    def test_default_configuration(self):
        self.browser.open(self.config_url)
        config = IMonitorConfigurationSchema(self.portal)

        self.assertFalse(config.enabled)
        self.assertFalse(self.browser.getControl(name='form.enabled').value)

        self.assertEqual(config.get_receivers(), [])
        self.assertEqual(
            self.browser.getControl(name='form.receivers').value,
            '')

        self.assertEqual(config.get_threshold(), 100)
        self.assertEqual(
            self.browser.getControl(name='form.threshold').value,
            '100')

    def test_save_with_defaults(self):
        self.browser.open(self.config_url)
        self.assertEqual(
            self.browser.getControl(name='form.receivers').value, '')
        self.browser.getControl('Save').click()
        self.assertEqual(
            self.browser.getControl(name='form.receivers').value, '')
        self.assertNotIn('There were errors', self.browser.contents)

    def test_change_configuration(self):
        self.browser.open(self.config_url)
        self.browser.getControl(name='form.enabled').value = True
        self.browser.getControl(name='form.receivers').value = '\n'.join((
                'my@test.local',
                'foo@bar.com'))
        self.browser.getControl(name='form.threshold').value = '75'
        self.browser.getControl(name='form.max_extraction_duration_seconds').value = '777'

        self.browser.getControl('Save').click()
        self.assertEqual(self.browser.url, self.config_url)
        self.assertIn('Updated on', self.browser.contents)

        config = IMonitorConfigurationSchema(self.portal)
        self.assertTrue(config.enabled)
        self.assertEqual(config.get_receivers(), [
                'my@test.local', 'foo@bar.com'])
        self.assertEqual(config.threshold, 75)
        self.assertEqual(config.max_extraction_duration_seconds, 777)

    def test_receiver_mail_validation(self):
        self.assertEqual(
            IMonitorConfigurationSchema(self.portal).get_receivers(), [])

        self.browser.open(self.config_url)
        self.browser.getControl(name='form.receivers').value = 'not an email'
        self.browser.getControl('Save').click()

        self.assertEqual(self.browser.url, self.config_url)
        self.assertNotIn('Updated on', self.browser.contents)
        self.assertIn('At least one of the defined addresses are not valid.',
                      self.browser.contents)

        self.assertEqual(
            IMonitorConfigurationSchema(self.portal).get_receivers(), [])

    def test_cancel_form_redirects_to_publisher_config(self):
        self.browser.open(self.config_url)
        self.assertEqual(self.browser.url, self.config_url)

        self.browser.getControl('Cancel').click()
        self.assertEqual(self.browser.url,
                         '%s/@@publisher-config' % self.portal_url)
