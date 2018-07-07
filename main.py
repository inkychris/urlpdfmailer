import yaml, argparse, schedule, time, logging.config, os
from urlpdfmailer import UrlPdfMailer, Mailer

# Monkey-patching logging to scheduler
def schedule_logging_decorator(function):
    def logged_call(self):
        function(self)
        schedule.logger.info('Scheduled job %s', self)
    return logged_call

schedule.Job._schedule_next_run = schedule_logging_decorator(schedule.Job._schedule_next_run)

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

os.makedirs('log', exist_ok=True)
with open('logging_config.yml', 'r') as yaml_block:
    logging.config.dictConfig(yaml.safe_load(yaml_block))

logger = logging.getLogger(__name__)

def email_pdfs():
    logger.info("Loading config file")
    try:
        with open(args.config_file, "r") as content:
            logger.info("Parsing contents of config file")
            instances = from_yaml_block(content)
    except Exception:
        logger.exception("Failed to load config file")
        return

    logger.info("Processing instances in config file")
    for instance in instances:
        logger.info("Exporting pdfs from instance")
        try:
            instance.export_all()
        except Exception:
            logger.exception("Failed to export pages as pdfs")
            return

        logger.info("Adding exported pdfs to email message")
        try:
            instance.update_mailer_attachments()
        except Exception:
            logger.exception("Failed to add pdfs as attachments to message")
            return

        logger.info("Sending message")
        try:
            pass#instance.mailer.send_message()
        except Exception:
            logger.exception("Failed to send email")
            return
        logger.info("Task completed successfully!")

def recurring_job():
    logger.info("Starting scheduled task")
    email_pdfs()

if not args.weekday:
    logger.info("Starting one off task")
    email_pdfs()
    exit(0)

schedule.every().__getattribute__(args.weekday).at(args.time).do(recurring_job)
while True:
    schedule.run_pending()
    time.sleep(1)
