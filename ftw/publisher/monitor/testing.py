from Testing.ZopeTestCase import installPackage
from collective.testcaselayer.ptc import BasePTCLayer
from collective.testcaselayer.common import common_layer

class MailreportFunctionalLayer(BasePTCLayer):
    """Layer for functional tests."""

    def afterSetUp(self):
        
        # Load testing zcml (optional)
        from ftw.publisher.mailreport import tests
        self.loadZCML('testing.zcml', package=tests)

        # installPackage() is *only* necessary for packages outside
        # the Products.* namespace which are also declared as Zope 2 products,
        # using <five:registerPackage /> in ZCML.
        installPackage('ftw.publisher.mailreport')

        # Load GS profile
#         self.addProfile('ftw.publisher.mailreport:default')

    def beforeTearDown(self):
        pass

mailreport_functional_layer = MailreportFunctionalLayer(
    bases=[common_layer])
