import  os
import calendar
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from chart_generators import *
from job_related_functions import update_picker_schedule


def show_chart(update, context):
	query = update.callback_query
	args = query.data.split()[1: ]

	if args[0] == "pie":
		query.message.reply_text("Pie Chart")
		query.message.reply_photo(get_pie_chart(context))
	elif args[0] == "bar":
		query.message.reply_text("Bar Chart")
		query.message.reply_photo(get_bar_chart(context))

	query.message.edit_reply_markup()

def check_uncheck_picker_day(update, context):
	query = update.callback_query
	day = int(query.data.split()[2])

	markup = query.message.reply_markup
	if markup["inline_keyboard"][day // 2][day % 2].text.startswith("✅"):
		markup["inline_keyboard"][day // 2][day % 2].text = markup["inline_keyboard"][day // 2][day % 2].text[1:]
	else:
		markup["inline_keyboard"][day // 2][day % 2].text = "✅" + markup["inline_keyboard"][day // 2][day % 2].text
	query.edit_message_reply_markup(markup)


def submit_picker_days(update, context):
	query = update.callback_query
	markup = query.message.reply_markup

	context.user_data["picker days"] = tuple(day for day in range(7) if markup["inline_keyboard"][day // 2][day % 2].text.startswith("✅"))

	if len(context.user_data["picker days"]) == 0:
		query.message.reply_text("Picker Is Turned Off")
		query.answer("Picker Is Turned Off")
	else:
		query.message.reply_text(f"New Picker Working Days:{os.linesep}{os.linesep.join(calendar.day_name[day] for day in context.user_data['picker days'])}")
		query.answer("Activity Picker Working Days Updated")

	update_picker_schedule(context, query.message.chat_id)
	query.message.delete()


def remove_activity_from_activities_list(update, context):
	query = update.callback_query
	activity = " ".join(query.data.split()[1:])
	del context.user_data["activities"][activity]

	query.message.reply_text(f"""Activity "{activity}" Removed""")
	query.message.delete()

def show_activities_pack(update, context):
	query = update.callback_query

	activities = list(context.user_data["activities"])

	pack_count = int(query.data.split()[3])
	buttons = []

	if len(activities) >= (pack_count + 1) * 3:
		for i in range(pack_count * 3, pack_count * 3 + 3):
			buttons.append([InlineKeyboardButton(activities[i], callback_data= f"remove {activities[i]}")])
		if pack_count > 0:
			buttons.append(
				[
					InlineKeyboardButton("☚", callback_data= f"remove show pack {pack_count - 1}"),
					InlineKeyboardButton("☛", callback_data= f"remove show pack {pack_count + 1}")
				]
				)
		else:
			buttons.append([InlineKeyboardButton("☛", callback_data= f"remove show pack {pack_count + 1}")])
	else:
		for i in range(pack_count * 3, len(activities)):
			buttons.append([InlineKeyboardButton(activities[i], callback_data= f"remove {activities[i]}")])
		if pack_count > 0:
			buttons.append([InlineKeyboardButton("☚", callback_data= f"remove show pack {pack_count - 1}")])

	markup = InlineKeyboardMarkup(buttons)
	query.message.edit_reply_markup(markup)