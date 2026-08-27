import requests

CLIENT_ID = 'REDACTED'
SECRET_ID = 'REDACTED'
url = 'https://www.reddit.com/api/v1/access_token'
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_ID)
print(auth)

data = {
    'grant_type': 'password',
    'username': 'MorganPGBot',
    'password': 'REDACTED',
    'scope': 'identity edit flair history modconfig modflair modlog modposts modwiki mysubreddits privatemessages read report save submit subscribe vote wikiedit wikiread'
}

headers = {'User-Agent': 'MorganPGBot/0.0.1'}
res = requests.post(url=url, auth=auth, data=data, headers=headers)
print(res.text)
headers_auth = {'User-Agent': 'MorganPGBot/0.0.1', 'Authorization': 'bearer ' + res.json()["access_token"]}

print(headers_auth)
posts = requests.get('https://oauth.reddit.com/user/MorganPG1/submitted?count=25&limit=25&show=given&sort=new', headers=headers_auth)
#posts = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers_auth)
sub = posts.json()["data"]["children"][0]["data"]["subreddit"]
url2 = posts.json()["data"]["children"][0]["data"]["url"]
title = posts.json()["data"]["children"][0]["data"]["title"]
author = posts.json()["data"]["children"][0]["data"]["author"]
print(sub, url2, title)
post_data = {'sr': 'u_morganpgbot', 'kind': 'self', 'title': 'Post by '+author+' in '+sub+'!', 'text': author+' made a post in '+sub+' with the title '+title+'! Source: '+url2}

test = requests.post('https://oauth.reddit.com/api/submit', headers=headers_auth, data=post_data)
print(test.text)