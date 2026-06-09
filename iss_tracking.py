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
img = Image.open("world_map.png") # Opens image file
photo = ImageTk.PhotoImage(img) # Makes it compatible with Tkinter

image_label = tk.Label(root, image=photo)
image_label.pack()

# WIDGETS FRAME
widgets_frame = tk.Frame(root)
widgets_frame.pack()

datetime_label = tk.Label(
    widgets_frame,
    font=("Arial", 14),
    bg="white",
    fg="black",
    padx=10,
    pady=5
)
datetime_label.pack()

coords_label = tk.Label(
    widgets_frame,
    font=("Arial", 14),
    bg="white",
    fg="black",
    padx=10,
    pady=5
)
coords_label.pack()

def update():
    try:
        data = requests.get(url).json()
        lat = data["iss_position"]["latitude"]
        lon = data["iss_position"]["longitude"]
        time = data["timestamp"]
        utc_time = datetime.datetime.fromtimestamp(time)
        datetime_label.config(text=utc_time)

        print(lat, lon, time, utc_time)

    except:
        pass

    root.after(2000, update)

update()

root.mainloop()