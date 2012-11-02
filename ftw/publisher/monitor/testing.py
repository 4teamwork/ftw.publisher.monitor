from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig


class MonitorLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ftw.publisher.monitor
        xmlconfig.file('configure.zcml',
                       ftw.publisher.monitor,
                       context=configurationContext)


MONITOR_FIXTURE = MonitorLayer()
MONITOR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MONITOR_FIXTURE, ),
    name="ftw.publisher.monitor:Integration")
MONITOR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MONITOR_FIXTURE, ),
    name="ftw.publisher.monitor:Functional")
