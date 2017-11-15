from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from ftw.publisher.monitor.handlers import invoke_notification
from ftw.publisher.monitor.interfaces import IMonitorConfigurationSchema
from ftw.publisher.monitor.interfaces import IMonitorNotifier
from ftw.publisher.monitor.testing import MONITOR_FUNCTIONAL_TESTING
from ftw.publisher.sender.interfaces import IConfig
from ftw.publisher.sender.interfaces import IQueue
from ftw.testing import MockTestCase
from mocker import ARGS, KWARGS, ANY
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from zope.component import getGlobalSiteManager
from zope.component import provideAdapter


class TestEventhandler(MockTestCase):

    layer = MONITOR_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestEventhandler, self).setUp()

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.folder = self.portal.get(self.portal.invokeFactory(
                'Folder', 'mailing-test', title='Mailing Test Folder'))
        self.queue = IQueue(self.portal)

        mtool = getToolByName(self.portal, 'portal_membership')
        self.user = mtool.getMemberById(TEST_USER_ID)

        self.config = IMonitorConfigurationSchema(self.portal)
        self.config.set_enabled(True)
        self.config.set_receivers_plain('hugo@boss.com')

        self.notifier_class = self.stub_interface(IMonitorNotifier)
        self.notifier = self.mock_interface(IMonitorNotifier)
        self.expect(self.notifier_class(self.portal)).result(
            self.notifier)

        provideAdapter(factory=self.notifier_class,
                       provides=IMonitorNotifier,
                       adapts=(IPloneSiteRoot,))

    def tearDown(self):
        sm = getGlobalSiteManager()
        sm.unregisterAdapter(factory=self.notifier_class,
                             provided=IMonitorNotifier,
                             required=(IPloneSiteRoot,))
        super(TestEventhandler, self).tearDown()

    def stub_current_queue_length(self, amount_of_jobs):
        while self.queue.countJobs() > 0:
            self.queue.popJob()

        for _i in range(amount_of_jobs):
            # Remove acquisition wrapper from "self.user" in order to
            # prevent the following error:
            #   TypeError: Can't pickle objects in acquisition wrappers.
            self.queue.createJob('push', self.folder, aq_base(self.user))

    def test_eventhandler_calls_notifier(self):
        self.config.set_threshold(2)
        self.stub_current_queue_length(3)
        event = self.create_dummy(queue=self.queue)

        self.expect(self.notifier(ANY, ANY, ANY))
        self.replay()

        invoke_notification(self.portal, event)

    def test_adapter_called_after_queue_execution(self):
        self.config.set_threshold(2)
        self.stub_current_queue_length(3)

        self.expect(self.notifier(ANY, ANY, ANY))
        self.replay()

        self.portal.unrestrictedTraverse('@@publisher.executeQueue')()

    def test_adapter_not_called_when_monitoring_disabled(self):
        self.config.set_threshold(2)
        self.stub_current_queue_length(3)

        self.config.set_enabled(False)

        self.expect(self.notifier(ANY, ANY, ANY)).count(0)
        self.replay()

        self.portal.unrestrictedTraverse('@@publisher.executeQueue')()

    def test_adapter_not_called_when_threshold_not_reached(self):
        self.config.set_threshold(10)
        self.stub_current_queue_length(1)

        self.expect(self.notifier(ARGS, KWARGS)).count(0)
        self.replay()

        self.portal.unrestrictedTraverse('@@publisher.executeQueue')()

    def test_adapter_is_called_even_when_publishing_disabled(self):
        self.config.set_threshold(2)
        self.stub_current_queue_length(3)

        config = IConfig(self.portal)
        config.set_publishing_enabled(False)

        self.expect(self.notifier(ARGS, KWARGS))
        self.replay()

        self.portal.unrestrictedTraverse('@@publisher.executeQueue')()
