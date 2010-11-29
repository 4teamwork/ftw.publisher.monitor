import unittest
import doctest
from Testing import ZopeTestCase as ztc
from base import MailreportBasicTestCase

OPTIONFLAGS = (doctest.NORMALIZE_WHITESPACE|
               doctest.ELLIPSIS|
               doctest.REPORT_NDIFF)


def test_suite():
    return unittest.TestSuite([
            # doctests in file bar.txt
            ztc.ZopeDocFileSuite(
                'config.txt', package='ftw.publisher.mailreport.tests',
                test_class=MailreportBasicTestCase, optionflags=OPTIONFLAGS),
            ztc.ZopeDocFileSuite(
                'utils.txt', package='ftw.publisher.mailreport.tests',
                test_class=MailreportBasicTestCase, optionflags=OPTIONFLAGS),
            ztc.ZopeDocFileSuite(
                'mailing.txt', package='ftw.publisher.mailreport.tests',
                test_class=MailreportBasicTestCase, optionflags=OPTIONFLAGS),
            ztc.ZopeDocFileSuite(
                'eventhandler.txt', package='ftw.publisher.mailreport.tests',
                test_class=MailreportBasicTestCase, optionflags=OPTIONFLAGS),
            ztc.ZopeDocTestSuite(
                'ftw.publisher.mailreport.browser.config',
                test_class=MailreportBasicTestCase, optionflags=OPTIONFLAGS),
            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
