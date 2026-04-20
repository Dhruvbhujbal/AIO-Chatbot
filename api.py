import requests

API_KEY = "api here"
city = "London"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

response = requests.get(url)

if response.status_code == 200:
    print("API key is working!")
    print(response.json())
else:
    print(f"Failed! Status code: {response.status_code}, Error: {response.text}")
