# Flask + Celery + Rabbit MQ Deployment Guide

This guide assumes you are running locally on windows and provides step-by-step instructions to deploy the Messaging Queue System application using Flask, Celery, and RabbitMQ.

## Prerequisites
Before you begin, ensure you have the following installed and set up:

- **Python**: version 3.11 or higher
Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

pip install -r requirements.txt
```bash
pip install -r requirements.txt
```


- **RabbitMQ**: message broker
```bash
choco install rabbitmq
rabbitmq-plugins enable rabbitmq_management
Start-Service rabbitmq-server
```

- The second command enables the RabbitMQ management plugin, which provides a web-based UI to manage RabbitMQ.
- The third command starts the RabbitMQ service on your local machine.
- After starting the service, you can access the RabbitMQ Management Dashboard using your web browser: URL: http://localhost:15672/ Username: guest Password: guest
- **SMTP server: e.g., Gmail for sending emails (optional)
