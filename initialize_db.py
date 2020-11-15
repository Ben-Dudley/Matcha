#!/usr/local/bin/python3

import requests
import json

url = 'http://localhost:5000'
headers = {'Content-type': 'application/json'}


def apicall(method, verb='POST', body=''):
    body = body.encode(encoding='utf-8')
    if verb == 'POST':
        response = requests.post(f'{url}{method}', headers=headers, data=body, verify=False)
    else:
        print('Unrecognized verb')
        return (1, 0)
    if response.ok:
        #jdata = json.loads(response.content)
        #return (0, jdata)
        return response.content.decode('utf-8')
    return f"Error:{response.status_code} {response.url} {response.content.decode('utf-8')}"

# register users
with open('backend/matcha/data.json', encoding='utf-8') as f:
    data = json.loads(f.read())
    for user in data['users']:
        request_json = json.dumps(user)
        response = apicall('/user/register', body=request_json)
        print(response)
