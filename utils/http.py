from urllib import request
from urllib.parse import quote
import json
import string

def post(url, data = None):
    data = bytes(json.dumps(data), "utf-8")
    req = request.Request(url, data, {
        'Content-Type': 'application/json; charset=UTF-8'
    })

    response = request.urlopen(req).read().decode('utf-8')

    if not response:
        return None

    response = json.loads(response)

    return response

def get(url, headers = {}):
    url = quote(url, safe = string.printable)
    print("requesting: ", url)
    req = request.Request(url, headers = headers)
    response = request.urlopen(req).read().decode('utf-8')

    if not response:
        return None

    response = json.loads(response)

    return response
