import re
import pandas as pd

def preprocess(data):
    pattern = '\[(\d{2}\/\d{2}\/\d{2}),\s(\d{2}:\d{2}:\d{2})\]\s(.+?):\s(.+)'

    messages = re.findall(pattern, data)
    dates = []
    users = []
    message_text = []
    for message in messages:
        dates.append(message[0] + ' ' + message[1])
        users.append(message[2])
        message_text.append(message[3])
    df = pd.DataFrame({'date': dates, 'user': users, 'message': message_text})
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y %H:%M:%S')

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
