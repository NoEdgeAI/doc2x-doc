import requests as rq

url = "https://api.doc2x.noedgeai.com/api/v1/limit"
api_key = ""

res = rq.get(url, headers={"Authorization": "Bearer " + api_key})
if res.status_code == 200:
    res_json = res.json()
    print(format("remain: %d" % (res_json["data"]["remain"])))
else:
    print(format("[ERROR] status code: %d, body: %s" % (res.status_code, res.text)))