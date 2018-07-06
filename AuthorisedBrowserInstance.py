from robobrowser import RoboBrowser
import pdfkit

class AuthorisedBrowserInstance:
    def __init__(self, login_url, login_form_id):
        self.session = RoboBrowser()
        self.login_url = login_url
        self.login_form_id = login_form_id
        self.verify = False

    def login(self, username, password):
        self.session.open(self.login_url, verify=self.verify)
        login_form = self.session.get_form(id=self.login_form_id)
        login_form["user[email]"] = username
        login_form["user[password]"] = password
        self.session.submit_form(login_form)

    def export_pdf(self, url, output_file):
        self.session.open(url)
        pdfkit.from_string(str(self.session.parsed), output_file)
