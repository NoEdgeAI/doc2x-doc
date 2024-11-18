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


def export_file(uid: str, to_format: str, formula_mode: str):
    url = f"{base_url}/api/v2/convert/parse"
    headers = {"Authorization": f"Bearer {secret}"}
    payload = {
        "uid": uid,
        "to": to_format,
        "formula_mode": formula_mode,
    }
    res = rq.post(url, headers=headers, json=payload)
    res.raise_for_status()  # 检查HTTP请求是否成功
    data = res.json()
    if data.get("code") == "success":
        return data["data"]
    raise Exception(f"export file failed: {data}")


def get_export_result(uid: str):
    url = f"{base_url}/api/v2/convert/parse/result?uid={uid}"
    headers = {"Authorization": f"Bearer {secret}"}
    res = rq.get(url, headers=headers)
    res.raise_for_status()  # 检查HTTP请求是否成功
    data = res.json()
    if data.get("code") == "success":
        return data["data"]
    raise Exception(f"get export result failed: {data}")


def download_file(file_url: str, output_path: str):
    res = rq.get(file_url)
    res.raise_for_status()  # 检查HTTP请求是否成功
    with open(output_path, "wb") as f:
        f.write(res.content)


def main(file):
    # 上传文件并等待解析完成
    upload_data = preupload()
    print(upload_data)
    url, uid = upload_data["url"], upload_data["uid"]

    put_file(file, url)

    for _ in range(100):
        status_data = get_status(uid)
        status = status_data.get("status")
        if status == "success":
            print("Save result to result.json")
            with open("result.json", "w") as f:
                json.dump(status_data["result"], f)
            break
        elif status == "failed":
            print(status_data)
            raise Exception(f"parse failed: {status_data.get('detail')}")
        elif status == "processing":
            print(status_data)
            print(f"progress: {status_data.get('progress')}")
            time.sleep(3)
    else:
        raise Exception(f"Fails to deal with uid: {uid} after 100 retries")

    # 导出文件
    print("Start exporting file...")
    export_file(uid, "docx", "normal")  # 可以根据需要修改格式和公式模式

    for _ in range(100):
        result_data = get_export_result(uid)
        status = result_data.get("status")
        if status == "success":
            file_url = result_data["url"]
            output_path = "output.docx"  # 根据实际格式修改扩展名
            print(f"Downloading file to {output_path}")
            download_file(file_url, output_path)
            return
        elif status == "failed":
            print(result_data)
            raise Exception("Export failed")
        elif status == "processing":
            print("Export processing...")
            time.sleep(3)
    raise Exception(f"Export timeout with uid: {uid} after 100 retries")


if __name__ == "__main__":
    main("test.pdf")
