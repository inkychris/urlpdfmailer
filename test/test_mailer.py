from urlpdfmailer import Mailer
from unittest import TestCase

host = "host.address.com"
port = "123"
sender = "sender@address.com"
password = "password"


class TestMailer(TestCase):
    def setUp(self):
        self.mailer = Mailer(host, port, sender, password)

    def tearDown(self):
        del self.mailer

    def test_to_recipients_string(self):
        self.mailer.to_recipients = "to@email.com"
        self.assertListEqual(["to@email.com"], self.mailer.to_recipients)

    def test_to_recipients_list(self):
        self.mailer.to_recipients = ["to@email1.com", "to@email2.com"]
        self.assertListEqual(["to@email1.com", "to@email2.com"], self.mailer.to_recipients)

    def test_cc_recipients_string(self):
        self.mailer.cc_recipients = "to@email.com"
        self.assertListEqual(["to@email.com"], self.mailer.cc_recipients)

    def test_cc_recipients_list(self):
        self.mailer.cc_recipients = ["to@email1.com", "to@email2.com"]
        self.assertListEqual(["to@email1.com", "to@email2.com"], self.mailer.cc_recipients)

    def test_bcc_recipients_string(self):
        self.mailer.bcc_recipients = "to@email.com"
        self.assertListEqual(["to@email.com"], self.mailer.bcc_recipients)

    def test_bcc_recipients_list(self):
        self.mailer.bcc_recipients = ["to@email1.com", "to@email2.com"]
        self.assertListEqual(["to@email1.com", "to@email2.com"], self.mailer.bcc_recipients)

    def test_all_recipients(self):
        self.mailer.to_recipients = ['to@email1.com']
        self.mailer.cc_recipients = ['to@email2.com', 'to@email3.com']
        self.mailer.bcc_recipients = ['to@email4.com']
        self.assertEqual(['to@email1.com', 'to@email2.com', 'to@email3.com', 'to@email4.com'], self.mailer.all_recipients)
