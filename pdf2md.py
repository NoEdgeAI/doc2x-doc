import requests as rq
import json

class PDF2MD:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.doc2x.noedgeai.com/api/v1/pdf"
        self.export_url = "https://api.doc2x.noedgeai.com/api/export"

    def convert(self, filepath, to="md"):
        res = rq.post(self.url, files={"file": open(filepath, "rb")}, headers={"Authorization": "Bearer " + self.api_key}, stream=True)

        if res.status_code == 200:
            with open("demo.txt", "w", encoding="utf-8") as f:
                for line in res.iter_lines():
                    if len(line) > 0:
                        decoded_line = line.decode("utf-8")
                        f.write(decoded_line + "\n")
                        print(decoded_line)
            
            uuid = json.loads(decoded_line.replace("data: ", ''))['uuid']
            print(uuid)
            
            if to == "md" or to == 'latex':
                path = 'demo.' + 'zip'
            elif to == 'docx':
                path = 'demo.docx'
            
            export_url = self.export_url + "?request_id=" + uuid + "&to=" + to
            res = rq.get(export_url, headers={"Authorization": "Bearer " + self.api_key})
            
            if res.status_code == 200:
                with open(path, "wb") as f:
                    f.write(res.content)
                print("保存成功，存入：", path)
            else:
                print(format("[ERROR] status code: %d, body: %s" % (res.status_code, res.text)))
        else:
            print(format("[ERROR] status code: %d, body: %s" % (res.status_code, res.text)))



def main():
    api_key = "sk-xxxx"
    filepath = r"test.pdf"
    converter = PDF2MD(api_key)
    converter.convert(filepath, to="md")


if __name__ == "__main__":
    main()