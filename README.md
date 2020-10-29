# telegram-bot
Telegram bot compatible with Python 3.6. Webhooks with ngrok to Telegram bot message stream, conditional responses. Celery for schedualed messages

adapted from https://github.com/jg-fisher/python-telegram-bot

## Instructions For Use:
Download ngrok into the project root directory: https://ngrok.com/download

Navigate the the root directory in terminal, run:

> ./ngrok http 5000

Add your telegram bot token to the TOKEN variable in .env

Add your ngrok https url to the NGROK_URL variable in .env

Configure conditional actions based on Telegram message text in telegram_bot.py TelegramBot.action class method

