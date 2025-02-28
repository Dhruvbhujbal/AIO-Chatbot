import requests

API_KEY = "614dc19ab2ac16adf6a8a8d790719873"
city = "London"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

response = requests.get(url)

if response.status_code == 200:
    print("API key is working!")
    print(response.json())
else:
    print(f"Failed! Status code: {response.status_code}, Error: {response.text}")
