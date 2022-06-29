import os
import calendar
from datetime import date, time, timedelta
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from job_related_functions import *

def start(update, context):
    if len(context.user_data) == 0:
        context.user_data["activities"] = {}
        context.user_data["picker days"] = ()
        context.user_data["picker time"] = time(hour= 10)

    update_picker_schedule(context, update.message.chat_id)

    update.message.reply_text("WELCOME")

def show_activities(update, context):
    activities = context.user_data["activities"]
    if len(activities):
        update.message.reply_text(os.linesep.join([f"{i + 1}. {activity}" for i, activity in enumerate(activities.keys())]))
    else:
        update.message.reply_text("No Activities Found")

def statistics(update, context):
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Pie Chart", callback_data= "chart pie"),
                InlineKeyboardButton("Bar Chart", callback_data= "chart bar")
            ]
        ]
    )
    update.message.reply_text("Chart Type:", reply_markup= markup)

def add_activity(update, context):
    markup = ForceReply(input_field_placeholder= "New Activity")
    update.message.reply_text("Type In New Activity", reply_markup= markup)

def remove_activity(update, context):
    activities = list(context.user_data["activities"])

    if len(activities) == 0:
        update.message.reply_text("You Have No Activities Stored")
        return

    buttons = []

    if len(activities) > 3:
        for i in range(3):
            buttons.append([InlineKeyboardButton(activities[i], callback_data= f"remove {activities[i]}")])
        buttons.append([InlineKeyboardButton("☛", callback_data= f"remove show pack 1")])
    else:
        for i in range(len(activities)):
            buttons.append([InlineKeyboardButton(activities[i], callback_data= f"remove {activities[i]}")])
    
   
    markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text("Choose Activity To Remove:", reply_markup= markup)

def set_activity_picker_days(update, context):
    buttons = [[] for i in range(4)]
    for day in range(7):
        buttons[day // 2].append(InlineKeyboardButton(calendar.day_name[day], callback_data= f"picker days {day}"))
        if day in context.user_data["picker days"]:
            buttons[day // 2][day % 2].text = "✅" + buttons[day // 2][day % 2].text

    buttons.append([InlineKeyboardButton("Submit", callback_data= "picker days submit")])
    markup = InlineKeyboardMarkup(buttons)
    
    update.message.reply_text("Check Days When Activity Picker Works:", reply_markup= markup)

def set_activity_picker_time(update, context):
    markup = ForceReply(input_field_placeholder= "Current alert time: " + context.user_data["picker time"].isoformat("minutes"))
    update.message.reply_text("Type In Activity Picker Alerting Time:", reply_markup= markup)