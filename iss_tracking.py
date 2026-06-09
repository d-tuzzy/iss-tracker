import tkinter as tk
from PIL import Image, ImageTk
import requests
import datetime

url = "http://api.open-notify.org/iss-now.json"

# GUI SETUP
root = tk.Tk()
root.title("ISS Tracking")
root.geometry("1280x610")
root.resizable(False, False)

# MAP IMAGE
img = Image.open("world_map.png")  # Opens image file
photo = ImageTk.PhotoImage(img)  # Makes it compatible with Tkinter

image_label = tk.Label(root, image=photo)
image_label.pack()

# WIDGETS FRAME AND LABELS SETUP
widgets_frame = tk.Frame(root)
widgets_frame.place(x=8, y=566)

datetime_label = tk.Label(
    widgets_frame,
    font=("Arial", 14),
    bg="white",
    fg="black",
    padx=10,
    pady=5
)

lat_label = tk.Label(
    widgets_frame,
    font=("Arial", 14),
    bg="white",
    fg="black",
    padx=10,
    pady=5
)

lon_label = tk.Label(
    widgets_frame,
    font=("Arial", 14),
    bg="white",
    fg="black",
    padx=10,
    pady=5
)

datetime_label.grid(row=0, column=0, padx=5) # All labels placed in a row, equally spaced
lat_label.grid(row=0, column=1, padx=5)
lon_label.grid(row=0, column=2, padx=5)

def update():
    try:
        data = requests.get(url).json() # Request from API
        lat = data["iss_position"]["latitude"]
        lon = data["iss_position"]["longitude"]
        time = data["timestamp"]
        utc_time = datetime.datetime.fromtimestamp(time) # Convert from UNIX to UTC time

        datetime_label.config(text=utc_time) # Apply new time to label
        lat_label.config(text=f"Lat: {lat}")
        lon_label.config(text=f"Lon: {lon}")
        print(lat, lon, time, utc_time)

    except:
        datetime_label.config(text="None")
        lat_label.config(text=f"Lat: None")
        lon_label.config(text=f"Lon: None")

    root.after(2000, update)

update()

root.mainloop()

# Testing for test-branch!