import pandas as pd
import seaborn as sns
import emoji
from collections import Counter
from wordcloud import WordCloud
from urlextract import URLExtract
extract=URLExtract()
def stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['User']==selected_user]
    num_of_messages=len(df)
    words=[]
    for m in df['Message']:
        words.extend(m.split())
    media=len(df[df['Message']=='<Media omitted>\n'])
    links=[]
    for m in df['Message']:
        links.extend(extract.find_urls(m))
    return num_of_messages,len(words),media,len(links)


def most_user(df):
    data=df['User'].value_counts().head()
    df=round((df['User'].value_counts()/len(df))*100,3).reset_index().rename(columns={'index':'Name','User':'Percent'})
    return data,df


def cloud(selected_user,df):

    if selected_user!='Overall':
        df=df[df['User']==selected_user]
    temp_df=df[df['User']!='group_notification']
    temp_df=temp_df[temp_df['Message']!='<Media omitted>\n']
    woc=WordCloud(width=350,height=350,min_font_size=10,background_color='white')
    temp_df['Message'].apply(remove_stopwords)
    df_woc=woc.generate(temp_df['Message'].str.cat(sep=" "))
    return df_woc


def remove_stopwords(Message):
    f=open('stopwords.txt','r')
    stopwords=f.read()
    li=[]
    for w in Message.lower().split():
        if w not in stopwords:
            li.append(w)
    return " ".join(li)




def commonwords(selected_user,df):
    f=open('stopwords.txt','r')
    stopwords=f.read()
    if selected_user!='Overall':
        df=df[df['User']==selected_user]
    temp_df=df[df['User']!='group_notification']
    temp_df=temp_df[temp_df['Message']!='<Media omitted>\n']
    word_list=[]
    for m in temp_df['Message']:
        for w in m.lower().split():
            if w not in stopwords:
                word_list.append(w)
    common_df=pd.DataFrame(Counter(word_list).most_common(15))
    return common_df



def find_emoji(selected_user,df):
    if selected_user!='Overall':
        df=df[df['User']==selected_user]
    em=[]
    for m in df['Message']:
        em.extend([c for c in m if c in emoji.UNICODE_EMOJI['en']])
    em_df=pd.DataFrame(Counter(em).most_common(10))
    return em_df 


def month_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['User']==selected_user]
    tl=df.groupby(['Year','Month Number','Month']).count()['Message'].reset_index()

    t=[]
    for i in range(tl.shape[0]):
        t.append(tl['Month'][i]+ "-" + str(tl['Year'][i]))

    tl['Time']=t
    return tl

def date_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['User']==selected_user]
    dtl=df.groupby('Date_time').count()['Message'].reset_index()
    return dtl


def most_active_week(selected_user,df):
    if selected_user!='Overall':
        df=df[df['User']==selected_user]
    return df['Day_name'].value_counts()

def most_active_month(selected_user,df):
    if selected_user!='Overall':
        df=df[df['User']==selected_user]
    return df['Month'].value_counts()

def heatmap(selected_user,df):
    if selected_user!='Overall':
        df=df[df['User']==selected_user]
    hm=df.pivot_table(index='Day_name',columns='Period',values='Message',aggfunc='count').fillna(0)
    return hm