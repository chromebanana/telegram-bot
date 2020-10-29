import os

BASE_TELEGRAM_URL = 'https://api.telegram.org/bot{}'.format(
    os.environ.get('BOT_TOKEN'))
LOCAL_WEBHOOK_ENDPOINT = '{}/webhook'.format(os.environ.get('NGROK_URL'))
TELEGRAM_INIT_WEBHOOK_URL = '{}/setWebhook?url={}'.format(
    BASE_TELEGRAM_URL, LOCAL_WEBHOOK_ENDPOINT)
TELEGRAM_SEND_MESSAGE_URL = BASE_TELEGRAM_URL + '/sendMessage?chat_id={}&text={}'
ETHERSCAN_URL = 'https://api.etherscan.io/api?module=stats&action=ethsupply&apikey={}'.format(
    os.environ.get('ETHERSCAN_TOKEN'))
