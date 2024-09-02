from flask import Flask, render_template, request, send_file 
from celery import Celery  
from tasks import send_mail_task 
import logging 
from datetime import datetime 

# Define the log file location and logging configuration
log_file = 'var/logs/messaging_system.logs'
logging.basicConfig(filename=log_file, level=logging.INFO)


# Function to get the client's IP address
def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers['X-Forwarded-For'].split(',')[0]
    else:
        ip = request.remote_addr
    return ip


# Initialize Flask application
app = Flask(__name__)

celery = Celery('app',
                broker='amqp://localhost',  # Message broker URL (RabbitMQ)
                backend='rpc://')  # Result backend URL (RPC)


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
        client_ip = request.remote_addr  # Get the IP address of the client
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current time
        logging.info(f"Hello request at {current_time}")
        return f"Logged Hello Request at {current_time} from {client_ip}"

    # If no valid parameters are provided, return a message
    return 'No valid parameters provided'


# Define a route to retrieve the log file
@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        with open(log_file, 'r') as file:
            log_content = file.read()
            return log_content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except FileNotFoundError:
        # Return a 404 error if the log file is not found
        return 'Logs not found', 404


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True) 


