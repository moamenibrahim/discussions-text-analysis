########################################################
#### Purpose of this file to convert mongodb to csv ####
########################################################

import pymongo
import pandas as pd

database_url="mongodb://localhost"

with pymongo.MongoClient(database_url,port=12345) as client:
  data = []
  collection = client.get_database('mydatabase')['users']
  raw=list(collection.find())
  for item in raw:
    p_id, p_info = item.items()
    user=p_info[0]
    for post in item[user]: 
        for thread in post:
            for item in post[thread]:
                time = list(item.keys())[0]
                text = list(item.values())[0]
                data.append([user,thread,time,text])
df=pd.DataFrame(data, columns = ["user", "thread", "time", "text"])
df.to_csv('scraped_data/cancerUK.csv', sep='\t')