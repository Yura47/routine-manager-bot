import random
import os
import json
import requests
from datetime import date


def pick_today_activity(context):
	job = context.job
	activities = job.context["user_data"]["activities"]

	quote = json.loads(requests.get("https://zenquotes.io/api/random").content)[0]

	context.bot.send_message(chat_id= job.context["chat_id"], text= f"Today's Quote: {os.linesep}{quote['q']}{os.linesep}{quote['a']}")
	if len(activities) != 0:
		picked_activity = list(activities)[random.randrange(len(activities))]
		activities[picked_activity].append(date.today())
		context.bot.send_message(chat_id= job.context["chat_id"], text= f"Today's Activity: {picked_activity}")
	else:
		context.bot.send_message(chat_id= job.context["chat_id"], text= f"Your Activities List Is Empty{os.linesep}Can't Pick Activity For You😢")