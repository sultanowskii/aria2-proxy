import requests

url = 'http://0.0.0.0:6800/jsonrpc'

# jsonreq = {'jsonrpc':'2.0', 'id':'1', 'method':'aria2.addUri', 'params': [['https://en.wikipedia.org/static/images/icons/wikipedia.png'], dict(out='wiki.png', dir='/tmp')]}
# jsonreq = {'jsonrpc':'2.0', 'id':'1', 'method':'aria2.getUris', 'params': ['8a816f5d5d3cf35e']}
jsonreq = {'jsonrpc':'2.0', 'id':'1', 'method':'aria2.tellActive'}

# some clients (https://binux.github.io/yaaw/demo) use this for some reason
headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

res = requests.post(
    url,
    json=jsonreq,
    headers=headers,
)

print(res.json())
