#Routine Manager Bot

import re
import os
import pytz
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, Defaults
from command_handlers_callbacks import *
from callback_query_handlers_callbacks import *
from message_handlers_callbacks import *
from redis_persistence import RedisPersistence
from config import BOT_TOKEN, APP_PORT, DB_URL

def main():
    bot_persistence = RedisPersistence(url= DB_URL, store_bot_data= False, store_chat_data= False)
    updater = Updater(BOT_TOKEN, persistence= bot_persistence, defaults = Defaults(tzinfo= pytz.timezone("Europe/Kiev")))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("show_activities", show_activities))
    dispatcher.add_handler(CommandHandler("add_activity", add_activity))
    dispatcher.add_handler(CommandHandler("remove_activity", remove_activity))
    dispatcher.add_handler(CommandHandler("statistics", statistics))
    dispatcher.add_handler(CommandHandler("set_picker_days", set_activity_picker_days))
    dispatcher.add_handler(CommandHandler("set_picker_time", set_activity_picker_time))

    dispatcher.add_handler(CallbackQueryHandler(show_chart, pattern= r"chart(?: [a-zA-Z])+"))
    dispatcher.add_handler(CallbackQueryHandler(check_uncheck_picker_day, pattern= r"picker days [0-6]"))
    dispatcher.add_handler(CallbackQueryHandler(submit_picker_days, pattern= r"picker days submit"))
    dispatcher.add_handler(CallbackQueryHandler(show_activities_pack, pattern= r"remove show pack \d"))
    dispatcher.add_handler(CallbackQueryHandler(remove_activity_from_activities_list, pattern= r"remove .+"))


    dispatcher.add_handler(MessageHandler(Filters.text & Filters.reply & Filters.regex(r"(([0-1][0-9])|(2[0-3])):(([0-5][0-9]))"), update_picker_time))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.reply, add_to_activities_list))

    updater.start_webhook(
        listen= "0.0.0.0",
        port= int(os.environ.get("PORT", APP_PORT)),
        url_path= BOT_TOKEN,
        webhook_url= "https://routine-manager-bot.herokuapp.com/" + BOT_TOKEN
    )
    updater.idle()


if __name__ == "__main__":
    main()

