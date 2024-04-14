import requests as rq

url = "https://api.doc2x.noedgeai.com/api/v1/img"
api_key = ""
filepath = "test.jpg"

res = rq.post(url, files={"file": open(filepath, "rb")}, headers={"Authorization": "Bearer " + api_key}, stream=True)

if res.status_code == 200:
    for line in res.iter_lines():
        if len(line) > 0:
            print(line)
else:
    print(format("[ERROR] status code: %d, body: %s" % (res.status_code, res.text)))

