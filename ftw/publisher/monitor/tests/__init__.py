from ftw.publisher.monitor.testing import MONITOR_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest import TestCase
from ftw.testing import MockTestCase as FTWMockTestCase
import transaction


class FunctionalTestCase(TestCase):
    layer = MONITOR_FUNCTIONAL_TESTING

    def setUp(self):
        super(FunctionalTestCase, self).setUp()
        self.portal = self.layer['portal']

    def grant(self, *roles):
        setRoles(self.portal, TEST_USER_ID, list(roles))
        transaction.commit()


class MockTestCase(FTWMockTestCase):
    layer = MONITOR_FUNCTIONAL_TESTING

    def setUp(self):
        super(MockTestCase, self).setUp()
        self.portal = self.layer['portal']

    def grant(self, *roles):
        setRoles(self.portal, TEST_USER_ID, list(roles))
        transaction.commit()
