import os 
import requests 
import requests.auth 
import pandas as pd 

#creds 
CLIENT_ID = 'REPLACE WITH YOUR PERSONAL USE SCRIPT' 
CLIENT_SECRET = 'REPLACE WITH YOUR SECRET' 
USERNAME = 'REPLAVCE WITH YOUR REDDIT USERNAME' 
PASSWORD = 'REPLACE WITH YOUR REDDIT PASSWORD' #remember to save these in your environment beforehand if using these on shared codespaces

#Authenticate Reddit App 
client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET) 
post_data = {'grant_type': 'password', 'username': USERNAME, 'password': PASSWORD} 
headers = { 'User-Agent': 'MyAPI/0/0/1 ' } 

# Getting Token Access ID 
TOKEN_ACCESS_ENDPOINT = 'https://www.reddit.com/api/v1/access_token' 
response = requests.post(TOKEN_ACCESS_ENDPOINT, data=post_data, headers=headers, auth=client_auth) 
if response.status_code == 200: 
    token_id = response.json()['access_token'] 
else: print("Auth failed:", response.status_code, response.text) 


# Use Reddit's REST API to perform operations 
OAUTH_URL = 'https://oauth.reddit.com' 
ENDPOINT = '/r/Audi/best/'
params_get = { 'limit': 100} 
headers_get = { 'User-Agent': 'MyAPI/0/0/1', 'Authorization': 'Bearer ' + token_id } 

response = requests.get(OAUTH_URL + ENDPOINT, headers=headers_get, params=params_get)

reddit_data = response.json() 

posts = [post['data'] for post in reddit_data['data']['children']]

df = pd.DataFrame(posts) 
#print(posts)
df.to_csv('dummy.csv', index=False)
