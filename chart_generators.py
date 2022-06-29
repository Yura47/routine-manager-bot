import io
from matplotlib import pyplot as plt

def get_pie_chart(context):
    activities = context.user_data["activities"]
    activities = {activity: activities[activity] for activity in activities if len(activities[activity]) != 0}

    plt.pie(
        [len(activity_records) for activity_records in activities.values()],
        labels= activities.keys(),
        autopct= lambda x: f"{round(x, 1)} %",
        shadow= True,
        radius= 1.25
    )

    buffer = io.BytesIO()
    plt.savefig(buffer, format= "png")
    plt.clf()
    return buffer.getvalue()


def get_bar_chart(context):
    activities = context.user_data["activities"]
    activities = {activity: activities[activity] for activity in activities if len(activities[activity]) != 0}
    
    plt.bar(
        activities.keys(),
        [len(activity_records) for activity_records in activities.values()],
    )

    buffer = io.BytesIO()
    plt.savefig(buffer, format= "png")
    plt.clf()
    return buffer.getvalue()