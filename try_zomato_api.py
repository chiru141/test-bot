import os
import requests
import json

zomato_api_key = "bdb3b7c195a74c2b0deefe4534c6a410"

raw_data=os.popen("curl https://developers.zomato.com/api/v2.1/categories?apikey=bdb3b7c195a74c2b0deefe4534c6a410").read()
data = json.loads(raw_data)
print data