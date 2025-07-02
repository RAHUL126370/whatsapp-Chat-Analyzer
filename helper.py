from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter
from textblob import TextBlob
import seaborn as sns
import matplotlib.pyplot as plt

def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    num_msgs = df.shape[0]
    # Filter string messages first into a new Series
    messages = df['message']
    string_messages = messages[messages.apply(lambda x: isinstance(x, str))]
    num_words = df['message'].apply(lambda x: len(x.split())).sum()
    media_msgs = df[df['message'] == "<Media omitted>"].shape[0]
    links = string_messages.str.contains('http', na=False).sum()
    return num_msgs, num_words, media_msgs, links

def most_active_users(df):
    x = df['user'].value_counts().head()
    return x, round((df['user'].value_counts(normalize=True)*100), 2).reset_index().rename(columns={'index': 'user', 'user': 'percent'})

def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    return wc.generate(" ".join(df[df['message'] != '<Media omitted>']['message']))

def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    emojis = []
    for msg in df['message']:
        emojis += [c for c in msg if c in emoji.EMOJI_DATA]
    return pd.DataFrame(Counter(emojis).most_common(), columns=['emoji', 'count'])

def sentiment_analysis(df):
    df['polarity'] = df['message'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['sentiment'] = df['polarity'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))
    return df

def daily_timeline(df):
    daily = df.groupby(df['datetime'].dt.date).count()['message'].reset_index()
    daily.columns = ['Date', 'Messages']
    return daily

def weekly_activity_map(df):
    return df['datetime'].dt.day_name().value_counts()

def monthly_timeline(df):
    timeline = df.groupby([df['datetime'].dt.month_name(), df['datetime'].dt.year]).count()['message'].reset_index()
    timeline['Month-Year'] = timeline['datetime'].astype(str) + "-" + timeline['user'].astype(str)
    return timeline
