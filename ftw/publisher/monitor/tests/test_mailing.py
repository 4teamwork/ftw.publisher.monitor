from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from ftw.builder import Builder
from ftw.builder import create
from ftw.publisher.monitor.interfaces import IMonitorConfigurationSchema
from ftw.publisher.monitor.tests import MockTestCase
from ftw.publisher.sender.interfaces import IQueue
from ftw.testbrowser import browsing
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from time import time
from zope.component import getUtility
import os


class TestEmailNotification(MockTestCase):

    def setUp(self):
        super(TestEmailNotification, self).setUp()
        self.grant('Manager')

        self.folder = create(Builder('folder'))
        self.queue = IQueue(self.portal)

        mtool = getToolByName(self.portal, 'portal_membership')
        self.user = mtool.getMemberById(TEST_USER_ID)

        # Enable notifier
        registry = getUtility(IRegistry)
        self.config = registry.forInterface(IMonitorConfigurationSchema)
        self.config.enabled = True
        self.config.receivers = [u'hugo@boss.com']

        # configure mail settings
        properties_tool = getToolByName(self.portal, 'portal_properties')
        properties_tool.email_from_name = 'Plone'
        properties_tool.email_from_address = 'test@plone.org'

        # patch MailHost
        self.mail_host = self.stub()
        self.mock_tool(self.mail_host, 'MailHost')
        self.mails = []
        self.mail_host.send = lambda *args, **kwargs: self.mails.append((args, kwargs))

    def stub_current_queue_length(self, amount_of_jobs):
        while self.queue.countJobs() > 0:
            self.queue.popJob()

        for _i in range(amount_of_jobs):
            # Remove acquisition wrapper from "self.user" in order to
            # prevent the following error:
            #   TypeError: Can't pickle objects in acquisition wrappers.
            self.queue.createJob('push', self.folder, aq_base(self.user))

    @browsing
    def test_notification_sent_after_executing_queue_when_queue_too_large(self, browser):
        self.config.threshold = 2
        self.stub_current_queue_length(3)

        self.portal.restrictedTraverse('@@publisher.executeQueue')()

        self.assertEqual(len(self.mails), 1)
        args, kwargs = self.mails.pop()

        self.assertEqual(kwargs.get('mfrom'), 'test@plone.org')
        self.assertEqual(kwargs.get('mto'), 'hugo@boss.com')
        self.assertEqual(kwargs.get('subject'), u'Publisher monitor warning: Plone site')

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
        self.config.max_extraction_duration_seconds = 10  # 10 seconds

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
        self.config.receivers = [u'demo@user.com', u'hugo@boss.com']
        self.config.threshold = 2
        self.stub_current_queue_length(3)

        self.portal.restrictedTraverse('@@publisher.executeQueue')()

        self.assertEqual(len(self.mails), 2)

        # we pop it reversed, therfore we test in opposite order than
        # it is configured.
        args, kwargs = self.mails.pop()
        self.assertEqual(kwargs.get('mto'), 'hugo@boss.com')

        args, kwargs = self.mails.pop()
        self.assertEqual(kwargs.get('mto'), 'demo@user.com')
