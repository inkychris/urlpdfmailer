import smtplib, logging
import os.path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def string_or_list_to_list(string_or_list):
    if type(string_or_list) == list:
        return string_or_list
    elif type(string_or_list) == str:
        return [string_or_list]
    else:
        raise TypeError("Expected string or list.")


class Mailer:
    def __init__(self, host, port, sender, password):
        self._message = MIMEMultipart()
        self.host = host
        self.port = port
        self.sender = sender
        self.password = password
        self.subject = ""
        self.body = ""
        self.logger = logging.getLogger(__name__)

    @property
    def to_recipients(self):
        return self._to_recipients

    @to_recipients.setter
    def to_recipients(self, recipients):
        self._to_recipients = string_or_list_to_list(recipients)

    @property
    def cc_recipients(self):
        return self._cc_recipients

    @cc_recipients.setter
    def cc_recipients(self, recipients):
        self._cc_recipients = string_or_list_to_list(recipients)

    @property
    def bcc_recipients(self):
        return self._bcc_recipients

    @bcc_recipients.setter
    def bcc_recipients(self, recipients):
        self._bcc_recipients = string_or_list_to_list(recipients)

    @property
    def all_recipients(self):
        return self.to_recipients + self.cc_recipients + self.bcc_recipients

    def add_attachments(self, files):
        for file in files:
            attachment = MIMEBase('application', 'octet-stream')
            self.logger.debug("Opening output file '{}' to attach to message".format(file))
            with open(file, 'rb') as content:
                self.logger.debug("Setting attachment payload to attachment")
                attachment.set_payload(content.read())
                self.logger.debug("Encoding attachment")
                encoders.encode_base64(attachment)
                self.logger.debug("Added attachment header")
                attachment.add_header('Content-Disposition', 'attachment; filename={}'.format(os.path.basename(file)))
                self.logger.debug("Adding attachment to message")
                self._message.attach(attachment)

    def clear_message(self):
        self.to_recipients = None
        self.cc_recipients = None
        self.bcc_recipients = None
        self.subject = ""
        self.body = ""
        self._message = MIMEMultipart()

    def send_message(self):
        self.logger.debug("Added message headers")
        self._message['To'] = ','.join(self.to_recipients)
        self._message['CC'] = ','.join(self.cc_recipients)
        self._message['Subject'] = self.subject
        self._message.attach(MIMEText(self.body))

        self.logger.debug("Connecting to SMTP server with SSL: {}:{}".format(self.host, self.port))
        with smtplib.SMTP_SSL(self.host, self.port) as server:
            self.logger.debug("Logging in to SMTP server")
            server.login(self.sender, self.password)
            self.logger.debug("Sending message from SMTP server")
            server.sendmail(self.sender, self.all_recipients, self._message.as_string())
