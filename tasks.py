from celery import Celery, shared_task
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
import os 
import dotenv  
import logging

# Define the log file location and logging configuration
log_file = 'var/logs/messaging_system.logs'
logging.basicConfig(filename=log_file, level=logging.INFO)

# Load environment variables from a .env file
dotenv.load_dotenv()

# Initialize Celery application
app = Celery('app',
             broker='amqp://localhost',
             backend='rpc://') 


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
    message['Subject'] = 'Testing'

    body = 'Hello from Dwayne'
    message.attach(MIMEText(body, 'plain'))

    try:
        logging.info(f"Connecting to SMTP server...")
        # Connect to the SMTP server using SSL
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password) 
        server.sendmail(sender_email, email, message.as_string())
        server.quit() 
      
        logging.info(f"Email sent successfully to {email}")
        return f'Email sent successfully to {email}'
      
    except smtplib.SMTPException as e:
        error = f'Failed to send email to {email}: {str(e)}'
        logging.error(error)
        return f'Failed to send email to {email}: {str(e)}'
