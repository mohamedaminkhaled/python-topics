import requests


def make_request(method, url, **kwargs):
    response = None
    try:
        response = requests.request(method, url, **kwargs)
    except Exception as err:
        print(err)
    return response
