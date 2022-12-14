import matplotlib.pyplot as plt 
import seaborn as sns
import streamlit as st
import preprocessor
import helper
# print("Hi")
st.sidebar.title("Whatsapp Chat Analyser")
uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.process(data)
    st.dataframe(df)
    user_list=df['User'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user=st.sidebar.selectbox("Show analysis with respect to",user_list)


    if st.sidebar.button("Analyse"):
        num_of_messages,words,media,links=helper.stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_of_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media Files")
            st.title(media)
        with col4:
            st.header("Total Links")
            st.title(links)
        if selected_user=='Overall':
            st.title('Most Busy Users')
            data,temp_df=helper.most_user(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)
            with col1:
                ax.bar(data.index,data.values,color='#8B2323')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(temp_df)
        st.title('Word Cloud')
        df_woc=helper.cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_woc)
        st.pyplot(fig)

        common_df=helper.commonwords(selected_user, df)
        fig,ax=plt.subplots()
        plt.xticks(rotation='vertical')
        ax.bar(common_df[0],common_df[1],color='#8B2323')
        st.title('Common Words')
        st.pyplot(fig)


        em_df=helper.find_emoji(selected_user,df)
        st.title("Emoji Count")
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(em_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(em_df[1].head(7),labels=em_df[0].head(7),autopct="%0.2f")
            st.pyplot(fig)


        st.title("Timeline by Month")
        tl=helper.month_timeline(selected_user, df)
        fig,ax=plt.subplots()
        ax.plot(tl['Time'],tl['Message'],color='#8B2323')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Timeline by Date")
        dtl=helper.date_timeline(selected_user, df)
        fig,ax=plt.subplots()
        ax.plot(dtl['Date_time'],dtl['Message'],color='#8B2323')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Activity by Week and Month")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most busy day")
            busy=helper.most_active_week(selected_user, df)
            fig,ax=plt.subplots()
            ax.bar(busy.index,busy.values,color='#8B2323')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most busy Month")
            busy=helper.most_active_month(selected_user, df)
            fig,ax=plt.subplots()
            ax.bar(busy.index,busy.values,color='#8B2323')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Activity Map")
        hm=helper.heatmap(selected_user, df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(hm)
        st.pyplot(fig)
        