import requests

if __name__ == '__main__':
    url = "http://127.0.0.1:5000/api/v1/estimation/calories"
    file = {"image": open("20151127_121613.jpg", "rb")}
    resp = requests.post(url=url, files=file)
    print(resp.json())
