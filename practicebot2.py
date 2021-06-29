import discord
import os
import json
import requests

url = "https://api.syncretism.io/ops"
userin = '{"itm":true,"otm":false,"max-diff":30,"calls":true,"order-by":"iv_desc","stock":true,"limit":1}'
resp = requests.get(url=url, data = userin, headers= {'Content-Type': 'application/json'})
data = resp.json() 

print(resp)
print(data)


