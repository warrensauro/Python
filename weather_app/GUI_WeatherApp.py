import os, requests, sys, datetime
from dotenv import load_dotenv
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QFrame,
    QLabel, QLineEdit, QPushButton, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from collections import defaultdict

load_dotenv()
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(480, 780)
        self.setWindowTitle("Weather App")
        self.setStyleSheet("QMainWindow {background-color: #F1EFE8}")
        self.initUI()
        
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        header_container = QWidget()
        header_container.setStyleSheet("background-color: #185FA5")
        header = QHBoxLayout(header_container)
        header.setContentsMargins(20, 16, 20, 16)
        header.setSpacing(10)

        self.search_bar = QLineEdit()
        self.search_bar.setStyleSheet("QLineEdit {padding: 7px 12px; color: #ffffff; background-color: rgba(255,255,255,0.15); border-radius: 8px; font-size: 13px}")
        self.search_bar.setPlaceholderText("Search city...")

        self.button = QPushButton("Search")
        self.button.setStyleSheet("QPushButton {padding: 7px 14px; background-color: rgba(255,255,255,0.2); color: #ffffff; border-radius: 8px; font-size: 13px; font-weight: 500}")
        header.addWidget(self.search_bar)
        header.addWidget(self.button)

        hero_container = QWidget()
        hero_container.setStyleSheet("background-color: #378ADD")
        hero = QVBoxLayout(hero_container)
        hero.setContentsMargins(24, 28, 24, 20)
        hero.setSpacing(0)

        self.city_label = QLabel("Manila, PH")
        self.city_label.setStyleSheet("font-size: 13px;color: rgba(255,255,255,0.8); letter-spacing: 0.5px;")
        self.date_label = QLabel("Tuesday, March 19")
        self.date_label.setStyleSheet("font-size: 11px; color: rgba(255,255,255,0.6)")
        self.icon_label = QLabel("S")
        self.icon_label.setFixedSize(72, 72)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("background-color: rgba(255,255,255,0.18); border-radius: 36px")
        self.temp_label = QLabel("32 C")
        self.temp_label.setStyleSheet("font-size: 58px; font-weight: 500; color: #ffffff")
        self.condition_label = QLabel("Sunny")
        self.condition_label.setStyleSheet("font-size: 14px; color: rgba(255,255,255,0.85)")

        hero.addWidget(self.city_label, alignment=Qt.AlignmentFlag.AlignCenter)
        hero.addSpacing(4)
        hero.addWidget(self.date_label, alignment=Qt.AlignmentFlag.AlignCenter)
        hero.addSpacing(20)
        hero.addWidget(self.icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
        hero.addSpacing(10)
        hero.addWidget(self.temp_label, alignment=Qt.AlignmentFlag.AlignCenter)
        hero.addSpacing(6)
        hero.addWidget(self.condition_label, alignment=Qt.AlignmentFlag.AlignCenter)
        hero.addSpacing(16)

        quick_stats = QHBoxLayout()
        quick_stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero.addLayout(quick_stats)
        quick_stats.setSpacing(24)

        feel_box = QVBoxLayout()
        feel_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quick_stats.addLayout(feel_box)
        feel_label = QLabel("FEELS LIKE")
        feel_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        feel_label.setStyleSheet("font-size: 11px; color: rgba(255,255,255,0.7)")
        self.feel_value = QLabel("35")
        self.feel_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feel_value.setStyleSheet("font-size: 11px;font-weight: 500; color: rgba(255,255,255,0.8)")
        feel_box.addWidget(feel_label)
        feel_box.addSpacing(2)
        feel_box.addWidget(self.feel_value)

        humid_box = QVBoxLayout()
        humid_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quick_stats.addLayout(humid_box)
        humid_label = QLabel("HUMIDITY")
        humid_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        humid_label.setStyleSheet("font-size: 11px; color: rgba(255,255,255,0.7)")
        self.humid_value = QLabel("78%")
        self.humid_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.humid_value.setStyleSheet("font-size: 11px;font-weight: 500; color: rgba(255,255,255,0.8)")
        humid_box.addWidget(humid_label)
        humid_box.addSpacing(2)
        humid_box.addWidget(self.humid_value)

        wind_box = QVBoxLayout()
        wind_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quick_stats.addLayout(wind_box)
        wind_label = QLabel("WIND")
        wind_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wind_label.setStyleSheet("font-size: 11px; color: rgba(255,255,255,0.7)")
        self.wind_value = QLabel("12 km/h")
        self.wind_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wind_value.setStyleSheet("font-size: 11px;font-weight: 500; color: rgba(255,255,255,0.8)")
        wind_box.addWidget(wind_label)
        wind_box.addSpacing(2)
        wind_box.addWidget(self.wind_value)

        details_container = QWidget()
        details_container.setStyleSheet("background-color: #F1EFE8")
        details = QGridLayout(details_container)
        details.setContentsMargins(20, 16, 20, 16)
        details.setSpacing(10)

        pressure_card, self.pressure_value = self.create_card("Pressure")
        details.addWidget(pressure_card, 0, 0)

        visibility_card, self.visibility_value = self.create_card("Visibility")
        details.addWidget(visibility_card, 0, 1)
        
        uv_card, self.uv_value = self.create_card("UV Index", value_color="#BA7517")
        details.addWidget(uv_card, 1, 0)

        sun_card, self.sun_value = self.create_card("Sunrise / Sunset", font_size="13px")
        details.addWidget(sun_card, 1, 1)

        forecast_container = QWidget()
        forecast_container.setStyleSheet("QWidget{background-color: #F1EFE8; border-top: 1px solid #D3D1C7} QLabel{border: none}")
        forecast_main = QVBoxLayout(forecast_container)
        forecast_main.setContentsMargins(20, 14, 20, 14)
        forecast_title = QLabel("5-DAY FORECAST")
        forecast_title.setStyleSheet("font-size: 11px; color: #888780; letter-spacing: 0.5px")
        forecast_main.addWidget(forecast_title)
        forecast_main.addSpacing(10)
        forecast_column = QHBoxLayout()
        forecast_main.addLayout(forecast_column)

        sun_cast, self.sun_icon, self.sun_temp = self.forecast("Sun")
        mon_cast, self.mon_icon, self.mon_temp = self.forecast("Mon")
        tue_cast, self.tue_icon, self.tue_temp = self.forecast("Tue")    
        wed_cast, self.wed_icon, self.wed_temp = self.forecast("Wed")
        thu_cast, self.thu_icon, self.thu_temp = self.forecast("Thu")

        forecast_column.addLayout(sun_cast)
        forecast_column.addLayout(mon_cast)
        forecast_column.addLayout(tue_cast)
        forecast_column.addLayout(wed_cast)
        forecast_column.addLayout(thu_cast)

        for i in range(5):
            forecast_column.setStretch(i, 1)

        status_container = QWidget()
        status_container.setStyleSheet("QWidget {background: #F1EFE8; border-top: 1px solid #D3D1C7} QLabel {border: none}")
        status = QHBoxLayout(status_container)
        status.setContentsMargins(20, 10, 20, 10)
        self.updated = QLabel("Last Updated: --:--")
        self.updated.setStyleSheet("font-size: 11px; color: #888780")
        self.refresh = QPushButton("Refresh")
        self.refresh.setStyleSheet("font-size: 11px; color: #185FA5; font-weight: 500")
        self.refresh.setFlat(True)
        status.addWidget(self.updated)
        status.addStretch(1)
        status.addWidget(self.refresh)

        main_layout.addWidget(header_container)
        main_layout.addWidget(hero_container)
        main_layout.addWidget(details_container)
        main_layout.addWidget(forecast_container)
        main_layout.addWidget(status_container)
        central_widget.setLayout(main_layout)

        self.button.clicked.connect(self.fetch_weather)
        self.refresh.clicked.connect(self.fetch_weather)
        

    def forecast(self, date, temp_color="#2C2C2A"):
        forecast = QVBoxLayout()
        day = QLabel(date)
        day.setStyleSheet("font-size: 12px; color: #888780")
        day.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon = QLabel("temp")
        icon.setStyleSheet("font-size: 18px")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        temp = QLabel("temp")
        temp.setStyleSheet(f"font-size: 12px; font-weight: 500; color: {temp_color}")
        temp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        forecast.addWidget(day)
        forecast.addSpacing(4)
        forecast.addWidget(icon)
        forecast.addSpacing(4)
        forecast.addWidget(temp)
        return forecast, icon, temp

    def create_card(self, name, font_size="16px", value_color="#2C2C2A"):
        card_widget = QFrame()
        card_widget.setFrameShape(QFrame.Shape.NoFrame)
        card_widget.setFrameShadow(QFrame.Shadow.Plain)
        card_widget.setLineWidth(0)
        card_widget.setStyleSheet("QFrame {background-color: #ffffff; border-radius: 8px; border: 1px solid #D3D1C7} QLabel { border: none; background: transparent; }")
        card_details = QVBoxLayout()
        card_details.setContentsMargins(14, 12, 14, 12)
        card_title = QLabel(name)
        card_title.setStyleSheet("font-size: 11px; color: #888780")
        card_value = QLabel("temp value")
        card_value.setStyleSheet(f"font-size: {font_size}; font-weight: 500; color: {value_color}")
        card_details.addWidget(card_title)
        card_details.addWidget(card_value)
        card_widget.setLayout(card_details)

        return card_widget, card_value
    
    def fetch_weather(self):
        api_key = os.getenv("API_KEY")
        user_input = self.search_bar.text().strip()

        weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=metric&appid={api_key}")
        weather_data = weather.json()
        if weather_data['cod'] != 200:
            print("Error:", weather_data.get("message"))
            return

        self.city_label.setText(f"{weather_data['name']}, {weather_data['sys']['country']}")
        date = datetime.datetime.now()
        self.date_label.setText(date.strftime("%A, %B %d"))

        icon_code = weather_data["weather"][0]["icon"]
        icon_data = requests.get(f"https://openweathermap.org/img/wn/{icon_code}@2x.png")
        pixmap = QPixmap()
        pixmap.loadFromData(icon_data.content)
        pixmap = pixmap.scaled(72, 72, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.icon_label.setPixmap(pixmap)
        if "Clear" in weather_data["weather"][0]["main"]:
           color = "background-color: rgba(255, 204, 0, 1.0)"
        elif "Clouds" in weather_data["weather"][0]["main"]:
            color = "background-color: rgba(149, 165, 166, 1.0)"
        elif "Rain" in weather_data["weather"][0]["main"]:
            color = "background-color: rgba(52, 152, 219, 1.0)"
        elif "Thunderstorm" in weather_data["weather"][0]["main"]:
            color = "background-color: rgba(62, 71, 143, 1.0)"
        elif "Snow" in weather_data["weather"][0]["main"]:
            color = "background-color: rgba(255, 255, 255, 0.9)"
        elif "Drizzle" in weather_data["weather"][0]["main"]:
            color = "background-color: rgba(128, 158, 161, 1.0)"
        elif ["Mist", "Smoke", "Haze", "Dust", "Fog", "Sand", "Ash", "Squall", "Tornado"] in weather_data["weather"][0]["main"]:
            color = "background-color: rgba(236, 240, 241, 0.7)"
        else:
            color = "background-color: rgba(189, 195, 199, 1.0)"    
        self.icon_label.setStyleSheet(f"{color}; border-radius: 36px")     

        self.temp_label.setText(f"{int(weather_data['main']['temp'])}°")
        self.condition_label.setText(weather_data['weather'][0]['description'].title())
        self.feel_value.setText(f"{int(weather_data['main']['feels_like'])}°")
        self.humid_value.setText(f"{weather_data['main']['humidity']}%")
        self.wind_value.setText(f"{round(weather_data['wind']['speed'] * 3.6)} km/h")

        self.pressure_value.setText(f"{weather_data['main']['pressure']} hPa")
        self.visibility_value.setText(f"{round(weather_data['visibility'] / 1000, 1)} km")
        lat = weather_data['coord']['lat']
        lon = weather_data['coord']['lon']
        uv_response = requests.get(f"https://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid={api_key}")
        uv = uv_response.json()
        self.uv_value.setText(f"{self.uv_label(uv['value'])} - {round(uv['value'])}")
        self.sun_value.setText(f"{datetime.datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%I:%M %p')} / {datetime.datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%I:%M %p')}")

        forecast_response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={user_input}&appid={api_key}&units=metric")
        forecast_data = forecast_response.json()
        icons, temps, colors = self.forecast_loader(forecast_data)
        self.sun_icon.setPixmap(icons[0])
        self.sun_icon.setStyleSheet(f"{colors[0]}; border-radius: 20px")
        self.mon_icon.setPixmap(icons[1])
        self.mon_icon.setStyleSheet(f"{colors[1]}; border-radius: 20px")
        self.tue_icon.setPixmap(icons[2])
        self.tue_icon.setStyleSheet(f"{colors[2]}; border-radius: 20px")
        self.wed_icon.setPixmap(icons[3])
        self.wed_icon.setStyleSheet(f"{colors[3]}; border-radius: 20px")
        self.thu_icon.setPixmap(icons[4])
        self.thu_icon.setStyleSheet(f"{colors[4]}; border-radius: 20px")

        self.sun_temp.setText(f"{int(temps[0])}°")
        self.mon_temp.setText(f"{int(temps[1])}°")
        self.tue_temp.setText(f"{int(temps[2])}°")
        self.wed_temp.setText(f"{int(temps[3])}°")
        self.thu_temp.setText(f"{int(temps[4])}°")
        self.updated.setText(f"Last Updated: {datetime.datetime.now().strftime('%I:%M %p')}")

    def forecast_loader(self, data):
        daily_data = defaultdict(list)

        for item in data['list']:
            date = item["dt_txt"].split(" ")[0]
            daily_data[date].append(item)

        icons = []
        temp = []
        colors = []
        for date, entries in daily_data.items():
            for entry in entries:
                if "12:00:00" in entry["dt_txt"]:
                    icon_code = entry["weather"][0]["icon"]

                    icon_data = requests.get(f"https://openweathermap.org/img/wn/{icon_code}@2x.png")
                    pixmap = QPixmap()
                    pixmap.loadFromData(icon_data.content)
                    pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

                    if "Clear" in entry["weather"][0]["main"]:
                       color = "background-color: rgba(255, 204, 0, 1.0)"
                    elif "Clouds" in entry["weather"][0]["main"]:
                        color = "background-color: rgba(149, 165, 166, 1.0)"
                    elif "Rain" in entry["weather"][0]["main"]:
                        color = "background-color: rgba(52, 152, 219, 1.0)"
                    elif "Thunderstorm" in entry["weather"][0]["main"]:
                        color = "background-color: rgba(62, 71, 143, 1.0)"
                    elif "Snow" in entry["weather"][0]["main"]:
                        color = "background-color: rgba(255, 255, 255, 0.9)"
                    elif "Drizzle" in entry["weather"][0]["main"]:
                        color = "background-color: rgba(128, 158, 161, 1.0)"
                    elif ["Mist", "Smoke", "Haze", "Dust", "Fog", "Sand", "Ash", "Squall", "Tornado"] in entry["weather"][0]["main"]:
                        color = "background-color: rgba(236, 240, 241, 0.7)"
                    else:
                        color = "background-color: rgba(189, 195, 199, 1.0)"

                    icons.append(pixmap)
                    temp.append(entry["main"]["temp"])
                    colors.append(color)
                    break
        return icons[:5], temp[:5], colors[:5]

    def uv_label(self, value):
        label = ""
        if value <= 2:
            label = "Low"
        elif value <= 5:
            label = "Moderate"
        elif value <= 7:
            label = "High"
        elif value <= 10:
            label = "Very High"
        else:
            label = "Extreme"

        return label

app = QApplication(sys.argv)
font = app.font()
font.setFamily("Segoe UI")
font.setPointSize(10)
font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
app.setFont(font)
window = MainWindow()
window.show()
app.exec()