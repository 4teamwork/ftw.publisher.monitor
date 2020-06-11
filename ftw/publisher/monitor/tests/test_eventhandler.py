from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from ftw.builder import Builder
from ftw.builder import create
from ftw.publisher.monitor.interfaces import IMonitorConfigurationSchema
from ftw.publisher.monitor.interfaces import IMonitorNotifier
from ftw.publisher.monitor.tests import FunctionalTestCase
from ftw.publisher.sender.interfaces import IConfig
from ftw.publisher.sender.interfaces import IQueue
from ftw.testing.mailing import Mailing
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import getGlobalSiteManager
from zope.component import getUtility
from zope.component import provideAdapter
import transaction


notifier_adapter_called = 0


class Notifier(object):
    def __init__(self, *a, **kw):
        pass

    def __call__(self, *a, **kw):
        global notifier_adapter_called
        notifier_adapter_called += 1


class TestEventhandler(FunctionalTestCase):

    def setUp(self):
        super(TestEventhandler, self).setUp()
        self.grant('Manager')

        self.folder = create(Builder('folder'))
        self.queue = IQueue(self.portal)

        mtool = getToolByName(self.portal, 'portal_membership')
        self.user = mtool.getMemberById(TEST_USER_ID)

        provideAdapter(factory=Notifier,
                       provides=IMonitorNotifier,
                       adapts=(IPloneSiteRoot,))

        # Enable notifier
        registry = getUtility(IRegistry)
        self.config = registry.forInterface(IMonitorConfigurationSchema)
        self.config.enabled = True
        self.config.receivers = [u'hugo@boss.com']

        # configure mail settings
        properties_tool = getToolByName(self.portal, 'portal_properties')
        properties_tool.email_from_name = 'Plone'
        properties_tool.email_from_address = 'test@plone.org'

        Mailing(self.layer['portal']).set_up()
        transaction.commit()

    def tearDown(self):
        global notifier_adapter_called
        notifier_adapter_called = 0

        sm = getGlobalSiteManager()
        sm.unregisterAdapter(factory=Notifier,
                             provided=IMonitorNotifier,
                             required=(IPloneSiteRoot,))

        super(TestEventhandler, self).tearDown()

        Mailing(self.layer['portal']).tear_down()

    def stub_current_queue_length(self, amount_of_jobs):
        while self.queue.countJobs() > 0:
            self.queue.popJob()

        for _i in range(amount_of_jobs):
            # Remove acquisition wrapper from "self.user" in order to
            # prevent the following error:
            #   TypeError: Can't pickle objects in acquisition wrappers.
            self.queue.createJob('push', self.folder, aq_base(self.user))

    def test_adapter_notifier_adapter_called_after_queue_execution(self):
        self.config.threshold = 2
        self.stub_current_queue_length(3)

        self.portal.unrestrictedTraverse('@@publisher.executeQueue')()
        self.assertEqual(notifier_adapter_called, 1)

    def test_adapter_not_notifier_adapter_called_when_monitoring_disabled(self):
        self.config.threshold = 2
        self.stub_current_queue_length(3)

        self.config.enabled = False

        self.portal.unrestrictedTraverse('@@publisher.executeQueue')()
        self.assertEqual(notifier_adapter_called, 0)

    def test_adapter_not_notifier_adapter_called_when_threshold_not_reached(self):
        self.config.threshold = 10
        self.stub_current_queue_length(1)

        self.portal.unrestrictedTraverse('@@publisher.executeQueue')()
        self.assertEqual(notifier_adapter_called, 0)

    def test_adapter_is_notifier_adapter_called_even_when_publishing_disabled(self):
        self.config.threshold = 2
        self.stub_current_queue_length(3)

        config = IConfig(self.portal)
        config.publishing_enabled = False

        self.portal.unrestrictedTraverse('@@publisher.executeQueue')()
        self.assertEqual(notifier_adapter_called, 1)
