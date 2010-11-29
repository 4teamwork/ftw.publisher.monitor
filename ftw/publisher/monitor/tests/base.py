from Products.PloneTestCase import ptc
from ftw.publisher.mailreport.testing import mailreport_functional_layer


class MailreportBasicTestCase(ptc.FunctionalTestCase):
    """Base class for integration tests."""

    layer = mailreport_functional_layer
