import requests

if __name__ == '__main__':
    url = "http://127.0.0.1:8000/api/v1/estimation"
    file = {
        "image": open("20151127_121613.jpg", "rb")
    }
    data = {
        "user_id": "oh",
        "token": "token",
        "webhook_url": "https://test.test.ch",
    }
    resp = requests.post(url=url, files=file, params=data)
    print(resp.json())
