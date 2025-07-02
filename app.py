import streamlit as st
import preprocess, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")

st.title("📱 WhatsApp Chat Analyzer")

uploaded_file = st.file_uploader("Upload exported WhatsApp chat (.txt)", type="txt")

if uploaded_file is not None:
    bytes_data = uploaded_file.read()
    data = bytes_data.decode('utf-8')
    df = preprocess.preprocess(data)

    user_list = df['user'].unique().tolist()
    if 'system' in user_list: user_list.remove('system')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.selectbox("Choose user to analyze", user_list)

    if st.button("Show Analysis"):

        # Stats
        num_msgs, num_words, media_msgs, links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Messages", num_msgs)
        col2.metric("Total Words", num_words)
        col3.metric("Media Shared", media_msgs)
        col4.metric("Links Shared", links)

        # Timeline
        st.markdown("### 📅 Daily Timeline")
        timeline = helper.daily_timeline(df)
        fig, ax = plt.subplots()
        ax.plot(timeline['Date'], timeline['Messages'], color='green')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Weekly Activity
        st.markdown("### 📊 Weekly Activity")
        busy_day = helper.weekly_activity_map(df)
        fig, ax = plt.subplots()
        ax.bar(busy_day.index, busy_day.values, color='skyblue')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # WordCloud
        st.markdown("### ☁️ WordCloud")
        wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc)
        st.pyplot(fig)

        # Emoji
        st.markdown("### 😊 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df.head(10))
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['count'].head(5), labels=emoji_df['emoji'].head(5), autopct="%0.2f")
            st.pyplot(fig)

        # Sentiment
        st.markdown("### 🧠 Sentiment Analysis")
        sentiment_df = helper.sentiment_analysis(df)
        fig, ax = plt.subplots()
        sns.countplot(data=sentiment_df, x='sentiment', palette='Set2', ax=ax)
        st.pyplot(fig)

        # Active Users
        if selected_user == "Overall":
            st.markdown("### 🧑‍🤝‍🧑 Most Active Users")
            x, new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()
            ax.bar(x.index, x.values, color='orange')
            st.pyplot(fig)
            st.dataframe(new_df)
