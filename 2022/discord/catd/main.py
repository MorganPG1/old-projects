from pickle import NONE
import requests
import json 

#Configuration
webhook = 'https://discord.com/api/webhooks/REDACTED' #Webhook URL
wname = "Cat Of The Day" #Webhook Name
wava = ""
url = 'https://api.thecatapi.com/v1/images/search'
surl = 'https://api.thecatapi.com/v1/images/'
#Code
a = requests.get(url)
ab = a.text
jsond = json.loads(ab)
b = requests.get('https://some-random-api.ml/facts/cat')
bc = b.text
jsond2 = json.loads(bc)
url2 = jsond[0]["url"]
fact = jsond2["fact"]
print(fact)
print(url2)
embed = [{ "title": "Cat of the day", "url":url2, "footer": { "text": "Did you know? " + fact}, "description":"@everyone, Here is the cat of the day!", "image":{"url": url2} }]
embed2 = json.dumps(embed)
dc = requests.post(webhook, json.dumps({"username":wname, "avatar_url": url2, "embeds":embed}), headers={"Content-Type": "application/json"})
print(dc.status_code, dc.text)

#"image":{"url": url2}