import re

from flask import request
import telegram
from flask_restx import Resource
from apps.bot.namespace import api
import os


# Telebot
from dotenv import load_dotenv
load_dotenv(verbose=True)
bot = telegram.Bot(os.getenv("BOT_TOKEN"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
BOT_URL = os.getenv("BOT_URL")


@api.route(f"/", methods=['POST'])
class BotResource(Resource):
    @api.doc("bot_root")
    def post(self):
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat_id
        msg_id = update.message.message_id
        text = update.message.text.encode('utf-8').decode()
        print("got text message:", text)

        if text == "/start":
            bot_welcome = """
            Welcome to HostHunter_bot, the bot is...
            """
            bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)


@api.route("setwebhook".format(BOT_TOKEN), methods=['GET', 'POST'])
class BotResource(Resource):
    @api.doc("webhook")
    def get(self):
        s = bot.setWebhook('{URL}{HOOK}'.format(URL=BOT_URL, HOOK=BOT_TOKEN))
        if s:
            return 'webhook ok'
        else:
            return 'webhook failed'

    @api.doc("webhook")
    def post(self):
        s = bot.setWebhook('{URL}{HOOK}'.format(URL=BOT_URL, HOOK=BOT_TOKEN))
        if s:
            return 'webhook ok'
        else:
            return 'webhook failed'

