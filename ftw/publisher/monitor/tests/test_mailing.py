from Acquisition import aq_base
from ftw.publisher.monitor.interfaces import IMonitorConfigurationSchema
from ftw.publisher.monitor.testing import MONITOR_FUNCTIONAL_TESTING
from ftw.publisher.sender.interfaces import IQueue
from ftw.testbrowser import browsing
from ftw.testing import MockTestCase
from mocker import ARGS, KWARGS
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from Products.CMFCore.utils import getToolByName
from pyquery import PyQuery as pq
from time import time
import os
import re


class TestEmailNotification(MockTestCase):

    layer = MONITOR_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestEmailNotification, self).setUp()

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.folder = self.portal.get(self.portal.invokeFactory(
                'Folder', 'mailing-test', title='Mailing Test Folder'))
        self.queue = IQueue(self.portal)

        mtool = getToolByName(self.portal, 'portal_membership')
        self.user = mtool.getMemberById(TEST_USER_ID)

        # Enable notifier
        self.config = IMonitorConfigurationSchema(self.portal)
        self.config.set_enabled(True)
        self.config.set_receivers_plain('hugo@boss.com')

        # configure mail settings
        properties_tool = getToolByName(self.portal, 'portal_properties')
        properties_tool.email_from_name = 'Plone'
        properties_tool.email_from_address = 'test@plone.org'

        # patch MailHost
        self.mail_host = self.stub()
        self.mock_tool(self.mail_host, 'MailHost')
        self.mails = []
        self.expect(self.mail_host.send(ARGS, KWARGS)).call(
            lambda *args, **kwargs: self.mails.append((args, kwargs)))
        self.expect(self.mail_host.secureSend(ARGS, KWARGS)).call(
            lambda *args, **kwargs: self.mails.append((args, kwargs)))

        self.replay()

    def tearDown(self):
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        super(TestEmailNotification, self).tearDown()

    def stub_current_queue_length(self, amount_of_jobs):
        while self.queue.countJobs() > 0:
            self.queue.popJob()

        for _i in range(amount_of_jobs):
            # Remove acquisition wrapper from "self.user" in order to
            # prevent the following error:
            #   TypeError: Can't pickle objects in acquisition wrappers.
            self.queue.createJob('push', self.folder, aq_base(self.user))

    def get_table_from_message(self, message):
        message = pq(str(message))
        return message('table:first').html()

    def normalize_message(self, message):
        message = re.sub('\s{1,}', ' ', message)
        message = message.replace('> <', '><')
        return message

    @browsing
    def test_notification_sent_after_executing_queue_when_queue_too_large(self, browser):
        self.config.set_threshold(2)
        self.stub_current_queue_length(3)

        self.portal.restrictedTraverse('@@publisher.executeQueue')()

        self.assertEqual(len(self.mails), 1)
        args, kwargs = self.mails.pop()

        self.assertEqual(kwargs.get('mfrom'), 'test@plone.org')
        self.assertEqual(kwargs.get('mto'), 'hugo@boss.com')
        self.assertEqual(kwargs.get('subject'),
                         u'Publisher monitor warning: Plone site')

        browser.open_html(args[0].get_payload(decode=True))
        self.assertEqual(
            'The amount of jobs in the publisher queue of '
            'the senders host reached the threshold. '
            'The queue may be blocked!',
            browser.css('.reason').first.text)

        self.assertEqual(
            [['Jobs in the queue:', '3']],
            browser.css('table').first.lists())

    @browsing
    def test_notification_sent_when_extraction_takes_too_long(self, browser):
        self.config.set_max_extraction_duration_seconds(10)  # 10 seconds
        self.stub_current_queue_length(1)
        job = self.queue.getJobs()[0]
        one_minute_ago = time() - 60
        open(job.dataFile, 'w+').close()  # empty the file
        os.utime(job.dataFile, (one_minute_ago, one_minute_ago))  # set the mtime

        self.portal.restrictedTraverse('@@publisher.executeQueue')()

        self.assertEqual(len(self.mails), 1)
        args, kwargs = self.mails.pop()

        self.assertEqual(kwargs.get('mfrom'), 'test@plone.org')
        self.assertEqual(kwargs.get('mto'), 'hugo@boss.com')
        self.assertEqual(kwargs.get('subject'),
                         u'Publisher monitor warning: Plone site')

        browser.open_html(args[0].get_payload(decode=True))
        self.assertEqual(
            'Extraction of a publisher job failed for 60 seconds.'
            ' This will probably jam the queue.',
            browser.css('.reason').first.text)

        self.assertEqual(
            [['Jobs in the queue:', '1']],
            browser.css('table').first.lists())

    def test_notification_is_sent_to_each_receiver(self):
        self.config.set_receivers_plain('\n'.join((
                    'demo@user.com',
                    'hugo@boss.com')))
        self.config.set_threshold(2)
        self.stub_current_queue_length(3)

        self.portal.restrictedTraverse('@@publisher.executeQueue')()

        self.assertEqual(len(self.mails), 2)

        # we pop it reversed, therfore we test in opposite order than
        # it is configured.
        args, kwargs = self.mails.pop()
        self.assertEqual(kwargs.get('mto'), 'hugo@boss.com')

        args, kwargs = self.mails.pop()
        self.assertEqual(kwargs.get('mto'), 'demo@user.com')
