# Import necessary modules
from flask import Flask, render_template, request, send_file  # Flask framework and relevant modules
from celery import Celery  # Celery for asynchronous task management
from tasks import send_mail_task, talk_to_me_task  # Import custom Celery tasks
import logging  # To log messages

# Define the log file location and logging configuration
log_file = 'var/logs/messaging_system.logs'
logging.basicConfig(filename=log_file, level=logging.INFO)


# Function to get the client's IP address
def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        # If the request passed through a proxy, use the first IP in the 'X-Forwarded-For' header
        ip = request.headers['X-Forwarded-For'].split(',')[0]
    else:
        # Otherwise, use the remote address
        ip = request.remote_addr
    return ip


# Initialize Flask application
app = Flask(__name__)

# Initialize Celery application
celery = Celery('app',
                broker='amqp://localhost',  # Message broker URL (RabbitMQ)
                backend='rpc://')  # Result backend URL (RPC)


# Define a route for the home page
@app.route('/')
def index():
    # Log access to the site with the client's IP address
    logging.info(f"Site Accessed - {get_client_ip()}")

    # Retrieve parameters from the URL query string
    sendmail_param = request.args.get('sendmail')
    talktome_param = request.args.get('talktome')

    # If the 'sendmail' parameter is present, send an email
    if sendmail_param:
        send_mail_task.delay(sendmail_param)  # Schedule the send_mail_task asynchronously
        return f'Sending email to {sendmail_param}'

    # If the 'talktome' parameter is present, log the current time
    if talktome_param:
        talk_to_me_task.delay()  # Schedule the talk_to_me_task asynchronously
        client_ip = request.remote_addr  # Get the IP address of the client
        return f'Logging current access time from IP - {client_ip}'

    # If no valid parameters are provided, return a message
    return 'No valid parameters provided'


# Define a route to retrieve the log file
@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        # Open and read the log file
        with open(log_file, 'r') as file:
            log_content = file.read()
            return log_content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except FileNotFoundError:
        # Return a 404 error if the log file is not found
        return 'Logs not found', 404


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode


