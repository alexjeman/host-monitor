from flask import request
import telegram
from telegram.ext import Updater
from flask_restx import Resource
from apps.bot.namespace import api
import os
import requests

# Telegram bot
from dotenv import load_dotenv
load_dotenv(verbose=True)
bot = telegram.Bot(os.getenv("BOT_TOKEN"))
updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
BOT_URL = os.getenv("BOT_URL")


@api.route('/', methods=['POST'], doc=False)
class BotResource(Resource):
    @api.doc("bot_root")
    def post(self):
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat_id
        msg_id = update.message.message_id
        text = update.message.text.encode('utf-8').decode()
        print("got text message:", text)

        if text == "/start":
            bot_message = """
            Welcome to HostMonitor, 
            I'm HostHunter_bot, and will interface you with our API! 🔥 🤘
            /register - Register with HostMonitor and receive a new API key.
            """
            bot.sendMessage(chat_id=chat_id, text=bot_message, reply_to_message_id=msg_id)
        elif text == "/register":
            bot_message = "Hey"
            request
            bot.sendMessage(chat_id=chat_id, text=bot_message, reply_to_message_id=msg_id)


@api.route("/setwebhook", methods=['GET'], doc=False)
class BotResource(Resource):
    @api.doc("webhook")
    def get(self):
        s = bot.setWebhook('{URL}'.format(URL=BOT_URL))
        if s:
            return 'webhook set'
        else:
            return 'webhook failed'

