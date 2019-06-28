import requests

from service.Encode import MyEncoder

cloud_server = "http://192.168.43.28:5000"
cloud_port = 5000


def post_request(path, data):
    r = requests.post(cloud_server + path, json=MyEncoder().encode(data))
    print(r.status_code, r.reason)
