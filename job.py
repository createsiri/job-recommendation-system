import streamlit as st
import pandas as pd
import pickle

import re  # regular experssion
import nltk # natural language tool kit
#SpaCy
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

ps=PorterStemmer()

def clean(text):
    data1=re.sub(r'[^ a-z A-Z 0-9 \s]',' ',text ) # he took value
    data2=nltk.word_tokenize(data1)
    data3=[ps.stem(i) for i in data2 if i not in stopwords.words('english')]
    return " ".join(data3) # data3  is list. converting list in string


def xyz(choice):
    tab = t_sample[t_sample['Position'] == choice].index[0]
    tab = t_sample.index.get_loc(tab)
    distance = simly[tab]
    job_list = sorted(list(enumerate(distance)), reverse=True, key=lambda dis: dis[1])[1:12]

    job = []
    company= []
    city=[]
    state=[]
    for i in job_list:
        job.append(sample.iloc[i[0]]["Position"])
        company.append(sample.iloc[i[0]]["Company"])
        city.append(sample.iloc[i[0]]["City"])
        state.append(sample.iloc[i[0]]["State.Name"])
    return job, company, city, state


simly=pickle.load(open('simly.pkl','rb'))
sample=pd.read_csv('sample.csv')
t_sample = pickle.load(open('t_sample.pkl','rb'))

st.title('Job Recommendation')
pos=st.selectbox('select position',sample['Position'])


if st.button('recommend',use_container_width=True):
    pos=clean(pos)

    rec_jobs, rec_company, rec_city, rec_state = xyz(pos)

    rec_data = {"Jobs": rec_jobs, "Company": rec_company, "City": rec_city, "State": rec_state}
    rec_df = pd.DataFrame(rec_data)
    rec_df.index = rec_df.index + 1

    st.table(rec_df)
