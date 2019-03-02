
#%%
import re
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import string
import nltk
import warnings 
warnings.filterwarnings("ignore", category=DeprecationWarning)

data  = pd.read_csv('scraped_data/cancerUK.csv')

data.head()


#%%
combi = data

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
        
    return input_txt    

# remove twitter handles (@user)
combi['tidy_text'] = np.vectorize(remove_pattern)(combi['text'], "@[\w]*")

# remove special characters, numbers, punctuations
combi['tidy_text'] = combi['tidy_text'].str.replace("[^a-zA-Z#]", " ")

combi['tidy_text'] = combi['tidy_text'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))
combi.head()


#%%
tokenized_tweet = combi['tidy_text'].apply(lambda x: x.split())
tokenized_tweet.head()


#%%
from nltk.stem.porter import *
stemmer = PorterStemmer()

tokenized_tweet = tokenized_tweet.apply(lambda x: [stemmer.stem(i) for i in x]) # stemming
tokenized_tweet.head()


#%%
for i in range(len(tokenized_tweet)):
    tokenized_tweet[i] = ' '.join(tokenized_tweet[i])

combi['tidy_text'] = tokenized_tweet


#%%
all_words = ' '.join([text for text in combi['tidy_text']])
from wordcloud import WordCloud
wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)


#%%
plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()


#%%
# function to collect hashtags
def hashtag_extract(x):
    hashtags = []
    # Loop over the words in the tweet
    for i in x:
        ht = re.findall(r"#(\w+)", i)
        hashtags.append(ht)

    return hashtags


#%%
# extracting hashtags from non racist/sexist tweets

HT_regular = hashtag_extract(combi['tidy_text'])

#%%
# unnesting list
HT_regular = sum(HT_regular,[])
a = nltk.FreqDist(HT_regular)
d = pd.DataFrame({'Hashtag': list(a.keys()),
                  'Count': list(a.values())})
# selecting top 10 most frequent hashtags     
d = d.nlargest(columns="Count", n = 10) 
plt.figure(figsize=(16,5))
ax = sns.barplot(data=d, x= "Hashtag", y = "Count")
ax.set(ylabel = 'Count')
plt.show()


#%%
from sklearn.feature_extraction.text import CountVectorizer
bow_vectorizer = CountVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')
# bag-of-words feature matrix
bow = bow_vectorizer.fit_transform(combi['tidy_text'])


#%%
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')
# TF-IDF feature matrix
tfidf = tfidf_vectorizer.fit_transform(combi['tidy_text'])


#%%
import pickle
pkl_filename = "scraped_data/pickle_model.pkl"  
# Load from file
with open(pkl_filename, 'rb') as file:  
    pickle_model = pickle.load(file)


#%%
# Calculate the predict target values
print(pickle_model)
prediction = pickle_model.predict_proba(tfidf)
print(prediction)
Ypredict = pickle_model.predict(bow) 
print(bow)
