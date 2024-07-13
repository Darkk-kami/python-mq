from celery import Celery, shared_task
from celery.utils.log import get_task_logger
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import dotenv
import logging
import datetime


dotenv.load_dotenv()
print(f"EMAIL_ADDRESS: {os.getenv('SENDER_EMAIL')}")
print(f"EMAIL_PASSWORD: {os.getenv('EMAIL_PASSWORD')}")

logger = get_task_logger(__name__)

log_file_path = r'var/logs/messaging_system.logs'
file_handler = logging.FileHandler(log_file_path)  # Adjust path as necessary
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(file_handler)
else:
    logger.handlers.clear()
    logger.addHandler(file_handler)

app = Celery('app',
             broker='amqp://localhost',
             backend='rpc://')


def time():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d at %H:%M:%S')
    return current_time


@shared_task()
def send_mail_task(email):
    logger.setLevel(logging.INFO)
    print(f'Sending email to {email}')
    logger.info(f'Got Request - Starting work::email\n')
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('EMAIL_PASSWORD')

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = 'Testing'

    body = 'Hi'
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
        server.quit()
        logger.info('Work::email Finished\n')
        return f'Email sent successfully to {email}'
    except smtplib.SMTPException as e:
        logger.info(f'work::email failed\n')
        print(f'Failed to send email to {email}: {str(e)}')
        return f'Failed to send email to {email}: {str(e)}'


@shared_task()
def talk_to_me_task(client_ip):
    logger.info(f'Got Request - Starting work::talktome\n')
    log_entry = f"{time()} - IP: {client_ip}"
    with open('var/logs/messaging_system.logs', 'a') as log_file:
        log_file.write(log_entry)
        logger.info('Work::talktome Finished\n')
