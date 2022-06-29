from job_handlers_callbacks import *

def update_picker_schedule(context, chat_id):
	picker_jobs = context.job_queue.get_jobs_by_name("activity picker job")
	for picker_job in picker_jobs:
		picker_job.schedule_removal()

	if len(context.user_data["picker days"]) == 0:
		return

	context.job_queue.run_daily(
        pick_today_activity,
        time= context.user_data["picker time"],
        days= context.user_data["picker days"],
        context= {"user_data": context.user_data, "chat_id": chat_id},
        name= "activity picker job"
    )