import streamlit as st
import matplotlib.pyplot as plt

import preprocessor, helper

st.sidebar.title("Whatsapp Chat Analyzer for iphones")

uploaded_file = st.sidebar.file_uploader("Upload your exported chat file without media")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    # user_list.remove(+918004006400)
    # user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        # Stats Area
        # num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        num_messages, total_words, total_files, total_links = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_messages)

        with col2:
            st.header('Total Words')
            st.title(total_words)

        with col3:
            st.header('Total Files')
            st.title(total_files)

        with col4:
            st.header('Total links')
            st.title(total_links)

        # Timeline
        st.title('Timeline')
        dft = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(dft.time, dft.message)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity map
        st.title('Activity Map wrt Time')

        col1, col2 = st.columns(2)

        with col1:
            st.header('Most Busy Day')
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most Busy month')
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)



        if selected_user == 'Overall':
            st.title('Activity Map wrt User')
            x, df1 = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                st.header("Most busy users")
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(df1)

        # wordcloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # emoji analysis
        st.title("emoji analysis")

        df2 = helper.emoji_calc(selected_user, df)
        st.dataframe(df2)
