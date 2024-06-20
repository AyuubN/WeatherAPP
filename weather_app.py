import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

# Your OpenWeatherMap API key
api_key = '60c6954fdf77069bd9ca0d8c95c829ad'

def get_weather(city):
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={api_key}")
    if weather_data.json()['cod'] == '404':
        date_label.config(text="No City Found", font=('Arial', 20))
        location_label.config(text="")
        temperature_label.config(text="")
        weather_label.config(text="")
        humidity_label.config(text="")
        wind_label.config(text="")
        precipitation_label.config(text="")
        weather_icon_label.config(image='')
    else:
        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])
        humidity = weather_data.json()['main']['humidity']
        wind_speed = weather_data.json()['wind']['speed']
        icon_code = weather_data.json()['weather'][0]['icon']
        
        # Update main weather info
        date_label.config(text="Tuesday\n20 Jun 2022", font=('Arial', 18, 'bold'))
        location_label.config(text=f"{city}", font=('Arial', 14))
        temperature_label.config(text=f"{temp} °C", font=('Arial', 48, 'bold'))
        weather_label.config(text=f"{weather}", font=('Arial', 18))
        
        # Update additional info
        humidity_label.config(text=f"HUMIDITY\n{humidity}%", font=('Arial', 12))
        wind_label.config(text=f"WIND\n{wind_speed} km/h", font=('Arial', 12))
        precipitation_label.config(text="PRECIPITATION\n0%", font=('Arial', 12))
        
        # Fetching the weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_image = Image.open(io.BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_image)
        weather_icon_label.config(image=icon_photo)
        weather_icon_label.image = icon_photo

def fetch_weather():
    city = city_entry.get()
    if city:
        get_weather(city)
    else:
        messagebox.showwarning("Input Error", "Please enter a city name")

# Setting up the GUI
root = tk.Tk()
root.title("Weather App")

# Styling
root.configure(bg='#2F3A48')
root.geometry('400x600')
style = {
    'font': ('Arial', 14),
    'bg': '#2F3A48',
    'fg': 'white',
    'button_bg': '#4CAF50',
    'button_hover_bg': '#45a049'
}

# Creating the input field
city_entry = tk.Entry(root, width=30, font=style['font'], bg='#424242', fg='white', insertbackground='white')
city_entry.pack(pady=20)

# Creating the submit button
submit_button = tk.Button(root, text="Change Location", command=fetch_weather, font=style['font'], bg=style['button_bg'], fg='white')
submit_button.pack(pady=10)

# Creating the frame for weather info
weather_frame = tk.Frame(root, bg=style['bg'])
weather_frame.pack(pady=10, fill='both', expand=True)

# Creating the label to display city and weather info
date_label = tk.Label(weather_frame, text="", bg=style['bg'], fg='white')
date_label.pack(pady=5)
location_label = tk.Label(weather_frame, text="", bg=style['bg'], fg='white')
location_label.pack(pady=5)
temperature_label = tk.Label(weather_frame, text="", bg=style['bg'], fg='white')
temperature_label.pack(pady=10)
weather_label = tk.Label(weather_frame, text="", bg=style['bg'], fg='white')
weather_label.pack(pady=5)

# Creating the label to display weather icon
weather_icon_label = tk.Label(weather_frame, bg=style['bg'])
weather_icon_label.pack(pady=10)

# Creating the frame for additional weather info
info_frame = tk.Frame(root, bg='#212121')
info_frame.pack(pady=20, fill='both', expand=True)

# Creating the label to display additional weather info
humidity_label = tk.Label(info_frame, text="", bg='#212121', fg='white')
humidity_label.pack(side='left', padx=20)
wind_label = tk.Label(info_frame, text="", bg='#212121', fg='white')
wind_label.pack(side='left', padx=20)
precipitation_label = tk.Label(info_frame, text="", bg='#212121', fg='white')
precipitation_label.pack(side='left', padx=20)

# Adding hover effect to the button
def on_enter(e):
    submit_button['bg'] = style['button_hover_bg']

def on_leave(e):
    submit_button['bg'] = style['button_bg']

submit_button.bind("<Enter>", on_enter)
submit_button.bind("<Leave>", on_leave)

# Running the GUI
root.mainloop()
