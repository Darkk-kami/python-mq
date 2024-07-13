from flask import Flask, render_template, request, send_file
from celery import Celery
from tasks import send_mail_task, talk_to_me_task


def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers['X-Forwarded-For'].split(',')[0]
    else:
        ip = request.remote_addr
    return ip


app = Flask(__name__)
celery = Celery('app',
                broker='amqp://localhost',
                backend='rpc://')


@app.route('/')
def index():
    app.logger.info("Accessing Site")
    return render_template('index.html')


@app.route('/messaging', methods=['GET'])
def messaging():
    sendmail_param = request.args.get('sendmail')
    talktome_param = request.args.get('talktome')

    if sendmail_param:
        app.logger.info("Sending Email")
        work = send_mail_task.delay(sendmail_param)
        app.logger.info(work.backend)
        return f'Sending email to {sendmail_param}'

    if talktome_param:
        client_ip = get_client_ip()
        work = talk_to_me_task.delay(client_ip)
        app.logger.info(work.backend)
        return f'Logging current access time from IP - {client_ip}'
    return 'No valid parameters provided'


@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        with open('var/logs/messaging_system.logs', 'r') as log_file:
            log_content = log_file.read()
            return log_content

    except FileNotFoundError:
        return 'Logs not found', 404



if __name__ == '__main__':
    app.run(debug=True)





