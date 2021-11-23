import requests

stufF_del = [1]



for id in stufF_del:
    url = f"http://127.0.0.1:8000/blog/{id}"
    resp = requests.delete(url)
    resp.raise_for_status()
    print(resp.json)

