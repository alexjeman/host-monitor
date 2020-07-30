from flask import request
import telegram
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from flask_restx import Resource
from apps.bot.models import BotLink, db
from apps.apikeys.models import ApiKey
from apps.bot.namespace import api
from apps.apikeys.security import get_owner
import os
import sys
from apps.bot.apihandler import APIHandler, APIHandlerNew
import requests
import logging
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
        print("got text message:", update.message, file=sys.stderr)



        if text == "/start":
            bot_message = f"Welcome to HostMonitor,\n" \
                f"I'm HostHunter_bot, and will interface you with our API! 🔥 🤘 \n" \
                f"/start - Channel intro.\n" \
                f"/register - Register with HostMonitor and receive a new API key.\n" \
                f"/myapikey - Get info about my apikey\n"

            bot.sendMessage(chat_id=chat_id, text=bot_message, reply_to_message_id=msg_id)

        if "/start " in text:
            parsed_key = text[text.index(" "):].strip()
            check_exists_apikey = bool(BotLink.query.filter_by(key=parsed_key).first())
            check_exists_chat_id = bool(BotLink.query.filter_by(chat_id=chat_id).first())
            if check_exists_apikey:
                bot.sendMessage(chat_id=chat_id, text="Someone already used this key! 👾\n", reply_to_message_id=msg_id)

            elif check_exists_chat_id:
                existing_key = BotLink.query.filter_by(chat_id=chat_id).first()
                bot.sendMessage(chat_id=chat_id, text=f"Your already have a key registered! 💃 {existing_key.key} 💃 \n", reply_to_message_id=msg_id)
            else:
                link_existing = BotLink(
                    key=parsed_key,
                    chat_id=chat_id
                )
                db.session.add(link_existing)
                db.session.commit()
                bot_message = f"API key {parsed_key}\n"
                bot.sendMessage(chat_id=chat_id, text=bot_message, reply_to_message_id=msg_id)

        elif text == "/register":

            new_api = APIHandlerNew(chat_id=chat_id)
            bot_message_pre = f"Requesting new API ✈ ⏰...\n"
            bot.sendMessage(chat_id=chat_id, text=bot_message_pre, reply_to_message_id=msg_id)

            new_api_request = new_api.get_newkey()
            if f"{new_api_request.status_code}" == "200":
                bot_message_success = f"Your new personal API key is : {new_api_request.json()['apikey']}\n"
                bot.sendMessage(chat_id=chat_id, text=bot_message_success, reply_to_message_id=msg_id)
                new_botlink = BotLink(
                    key=new_api_request.json()['apikey'],
                    chat_id=chat_id
                )
                db.session.add(new_botlink)
                db.session.commit()
                print("linked", chat_id, new_api_request.json()['apikey'])

            elif f"{new_api_request.status_code}" == "409":
                bot.sendMessage(chat_id=chat_id, text=f"You are already registered, try some get requests! 🔔\n", reply_to_message_id=msg_id)

        elif text == "/myapikey":
            new_api = APIHandler(obj=BotLink, chat_id=chat_id)
            api_request = new_api.get_apikey_info()
            host_list = api_request.json()['hosts']
            bot_message = f"Chat ID linked: {api_request.json()['email']}\n" \
                          f"Total hosts added: {len(host_list)}\n" \
                          f"{[['Host id: ' + str(hos['id']) + chr(10) + str('Name: ') + str(hos['name'] + chr(10) + str('URL: ') + str(hos['url'])  + chr(10))][0]for hos in host_list][0]}" \
                if len(host_list) > 0 \
                else f"Add some hosts to watch! 👽\n"
            bot.sendMessage(chat_id=chat_id, text=bot_message, reply_to_message_id=msg_id)
        else:
            print()


@api.route("/setwebhook", methods=['GET'], doc=False)
class BotResource(Resource):
    @api.doc("webhook")
    def get(self):
        s = bot.setWebhook('{URL}'.format(URL=BOT_URL))
        if s:
            return 'webhook set'
        else:
            return 'webhook failed'

