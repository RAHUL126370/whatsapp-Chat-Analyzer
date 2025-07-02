import re
import pandas as pd

def preprocess(data):
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2})\s(AM|PM)\s-\s'
    messages = re.split(pattern, data)[1:]
    dates, times, ampm, users, msgs = [], [], [], [], []

    for i in range(0, len(messages), 4):
        date = messages[i]
        time = messages[i+1]
        am_pm = messages[i+2]
        content = messages[i+3]

        try:
            user, msg = content.split(': ', 1)
        except:
            user = 'system'
            msg = content

        dates.append(date)
        times.append(time)
        ampm.append(am_pm)
        users.append(user)
        msgs.append(msg)

    df = pd.DataFrame({'date': dates, 'time': times, 'ampm': ampm,
                       'user': users, 'message': msgs})
    df['datetime'] = pd.to_datetime(
        df['date'].astype(str) + ' ' + df['time'].astype(str) + ' ' + df['ampm'].astype(str),
        format='%d/%m/%Y %I:%M %p', errors='coerce')
    df.drop(columns=['date', 'time', 'ampm'], inplace=True)
    return df
