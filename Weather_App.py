import requests

api_key = "b7d807b470fefb5b9aa74bf7512076bc"

user_input = input("Enter City: ")

weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_input},PH&units=metric&appid={api_key}")
weather.raise_for_status()
data = weather.json()
print(data)
forecast = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={user_input}&appid={api_key}")
days = forecast.json()
# print(days)

# if data['cod'] != 200:  
#     print("No City found")
# else:
#     weather = data['weather'][0]['main']
#     temp = round(data['main']['temp'], 2)

#     print(f"{user_input.title()} Weather")
#     print(f"Weather: {weather}")
#     print(f"Temperature: {temp}\u00b0C")