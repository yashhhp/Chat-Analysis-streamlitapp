import pandas as pd
import re
def process(data):
    pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    mess=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({'Message':mess,'Date':dates})
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y, %H:%M - ')
    users=[]
    mes=[]
    for mess in df['Message']:
        entry=re.split('([\w\W]+?):\s',mess)
        if entry[1:]:
            users.append(entry[1])
            mes.append(entry[2])
        else:
            users.append('group_notification')
            mes.append(entry[0])

    df['User']=users
    df.Message=mes
    df['Year']=df['Date'].dt.year
    df['Month']=df['Date'].dt.month_name()
    df['Month Number']=df['Date'].dt.month 
    df['Date_time']=df['Date'].dt.date
    df['Day_name']=df['Date'].dt.day_name()
    df['Day']=df['Date'].dt.day
    df['Hour']=df['Date'].dt.hour
    df['Minute']=df['Date'].dt.minute
    P=[]
    for h in df[['Day_name','Hour']]['Hour']:
        if h==23:
            P.append(str(h)+"-"+str('00'))
        elif h==0:
            P.append(str('00')+"-"+str(h+1))
        else:
            P.append(str(h)+"-"+str(h+1))
    df['Period']=P
    return df 
