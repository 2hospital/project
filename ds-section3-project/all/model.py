import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle
from pymongo import MongoClient

os.chdir(os.path.abspath(os.path.dirname(__file__)))

HOST = 'cluster0.qmfz4.mongodb.net'
USER = 'user'
PASSWORD = 'user1234'
DATABASE_NAME = 'algae'
COLLECTION_NAME = 'algae'
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)

database = client[DATABASE_NAME]

collection = database[COLLECTION_NAME]

df = pd.DataFrame([i for i in collection.find()])

df.drop('_id',axis=1,inplace=True)

df.month = df.month.astype('object')

df_dum = pd.get_dummies(df, prefix=['month'])

skewed_data = ['pH','NTU','chl-a','cyan']
df_dum[skewed_data] = df_dum[skewed_data].applymap(lambda x: np.log(x) if x > 0 else 0)

target = 'cyan'
features = df_dum.columns.drop(target)

train, test = train_test_split(df_dum,test_size=0.2,random_state=2)

X_train = train[features]
y_train = train[target]
X_test = test[features]
y_test = test[target]

rf = RandomForestRegressor(n_jobs=-1, random_state=2)

rf.fit(X_train, y_train)

with open('model.pkl','wb') as pickle_file:
    pickle.dump(rf, pickle_file)