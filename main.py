import yaml, argparse, schedule, time
from urlpdfmailer import UrlPdfMailer, Mailer

def valid_time(string):
    if ':' not in string:
        raise AttributeError('Time format requires ":" separator e.g: 12:30')
    time = string.split(':')
    hour = int(time[0])
    minute = int(time[1])
    if hour < 0 or hour > 23:
        raise AttributeError('Hour value out of range 0-23')
    if minute < 0 or minute > 59:
        raise AttributeError('Minute value out of range 0-59')
    return string

parser = argparse.ArgumentParser(description="Pull HTML from URLs and email them as PDF attachments to a schedule.")
parser.add_argument('config_file', type=str, help="URL/email configuration file.")
parser.add_argument('--weekly', dest='weekday', type=str, help="Specify weekly occurrence on specific day of week.")
parser.add_argument('--trigger_time', dest='time', type=valid_time, help="Trigger time for daily or weekly scheduling.")
args = parser.parse_args()

def from_yaml_block(yaml_block):
    instances = []
    settings = yaml.safe_load(yaml_block)

    for site in settings["sites"]:
        upm_instance = UrlPdfMailer(site["login_url"], site["login_form_id"], verify=site.get("verify", True),
                                    username_field_id=site["username_field_id"],
                                    password_field_id=site["password_field_id"])

        upm_instance.login(site["username"], site["password"])
        upm_instance.pages_to_export = site["pages_to_export"]

        upm_instance.mailer = Mailer(
            settings['ssl_email_settings']['host'],
            settings['ssl_email_settings']['port'],
            settings['ssl_email_settings']['email_address'],
            settings['ssl_email_settings']['password']
        )
        upm_instance.mailer.to_recipients = site['email'].get('to', '')
        upm_instance.mailer.cc_recipients = site['email'].get('cc', '')
        upm_instance.mailer.bcc_recipients = site['email'].get('bcc', '')
        upm_instance.mailer.subject = site['email'].get('subject')
        upm_instance.mailer.body = site['email'].get('body')

        instances.append(upm_instance)
    return instances

def email_pdfs():
    with open(args.config_file, "r") as content:
        instances = from_yaml_block(content)

    for instance in instances:
        instance.export_all()
        instance.update_mailer_attachments()
        #instance.mailer.send_message()

def recurring_job():
    email_pdfs()
    print("Next run scheduled:", schedule.next_run())

if not args.weekday:
    email_pdfs()
    exit(0)

schedule.every().__getattribute__(args.weekday).at(args.time).do(recurring_job)
print("First run scheduled:", schedule.next_run())
while True:
    schedule.run_pending()
    time.sleep(1)
