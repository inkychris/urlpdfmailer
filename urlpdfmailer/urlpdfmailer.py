from robobrowser import RoboBrowser
import pdfkit


class UrlPdfMailer:
    def __init__(self, login_url, login_form_id, username_field_id='username', password_field_id='password'):
        self.session = RoboBrowser(parser='html.parser')
        self.login_url = login_url
        self.login_form_id = login_form_id
        self.username_field_id = username_field_id
        self.password_field_id = password_field_id
        self.pages_to_export = {}
        self.verify = False
        self.mailer = None

    @property
    def output_files(self):
        return self.pages_to_export.keys()

    def login(self, username, password):
        self.session.open(self.login_url, verify=self.verify)
        login_form = self.session.get_form(id=self.login_form_id)
        login_form[self.username_field_id] = username
        login_form[self.password_field_id] = password
        self.session.submit_form(login_form)

    def export_pdf(self, url, output_file):
        self.session.open(url)
        pdfkit.from_string(str(self.session.parsed), output_file, options={'quiet':''})

    def export_all(self):
        for output_file, url in self.pages_to_export.items():
            self.export_pdf(url, "{}.pdf".format(output_file))

    def update_mailer_attachments(self):
        self.mailer.add_attachments(["{}.pdf".format(i) for i in self.output_files])
