from ftw.builder.testing import BUILDER_LAYER
from ftw.testing import IS_PLONE_5
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from zope.configuration import xmlconfig


class MonitorLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ftw.publisher.monitor
        xmlconfig.file('configure.zcml',
                       ftw.publisher.monitor,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.publisher.monitor:default')

        if IS_PLONE_5:
            applyProfile(portal, 'plone.app.contenttypes:default')


MONITOR_FIXTURE = MonitorLayer()
MONITOR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MONITOR_FIXTURE, ),
    name="ftw.publisher.monitor:Integration")
MONITOR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MONITOR_FIXTURE, ),
    name="ftw.publisher.monitor:Functional")
