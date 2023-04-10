from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # 1. no of msg
    num_of_msg = df.shape[0]

    # 2.no of words
    words = []
    for msg in df['message']:
        words.extend(msg.split())

    # 3. no of media files
    no_of_files = df[df.message.str.contains('omitted', regex=True, na=False)].shape[0]

    # 4. no of links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_of_msg, len(words), no_of_files, len(links)


def most_busy_user(df):
    x = df.user.value_counts().sort_values(ascending=False)
    df1 = round((df.user.value_counts().sort_values(ascending=False) / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'names', 'user': 'percent'})
    return x, df1


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def emoji_calc(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    df2 = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return df2


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index().sort_values(
        ['year', 'month_num'], ascending=[True, True])

    time = []
    for i in range(timeline.shape[0]):
        time.append(str(timeline.year[i]) + '-' + timeline.month[i])
    timeline['time'] = time

    return timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.day_name.value_counts().sort_values()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.month.value_counts().sort_values()