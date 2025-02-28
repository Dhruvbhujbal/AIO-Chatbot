from flask import Flask, render_template, request, jsonify
import random
import json
import re
import datetime
import calendar
import os
import requests
from groq import Groq

app = Flask(__name__)

# Load intents
with open('intents.json') as file:
    intents = json.load(file)

# Groq API Initialization
groq_api_key = os.environ.get("GROQ_API_KEY")  # Fetch Groq key from the correct environment variable
client = Groq(api_key=groq_api_key)

# OpenWeatherMap API Key
weather_api_key = os.environ.get("WEATHER_API_KEY")  # Fetch OpenWeather API key

# Store reminders (in-memory for simplicity)
reminders = []

def get_response(user_input):
    # Check if the user is asking for a calculator operation
    if "calculate" in user_input.lower() or any(char in user_input for char in '+-*/%^'):
        return calculator(user_input)
    elif "reminder" in user_input.lower():
        return set_reminder(user_input)
    elif "calendar" in user_input.lower() or "date" in user_input.lower():
        return show_calendar()
    elif "weather" in user_input.lower():
        return get_weather(user_input)
    return handle_groq_query(user_input)

def calculator(user_input):
    try:
        expression = re.sub('[^0-9+\-*/%^(). ]', '', user_input)
        result = eval(expression)
        return f"The result is: {result}"
    except Exception:
        return "Sorry, I couldn't process the calculation. Please try again."

def set_reminder(user_input):
    reminder = re.sub(r"(reminder|set reminder|remind me)", "", user_input, flags=re.I).strip()
    if reminder:
        reminders.append(reminder)
        return f"Reminder set: {reminder}"
    return "Please specify what you would like me to remind you about."

def show_calendar():
    today = datetime.date.today()
    day_of_week = today.strftime("%A")
    formatted_date = today.strftime("%B %d, %Y")
    return f"Today's date is {formatted_date}, and it is a {day_of_week}."

def handle_groq_query(user_input):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_input}],
            model="llama-3.3-70b-versatile"
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception:
        return "Sorry, I couldn't fetch the information at the moment. Please try again later."

def get_weather(user_input):
    try:
        match = re.search(r"weather in (\w+(?: \w+)*)", user_input, re.I)
        city = match.group(1) if match else "Pune"

        # Check if API key is set
        if not weather_api_key:
            return "Weather service API key is not set. Please configure it properly."

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        response = requests.get(url)

        if response.status_code != 200:
            return f"Error: Unable to fetch weather details for {city}. ({response.status_code}: {response.json().get('message')})"

        data = response.json()
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return f"The weather in {city.title()} is currently {description} with a temperature of {temperature:.1f}°C."

    except requests.RequestException:
        return "Network error: Unable to reach the weather service. Please try again."
    except KeyError:
        return f"Weather information for {city} is currently unavailable."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response_route():
    user_input = request.json.get("message")
    response = get_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
