# Import necessary modules
from celery import Celery, shared_task  # Celery is an asynchronous task queue/job queue
import smtplib  # SMTP protocol client to send email
from email.mime.multipart import MIMEMultipart  # To create a multipart email message
from email.mime.text import MIMEText  # To attach text content to the email
import os  # To access environment variables
import dotenv  # To load environment variables from a .env file
import datetime  # To handle date and time operations
import logging  # To log messages

# Define the log file location and logging configuration
log_file = 'var/logs/messaging_system.logs'
logging.basicConfig(filename=log_file, level=logging.INFO)

# Load environment variables from a .env file
dotenv.load_dotenv()

# Initialize Celery application
app = Celery('app',
             broker='amqp://localhost',  # Message broker URL (RabbitMQ in this case)
             backend='rpc://')  # Result backend URL (RPC in this case)

# Function to get the current time formatted as a string
def time():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return current_time

# Define a Celery shared task for sending emails
@shared_task()
def send_mail_task(email):
    print(f'Sending email to {email}')
    logging.info(f"Attempting to send email to {email}")

    # Retrieve sender email and password from environment variables
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('EMAIL_PASSWORD')

    # Create a multipart email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = 'Testing'  # Subject of the email

    # Email body
    body = 'Hello from Dwayne'
    message.attach(MIMEText(body, 'plain'))

    try:
        logging.info(f"Connecting to SMTP server...")
        # Connect to the SMTP server using SSL
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)  # Login to the SMTP server
        server.sendmail(sender_email, email, message.as_string())  # Send the email
        server.quit()  # Terminate the SMTP session
        logging.info(f"Email sent successfully to {email}")
        return f'Email sent successfully to {email}'
    except smtplib.SMTPException as e:
        error = f'Failed to send email to {email}: {str(e)}'
        logging.error(error)
        return f'Failed to send email to {email}: {str(e)}'

# Define a Celery shared task for logging the current time
@shared_task()
def talk_to_me_task():
    log_entry = f"{time()}"  # Get the current time
    logging.info(f"Hello request at {log_entry}")

