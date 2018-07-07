from robobrowser import RoboBrowser
import logging
from weasyprint import HTML


class UrlPdfMailer:
    def __init__(self, login_url, login_form_id, username_field_id='username', password_field_id='password',
                 verify=True):
        self.session = RoboBrowser(parser='html.parser')
        self.login_url = login_url
        self.login_form_id = login_form_id
        self.username_field_id = username_field_id
        self.password_field_id = password_field_id
        self.pages_to_export = {}
        self.verify = verify
        self.mailer = None
        self.logger = logging.getLogger(__name__)

    @property
    def output_files(self):
        return self.pages_to_export.keys()

    def login(self, username, password):
        self.logger.debug("Logging in to site")
        self.logger.debug("Navigating to login page")
        self.session.open(self.login_url, verify=self.verify)
        self.logger.debug("Retrieving login form")
        login_form = self.session.get_form(id=self.login_form_id)
        login_form[self.username_field_id] = username
        login_form[self.password_field_id] = password
        self.logger.debug("Submitting login form")
        self.session.submit_form(login_form)

    def export_pdf(self, url, output_file):
        self.logger.debug("Downloading url as pdf")
        self.logger.debug("Navigating to page to export")
        self.session.open(url)
        self.logger.debug("Exporting html to pdf")
        weasy_html = HTML(string=str(self.session.parsed))
        weasy_html.write_pdf(output_file)

    def export_all(self):
        for output_file, url in self.pages_to_export.items():
            self.export_pdf(url, "{}.pdf".format(output_file))

    def update_mailer_attachments(self):
        self.logger.debug("Adding attachments to mailer")
        self.mailer.add_attachments(["{}.pdf".format(i) for i in self.output_files])
