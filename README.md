# Flask + Celery + Rabbit MQ Deployment Guide

This guide assumes you are running locally on windows and provides step-by-step instructions to deploy the Messaging Queue System application using Flask, Celery, and RabbitMQ.

## Prerequisites
Before you begin, ensure you have the following installed and set up:

### **Python**: version 3.11 or higher
Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

### Install requirements
```bash
pip install -r requirements.txt
```

### **RabbitMQ**: message broker
```bash
choco install rabbitmq
rabbitmq-plugins enable rabbitmq_management
Start-Service rabbitmq-server
```
- The second command enables the RabbitMQ management plugin, which provides a web-based UI to manage RabbitMQ.
- The third command starts the RabbitMQ service on your local machine.
- After starting the service, you can access the RabbitMQ Management Dashboard using your web browser: URL: http://localhost:15672/ Username: guest Password: guest


### **SMTP server: e.g., Gmail for sending emails (optional)

## Deployment
### Start the Flask Web Server: The application will run at http://localhost:5000 by default.
```bash
flask run
```
### Start Celery Worker:
Open a new Command Prompt, activate the virtual environment, and run:
```bash
celery -A tasks worker --loglevel=info -P gevent -n worker1@%h
```

## Usage
### Access and testing the endpoints:
By default
- ***To generate endpoint access time logs:*** http://localhost:5000/messaging?talktome=true
- ***To send a test email:*** http://localhost:5000/messaging?sendmail=example@mail.com



