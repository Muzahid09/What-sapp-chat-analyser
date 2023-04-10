import re
import pandas as pd


def preprocess(data):
    pattern = "\D\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{1,2}:\d{1,2}\s\w{2}\D\s"

    msg = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)

    df = pd.DataFrame({'dates': dates, 'msg': msg})

    df['dates'] = df.dates.apply(lambda x: x[1:-2])

    # Converting to datetime format
    df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%y, %I:%M:%S %p')

    # Splitting user name and its msg
    users = []
    messages = []
    for message in df['msg']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['msg'], inplace=True)

    # Seperating all things from dates
    df['only_date'] = df['dates'].dt.date
    df['year'] = df['dates'].dt.year
    df['month_num'] = df['dates'].dt.month
    df['month'] = df['dates'].dt.month_name()
    df['day'] = df['dates'].dt.day
    df['day_name'] = df['dates'].dt.day_name()
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute




    return df
    # df.drop('dates',axis=1,inplace=True)
