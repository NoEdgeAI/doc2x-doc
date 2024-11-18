import json
import time
import requests as rq
import os

base_url = "https://v2.doc2x.noedgeai.com"
secret = os.getenv("DOC2X_APIKEY")


def preupload():
    url = f"{base_url}/api/v2/parse/preupload"
    headers = {"Authorization": f"Bearer {secret}"}
    res = rq.post(url, headers=headers)
    res.raise_for_status()  # 检查HTTP请求是否成功
    data = res.json()
    if data.get("code") == "success":
        return data["data"]
    raise Exception(f"get preupload url failed: {data}")


def put_file(path: str, url: str):
    with open(path, "rb") as f:
        res = rq.put(url, data=f)  # body为文件二进制流
        res.raise_for_status()  # 检查HTTP请求是否成功


def get_status(uid: str):
    url = f"{base_url}/api/v2/parse/status?uid={uid}"
    headers = {"Authorization": f"Bearer {secret}"}
    res = rq.get(url, headers=headers)
    res.raise_for_status()  # 检查HTTP请求是否成功
    data = res.json()
    if data.get("code") == "success":
        return data["data"]
    raise Exception(f"get status failed: {data}")


def main(file):
    upload_data = preupload()
    print(upload_data)
    url, uid = upload_data["url"], upload_data["uid"]

    put_file(file, url)

    max_retries = 100
    for retries in range(max_retries):
        status_data = get_status(uid)
        status = status_data.get("status")
        if status == "success":
            print("Save result to result.json")
            with open("result.json", "w") as f:
                json.dump(status_data["result"], f)
            return
        elif status == "failed":
            print(status_data)
            raise Exception(f"parse failed: {status_data.get('detail')}")
        elif status == "processing":
            print(status_data)
            print(f"progress: {status_data.get('progress')}")
            time.sleep(3)
    raise Exception(f"Fails to deal with uid: {uid} after {max_retries} retries")


if __name__ == "__main__":
    main("test.pdf")
