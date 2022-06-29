import pytz
from datetime import date, time
from job_related_functions import update_picker_schedule


def update_picker_time(update, context):
	new_picker_time = time.fromisoformat(update.message.text)
	activities = context.user_data["activities"]
	context.user_data["picker time"] = new_picker_time
	for activity in activities:
		if date.today() in activities[activity]:
			activities[activity].remove(date.today())
			update.message.reply_text(f"Today's {activity} log entry will be nullified")

	update_picker_schedule(context, update.message.chat_id)

	update.message.reply_text(f"New Picker Alerting Time: {new_picker_time.isoformat('minutes')}")


def add_to_activities_list(update, context):
	if update.message.text in context.user_data["activities"]:
		update.message.reply_text(f""""{update.message.text}" Already In The List""")
		return

	context.user_data["activities"][update.message.text] = []
	update.message.reply_text("New Activity Added")