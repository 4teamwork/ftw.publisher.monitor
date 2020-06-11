from ftw.publisher.monitor import utils
from unittest import TestCase


class TestEmailAddressValidator(TestCase):

    def test_valid_email(self):
        self.assertTrue(utils.email_addresses_validator(['hugo.boss@web.de']))

    def test_valid_multiline_emails(self):
        self.assertTrue(utils.email_addresses_validator(['hugo.boss@web.de',
                                                         'hugo@boss.com']))

    def test_number_emails(self):
        self.assertTrue(utils.email_addresses_validator(['1my@mail.ch']))
        self.assertTrue(utils.email_addresses_validator(['info@4teamwork.ch']))

    def test_special_emails(self):
        self.assertTrue(utils.email_addresses_validator([
            'my-very.special-mail@ver.y.spec.ial.do.main.com']))

    def test_local_addresses(self):
        self.assertTrue(utils.email_addresses_validator(['me@home.local']))
        self.assertFalse(utils.email_addresses_validator(['me@local']))

    def test_invalid_addresses(self):
        self.assertFalse(utils.email_addresses_validator(['invalid']))
        self.assertFalse(utils.email_addresses_validator(['hugo@boss.com',
                                                          'invalid',
                                                          'hugo@boss.com']))
