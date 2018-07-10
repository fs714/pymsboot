import json
import time

import requests

url = 'http://192.168.56.201:9666/'
print(json.dumps(requests.get(url).json(), indent=4))

url = 'http://192.168.56.201:9666/v1'
print(json.dumps(requests.get(url).json(), indent=4))

url = 'http://192.168.56.201:9666/v1/movies'
print(json.dumps(requests.get(url).json(), indent=4))

url = 'http://192.168.56.201:9666/v1/movies/c840f0b6-0d28-4c0c-abaa-f96dca76c057'
print(json.dumps(requests.get(url).json(), indent=4))

data = {
    'id': 'f11edef0-d6e6-4935-ac97-06769cc084a3',
    'name': 'Jian Guo Da Ye',
    'rank': 1,
    'url': 'http://www.baidu.com'
}

url = 'http://192.168.56.201:9666/v1/movies'
print(json.dumps(requests.post(url, json=data).json(), indent=4))

time.sleep(5)
url = 'http://192.168.56.201:9666/v1/movies/f11edef0-d6e6-4935-ac97-06769cc084a3'
for i in range(1, 6):
    print('------ {}s ------'.format(i * 5))
    print(json.dumps(requests.get(url).json(), indent=4))
    time.sleep(5)

url = 'http://192.168.56.201:9666/v1/movies'
print(json.dumps(requests.get(url).json(), indent=4))

data = {
    'id': 'f11edef0-d6e6-4935-ac97-06769cc084a3',
    'name': 'Jian Guo Da Ye',
    'rank': 1,
    'url': 'http://www.google.com'
}

url = 'http://192.168.56.201:9666/v1/movies/f11edef0-d6e6-4935-ac97-06769cc084a3'
print(json.dumps(requests.put(url, json=data).json(), indent=4))

time.sleep(5)
url = 'http://192.168.56.201:9666/v1/movies/f11edef0-d6e6-4935-ac97-06769cc084a3'
for i in range(1, 7):
    print('------ {}s ------'.format(i * 5))
    print(json.dumps(requests.get(url).json(), indent=4))
    time.sleep(5)

url = 'http://192.168.56.201:9666/v1/movies'
print(json.dumps(requests.get(url).json(), indent=4))

url = 'http://192.168.56.201:9666/v1/movies/f11edef0-d6e6-4935-ac97-06769cc084a3'
print(json.dumps(requests.delete(url).json(), indent=4))

url = 'http://192.168.56.201:9666/v1/movies'
print(json.dumps(requests.get(url).json(), indent=4))

time.sleep(10)
print('------ 15s ------')
url = 'http://192.168.56.201:9666/v1/movies'
print(json.dumps(requests.get(url).json(), indent=4))
