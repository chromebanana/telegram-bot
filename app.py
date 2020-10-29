from celery import Celery
from flask import Flask, request, jsonify
from telegram_bot import TelegramBot
from config import TELEGRAM_INIT_WEBHOOK_URL
import logging


def make_celery(app):
    celery = Celery(
        app.name,
        backend=app.config['result_backend'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='amqp://',
    result_backend='rpc://'
)

celery = make_celery(app)
TelegramBot.init_webhook(TELEGRAM_INIT_WEBHOOK_URL)


@celery.task()
def add(a, b):
    return a + b


def printMsg():
    app.logger.warning('testing warning log')


@app.route('/webhook', methods=['POST'])
def index():
    req = request.get_json()
    bot = TelegramBot()
    bot.parse_webhook_data(req)
    success = bot.action()
    add.delay(4, 4)
    # TODO: Success should reflect the success of the reply
    return jsonify(success=success)


if __name__ == '__main__':
    app.run(port=5000)
