from ftw.publisher.monitor.interfaces import IMonitorConfigurationSchema
from ftw.publisher.monitor.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from zope.component import getUtility
from plone.registry.interfaces import IRegistry


class TestConfig(FunctionalTestCase):

    def setUp(self):
        super(TestConfig, self).setUp()
        self.portal_url = self.portal.portal_url()
        self.config_url = '%s/@@publisher-monitor-config' % self.portal_url
        self.publisher_config_url = '%s/@@publisher-config' % self.portal_url

        registry = getUtility(IRegistry)
        self.config = registry.forInterface(IMonitorConfigurationSchema)

        self.grant('Manager')

    @browsing
    def test_link_is_in_controlpanel(self, browser):
        browser.login().open(self.publisher_config_url)
        link = browser.find_link_by_text('Monitor configuration')
        self.assertIsNotNone(
            link, 'Monitor configuration not found in publisher control panel')

        link.click()
        self.assertEqual(browser.url, self.config_url)

    @browsing
    def test_change_configuration(self, browser):
        browser.login().open(self.config_url)
        browser.fill({
            'Notification enabled': True,
            'Receivers': 'my@test.local\nfoo@bar.com',
            'Queue size threshold': '75',
            'Maximum extraction duration (seconds)': '777',
        }).submit()

        self.assertEqual(browser.url, self.config_url)

        self.assertTrue(self.config.enabled)
        self.assertEqual(self.config.receivers, ['my@test.local', 'foo@bar.com'])
        self.assertEqual(self.config.threshold, 75)
        self.assertEqual(self.config.max_extraction_duration_seconds, 777)

    @browsing
    def test_receiver_mail_validation(self, browser):
        browser.login().open(self.config_url)
        browser.fill({
            'Notification enabled': True,
            'Receivers': 'not an email',
        }).submit()

        self.assertEqual(browser.url, self.config_url)
        self.assertIn('At least one of the defined addresses are not valid.',
                      browser.contents)

        self.assertEqual(self.config.receivers, [])

    @browsing
    def test_cancel_form_redirects_to_publisher_config(self, browser):
        browser.login().open(self.config_url)
        browser.find_button_by_label('Cancel').click()
        self.assertEqual(browser.url, self.publisher_config_url)
