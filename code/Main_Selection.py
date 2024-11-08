import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
import sqlite3

#connecting to database and load the tables
conn = sqlite3.connect('hushhushDB.db')


filename = "kmeans.pickle"
loaded_model = pickle.load(open(filename, 'rb'))

df = pd.read_csv("testdata.csv")
df2 = df.drop(columns=['Name', 'Email','Public Reposcount','Public Gistscount'])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df2)
cluster = loaded_model.predict(X_scaled)
df2['clusters'] = cluster
selected_id = df2[df2['clusters'] == 1]['id']
selectedtable = df[df['id'].isin(selected_id)][['Name', 'Email']].drop_duplicates()

#pushing the final list of candidates
selectedtable.to_sql('selected_users', conn, if_exists='replace', index=False)

# Close the SQLite connection
conn.close()

print("Data pushed to selected_users table successfully.")