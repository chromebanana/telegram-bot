import logging
import os
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ.get('BOT_TOKEN')
APP_NAME = os.environ.get('HEROKU_APP_NAME')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Hi! Use /add_bin_reminder')


def alarm(context):
    job = context.job
    context.bot.send_message(
        job.context, text='Has anybody taken the bins out?')


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_reminder(update, context):
    chat_id = update.message.chat_id
    due = datetime.time(18, 0, 0)
    days = [1]  # only weds for now
    dow = ["Monday", "Tuesday", "Wednesday",
           "Thursday", "Friday", "Saturday", "Sunday"]
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_daily(
        alarm, due, days, context=chat_id, name=str(chat_id))

    text = 'Bin reminder successfully set for' dow[days[0]] + due.strftime("%X")
    if job_removed:
        text += '. Old one was removed.'
    update.message.reply_text(text)


def unset(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Bin reminder successfully cancelled!' if job_removed else 'You have no active reminder!'
    update.message.reply_text(text)


def main():
    updater = Updater((TOKEN), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("add_bin_reminder", set_reminder))
    dp.add_handler(CommandHandler("remove_bin_reminder", unset))
    dp.add_handler(CommandHandler("echo", echo))
    dp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://' + APP_NAME + '.herokuapp.com/' + TOKEN)

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
