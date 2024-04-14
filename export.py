import requests as rq

uuid = ""
to = "docx"
url = "https://api.doc2x.noedgeai.com/api/export"+"?request_id="+uuid+"&to="+to
api_key = ""


res = rq.get(url, headers={"Authorization": "Bearer " + api_key})
if res.status_code == 200:
    # save as res.docx
    with open("res.docx", "wb") as f:
        f.write(res.content)
else:
    print(format("[ERROR] status code: %d, body: %s" % (res.status_code, res.text)))