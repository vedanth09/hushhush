import sqlite3
import pandas as pd

# Establish a connection to the SQLite database
conn = sqlite3.connect('hushhushDB.db')
c = conn.cursor()
# Creating table for Github_Users
c.execute('''
    CREATE TABLE IF NOT EXISTS github_users (
        user_id INTEGER PRIMARY KEY,
        Email TEXT,
        Name TEXT,
        Followers_Count INTEGER,
        Following_Count INTEGER,
        Public_Reposcount INTEGER,
        Public_Gistscount INTEGER
    )
''')
conn.commit()


# Read the CSV file into a DataFrame
github_users_df = pd.read_csv('Github_Users.csv')

# Print DataFrame columns and the first few rows for debugging
print("Github Users DataFrame columns:", github_users_df.columns)
print(github_users_df.head())

# # Define the insert query for github_users
insert_github_users_query = '''
    INSERT INTO github_users (
        user_id, Email, Name, Followers_Count, Following_Count, Public_Reposcount, Public_Gistscount
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
'''

# # Insert data into the github_users table
for row in github_users_df.itertuples(index=False, name=None):
    if len(row) == 7:  # Ensure the row has exactly 7 values
        c.execute(insert_github_users_query, row)
    else:
        print(f"Skipping row with incorrect number of values: {row}")

conn.commit()

# Creating table for Github_Users_Repos
c.execute('''
    CREATE TABLE IF NOT EXISTS github_users_repos (
        user_id INTEGER,
        stargazers_count INTEGER,
        watchers_count INTEGER,
        repo_id INTEGER PRIMARY KEY,
        language TEXT,
        forks_count INTEGER,
        open_issues INTEGER,
        FOREIGN KEY (user_id) REFERENCES github_users(user_id)
    )
''')

conn.commit()

# Read the CSV file into a DataFrame
github_users_repos_df = pd.read_csv('Github_Users_Repos.csv')

# # Print DataFrame columns and the first few rows for debugging
print("Github Users Repos DataFrame columns:", github_users_repos_df.columns)
print(github_users_repos_df.head())

# # Define the insert query for github_users_repos
insert_github_users_repos_query = '''
    INSERT INTO github_users_repos (
        user_id, stargazers_count, watchers_count, repo_id, language, forks_count, open_issues
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
'''

# # Insert data into the github_users_repos table
for row in github_users_repos_df.itertuples(index=False, name=None):
    if len(row) == 7:  # Ensure the row has exactly 7 values
        c.execute(insert_github_users_repos_query, row)
    else:
        print(f"Skipping row with incorrect number of values: {row}")

conn.commit()

c.execute('''
    CREATE TABLE IF NOT EXISTS stackoverflow_data(
    view_count INTEGER,
    answer_count INTEGER,
    question_count INTEGER,
    reputation_change INTEGER,
    reputation INTEGER,
    link TEXT,
    display_name TEXT,
    user_id INTEGER,
    bronze INTEGER,
    silver INTEGER,
    gold INTEGER
    )
''')

conn.commit()

# Read the CSV file into a DataFrame
stackoverflow_df = pd.read_csv('stackoverflow_newdata.csv')

# Print DataFrame columns and the first few rows for debugging
print("StackOverflow DataFrame columns:", stackoverflow_df.columns)
print(stackoverflow_df.head())

# Define the insert query for stackoverflow_users
insert_stackoverflow_query = '''
    INSERT INTO stackoverflow_data (view_count, answer_count, question_count, reputation_change, reputation, link, display_name, user_id, bronze, silver, gold) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
'''

# Insert data into the stackoverflow_users table
for row in stackoverflow_df.itertuples(index=False, name=None):
    if len(row) == 11:  # Ensure the row has exactly 11 values
        c.execute(insert_stackoverflow_query, row)
    else:
        print(f"Skipping row with incorrect number of values: {row}")

conn.commit()

# Creating table for Github_Users_Repos
c.execute('''
    CREATE TABLE IF NOT EXISTS selected_users (
        Name varchar(255),
        Email varchar(255)
    )
''')

conn.commit()

c.execute('''
CREATE TABLE IF NOT EXISTS live_data(
          user_id INTEGER,
          name varchar(255),
          followers_count INTEGER,
          following_count INTEGER,
          public_reposcount INTEGER,
          public_gistscount INTEGER,
          view_count INTEGER,
          answer_count INTEGER,
          question_count INTEGER,
          reputation INTEGER,
          bronze INTEGER,
          silver INTEGER,
          gold INTEGER,
          repo_count INTEGER
           )
''')

conn.commit()