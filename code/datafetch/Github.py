import requests
import numpy as np
import pandas as pd
import time
from dotenv import load_dotenv
import os

load_dotenv()

# Defne the parameters
Repos_Data = []
User_Data = []
completed_user_id = 0
user_url =[]
Starred_Repos_Data =[]

#function to get user's basic details
def userdetails(id , user):
   Git_users_dict = {}
   Git_users_dict['user_id'] =id
   Git_users_dict['Email'] = user['email']
   Git_users_dict['Name']=  user['name'] 
   Git_users_dict['Followers Count']= user['followers']
   Git_users_dict['Following Count']= user['following']
   Git_users_dict['Public Reposcount']= user['public_repos']
   Git_users_dict['Public Gistscount']= user['public_gists']
   return Git_users_dict

#function to get user's Repo details
def UserRepoDetails (id , repos_data):
   Repos_list = []
   for repos in repos_data:
      if repos['language']:
         Repo_dict ={
            'user_id' : id,
            'stargazers_count' : repos['stargazers_count'],
            'watchers_count':  repos['watchers_count'],
            'repo_id' : repos['id'],
            'language' : repos['language'],
            'forks_count': repos['forks_count'],
            'open_issues': repos['open_issues']
            }
         Repos_list.append(Repo_dict)
   return Repos_list

# Logic for getting the data
headers = {
    "Authorization": f"token {os.getenv('GITHUB_TOKEN')}"
}
for j in range (0,875,30):
   link = f"https://api.github.com/users?since={j}"
   try:
      response = requests.get(link, headers=headers, timeout=5)
      response.raise_for_status()
      results = response.json()
      for user in results:
         user_url = user['url']
         repos_url = user['repos_url']

         #  To avoid duplicate fetching of same user data
         if(user['id'] > completed_user_id):
            usr = requests.get(user_url, headers= headers, timeout=5)
            usr.raise_for_status
            userdata = usr.json()
            repos = requests.get(repos_url, headers= headers, timeout=5)
            repos.raise_for_status
            reposdata = repos.json()

      # Get the basic user details and get the inner urls
            if(userdata['name']):
               print(f"Getting data for user id:{user['id']}")
               Git_users_dict = userdetails(user['id'],userdata)
               User_Data.append(Git_users_dict)
               time.sleep(1)
         
         # Gets the data from the repositories for the user
               Repo_dict = UserRepoDetails(user['id'], reposdata)
               Repos_Data.extend(Repo_dict)
               time.sleep(1)
      completed_user_id = user['id']

   except requests.exceptions.RequestException as e:
       print(f"Error fetching data for {j} with error {e}")

users_df = pd.DataFrame(User_Data)
users_df['Email'].fillna(users_df['Name'].str.replace(r'[^a-zA-Z0-9]', '', regex=True).str.lower() + '@gmail.com', inplace=True)
repos_df = pd.DataFrame(Repos_Data)
 
users_df.to_csv('Github_Users.csv', index=False)
repos_df.to_csv('Github_Users_Repos.csv', index=False)
