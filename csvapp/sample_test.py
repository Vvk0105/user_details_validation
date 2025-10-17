import requests

url = "http://127.0.0.1:8000/upload/"

for i in range(105):
    r = requests.get(url)
    print(f"Request {i+1}: {r.status_code} Remaining: {r.headers.get('X-RateLimit-Remaining')}")
    if r.status_code == 429:
        print("Request Blocked")
        print(r.json())
        break
