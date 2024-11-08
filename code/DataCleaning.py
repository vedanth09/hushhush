import pandas as pd
from difflib import SequenceMatcher
import sqlite3


#connecting to database and load the tables
conn = sqlite3.connect('hushhushDB.db')

Git_Users_df = pd.read_sql_query("SELECT * FROM github_users", conn)
Repos_df = pd.read_sql_query("SELECT * FROM github_users_repos", conn)
Stack_Users_df = pd.read_sql_query("SELECT * FROM stackoverflow_data",conn)

names_1 = Git_Users_df['Name']
names_2 = Stack_Users_df['display_name']

def is_similar(name1, name2, threshold=0.70):
    similarity_ratio = SequenceMatcher(None, name1, name2).ratio()
    return similarity_ratio >= threshold 

matches = []

user_counts = Repos_df['user_id'].value_counts().reset_index()
user_counts.columns = ['user_id', 'Repo_count'] 

for name1 in names_1:
    for name2 in names_2:
        if is_similar(name1, name2):  
            matches.append((name1, name2))

matches_df = pd.DataFrame(matches, columns=['Name in File Git', 'Name in File Stack'])

x = matches_df.drop_duplicates()

merged1_df = pd.merge(x, Git_Users_df, left_on='Name in File Git', right_on= 'Name', how='inner')  

merged2_df = pd.merge(merged1_df, Stack_Users_df, left_on='Name in File Stack', right_on= 'display_name', how='inner')  
merged =merged2_df.drop_duplicates()

mergeduser = merged.drop(columns=['Name in File Git','Name in File Stack'])

merge = pd.merge(mergeduser,user_counts , how='inner',left_on='user_id_x', right_on='user_id')
df = merge.rename(columns={'user_id_x': 'id'})

final = df.drop_duplicates()
Final = final.drop(columns=['display_name','reputation_change','link','user_id_y','user_id'])

# after cleaning pushing the data into live table.
Final.to_sql('live_data', conn, if_exists='replace', index=False)

# Close the SQLite connection
conn.close()
print("Data pulled, cleaned, and pushed to 'live_data' table successfully.")