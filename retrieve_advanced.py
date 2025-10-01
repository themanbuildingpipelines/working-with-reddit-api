import os
import requests
import requests.auth
import pandas as pd

# ==========================
# 1. Defining Credentials
# ==========================
CLIENT_ID = "REPLACE_WITH_YOUR_PERSONAL_USE_SCRIPT"
CLIENT_SECRET = "REPLACE_WITH_YOUR_SECRET"
USERNAME = "REPLACE_WITH_YOUR_REDDIT_USERNAME"
PASSWORD = "REPLACE_WITH_YOUR_REDDIT_PASSWORD" #Remember: store these in environment variables if using shared codespaces

# ==========================
# 2. Authentication
# ==========================
client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
post_data = {
    "grant_type": "password",
    "username": USERNAME,
    "password": PASSWORD
}
headers = {"User-Agent": "MyAPI/0/0/1"}

TOKEN_ACCESS_ENDPOINT = "https://www.reddit.com/api/v1/access_token"
response = requests.post(TOKEN_ACCESS_ENDPOINT, data=post_data, headers=headers, auth=client_auth)

if response.status_code == 200:
    token_id = response.json()["access_token"]
else:
    print("Auth failed:", response.status_code, response.text)
    exit()

# ==========================
# 3. Pulling Data
# ==========================
OAUTH_URL = "https://oauth.reddit.com"
headers_get = {
    "User-Agent": "MyAPI/0/0/1",
    "Authorization": f"Bearer {token_id}"
}

def fetch_posts(endpoint, max_posts=1000):
    all_posts = []
    after = None

    while len(all_posts) < max_posts:
        params = {"limit": 100, "after": after}
        resp = requests.get(OAUTH_URL + endpoint, headers=headers_get, params=params)

        if resp.status_code != 200:
            print(f"Request failed: {resp.status_code} {resp.text}")
            break

        data = resp.json()["data"]
        children = data.get("children", [])
        if not children:
            break

        for post in children:
            all_posts.append(post["data"])  #collect full post info

        after = data.get("after")
        if after is None:
            break

    return all_posts

# ==========================
# 4. Define Sources
# ==========================
sources = {
    "DataEngineering Best": "/r/DataEngineering/best",
    "CloudEngineering New": "/r/CloudEngineering/new",
    "Python Hot": "/r/Python/hot"
    # Add any subreddit + listing type here
}

# ==========================
# 5. Run Collection
# ==========================
all_data = []
for source, endpoint in sources.items():
    posts = fetch_posts(endpoint, max_posts=1000)  # fetch up to 200 per source
    for p in posts:
        p["source"] = source
    all_data.extend(posts)
    print(f"Fetched {len(posts)} posts from {source}")

df = pd.DataFrame(all_data)
print(df.head())
print("Total posts collected:", len(df))
