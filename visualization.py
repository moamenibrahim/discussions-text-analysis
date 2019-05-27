
#%%
import os
import sys
import json
import re
import nltk
import plotly
import operator
import string
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns

plotly.tools.set_credentials_file(
    username='moamenibrahim', api_key='mV0gCyPj5sIKGQqC78zC')


#%%
data  = pd.read_csv('scraped_data/processed.csv')


#%%
porter = nltk.stem.porter.PorterStemmer()


#%%
df = data 
df.info()


#%%
df['main_thread']=df['time'].apply(lambda x: False if 'in response to' in x else True)


#%%
thread_divided = tuple(df.groupby(data['thread']))


#%%
tuple(df.groupby(data['thread']))


#%%
df.head()


#%%
re.findall(r'[\d]{1,2} [ADFJMNOS]\w* [\d]{4}', df['time'][0])


#%%
from dateutil.parser import parse
##'%m/%d/%Y %I:%M%p'
df['time_adjusted']=df['time'].apply(lambda x: re.findall(r'[\d]{1,2} [ADFJMNOS]\w* [\d]{4}',x)[0])    


#%%
df.head()


#%%



#%%
df['user'].value_counts().plot(kind='barh')


#%%



#%%
df['sentiment'].value_counts().plot(kind='barh')


#%%
df['topic'].value_counts()[:20].plot(kind='barh')


#%%
import ast
from collections import Counter


#%%
topic_items=[]

def add_to_dict(string_list):
    try:
        string_list = ast.literal_eval(string_list)
        string_list = [n.strip() for n in string_list]
        for item in string_list:
            topic_items.append(item)
    except TypeError:
        pass
        
df['topic'].apply(lambda x: add_to_dict(x));
staged_topics = Counter(topic_items)
staged_topics = {x : staged_topics[x] for x in staged_topics if len(x) >= 3}
staged_topics = sorted(staged_topics.items(), key=operator.itemgetter(1), reverse=True)


#%%
staged_topics


#%%
sentiment_items=[]

def add_to_sentiment(string_list):
    try:
        string_list = ast.literal_eval(string_list)
        string_list = [n.strip() for n in string_list]
        for item in string_list:
            sentiment_items.append(item)
    except ValueError:
        pass
        
df['sentiment'].apply(lambda x: add_to_sentiment(x));
staged_sentiment = Counter(sentiment_items)
staged_sentiment = {x : staged_sentiment[x] for x in staged_sentiment if len(x) >= 1}
staged_sentiment = sorted(staged_sentiment.items(), key=operator.itemgetter(1), reverse=True)


#%%
staged_sentiment


#%%
from math import log


#%%
testList = [(elem1, elem2) for elem1, elem2 in staged_sentiment]
testList = sorted(testList, key=lambda x: int(x[0]))
zip(*testList)
plt.scatter(*zip(*testList))
plt.show()


#%%
testList2 = [(elem1, elem2) for elem1, elem2 in staged_topics][:12]
zip(*testList2)
plt.scatter(*zip(*testList2))
plt.show()


#%%



#%%
import cancerType

for i,x in enumerate(df['tidy_text']):
    cancerType.get_cancer_type(x, df.loc[i]['user'])


#%%



#%%



