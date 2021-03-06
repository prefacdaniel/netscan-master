import requests
import urllib.request

from service.Encode import MyEncoder

cloud_server = "http://192.168.0.101:5000"
cloud_port = 5000


def post_request(path, data):
    r = requests.post(cloud_server + path, json=MyEncoder().encode(data))
    print(r.status_code, r.reason)


def get_request(path, data):
    r = requests.get(cloud_server + path, json=MyEncoder().encode(data))
    print(r.status_code, r.reason)


def get_request_by_id(path):
    r = requests.get(cloud_server + path)
    return r.content


def get_training_for_device(device_id):
    path = "/getactivetraining/" + str(device_id)
    return get_request_by_id(path)


def get_training_model_for_device(device_id):
    path = "/getactivetrainingmodel/" + str(device_id)
    return get_request_by_id(path)
