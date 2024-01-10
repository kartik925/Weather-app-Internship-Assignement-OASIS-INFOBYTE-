import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OASIS INFOBYTE WEATHER APPLICATION")
        self.root.geometry("400x400")

        self.api_key = "227c04b2874ea352703e46b0786d03b6"
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

        self.temperature_units = ["metric", "imperial"]
        self.selected_unit = tk.StringVar(value="metric")

        self.create_gui()

    def get_weather_data(self):
        city = self.city_entry.get()
        if not city:
            self.display_error("Please enter a city.")
            return

        params = {
            "q": city,
            "appid": self.api_key,
            "units": self.selected_unit.get(),
        }

        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()  # Parsing JSON data here

            if response.status_code == 200:
                self.display_weather_data(data)
            else:
                self.display_error(data["message"])
        except Exception as e:
            self.display_error(f"Error fetching data: {e}")

    def display_weather_data(self, data):
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]

        unit_label = "°C" if self.selected_unit.get() == "metric" else "°F"
        result_text = f"Temperature: {temperature}{unit_label}\nDescription: {description}\nWind Speed: {wind_speed} m/s"
        self.result_label.config(text=result_text)

        # Display weather icon
        icon_id = data["weather"][0]["icon"]
        self.display_weather_icon(icon_id)

    def display_weather_icon(self, icon_id):
        icon_url = f"http://openweathermap.org/img/wn/{icon_id}.png"
        icon_image = Image.open(requests.get(icon_url, stream=True).raw)
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.icon_label.config(image=icon_photo)
        self.icon_label.image = icon_photo  # Keep a reference to avoid garbage collection

    def display_error(self, message):
        self.result_label.config(text=f"Error: {message}")

    def create_gui(self):
        self.root.configure(bg="#3498db")  # Set background color

        frame = ttk.Frame(self.root, padding="20", style="TFrame")
        frame.grid(row=0, column=0, sticky="wens")

        # Title Section
        title_label = ttk.Label(frame, text="OASIS INFOBYTE WEATHER APPLICATION", font=("Arial", 18, "bold"), style="TLabel")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Input Section
        ttk.Label(frame, text="Enter City:", style="TLabel").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.city_entry = ttk.Entry(frame, width=20)
        self.city_entry.grid(row=1, column=1, sticky=tk.W, pady=(0, 5))

        ttk.Label(frame, text="Select Unit:", style="TLabel").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        unit_dropdown = ttk.Combobox(frame, textvariable=self.selected_unit, values=self.temperature_units)
        unit_dropdown.grid(row=2, column=1, sticky=tk.W, pady=(0, 5))

        get_weather_button = ttk.Button(frame, text="Get Weather", command=self.get_weather_data, style="TButton")
        get_weather_button.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        # Result Section
        self.result_label = ttk.Label(frame, text="", style="TLabel")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=(10, 0))

        # Icon Section
        self.icon_label = ttk.Label(frame, image=None, style="TLabel")
        self.icon_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))

        # Configure styles
        ttk.Style().configure("TLabel", background="#3498db", foreground="white")
        ttk.Style().configure("TButton", padding=10, relief="flat", background="#2ecc71", foreground="white")
        ttk.Style().configure("TFrame", background="#3498db")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
