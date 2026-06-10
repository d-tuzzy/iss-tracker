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


# WIDGETS FRAME AND LABELS SETUP
widgets_frame = tk.Frame(root)
widgets_frame.place(x=8, y=566)

utctime_label = tk.Label(
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

utctime_label.grid(row=0, column=0, padx=5) # All labels placed in a row, equally spaced
lat_label.grid(row=0, column=1, padx=5)
lon_label.grid(row=0, column=2, padx=5)


# MAP AND DOT SETUP
img = Image.open("world_map.png")  # Opens image file
photo = ImageTk.PhotoImage(img)  # Makes it compatible with Tkinter

canvas = tk.Canvas(root, width=1280, height=555) # Canvas that dot can move in
canvas.create_image(0, 0, image=photo, anchor="nw")
canvas.pack()


def find_position(pLat, pLon): # Turn coordinates into discrete pixel values
    x = ((pLon + 180) / 360) * 1280
    y = ((90 - pLat) / 180) * 555
    return int(x), int(y)


previous_position = [None, None] # Previous pixel coordinates of dot (where it is on the screen now)

def update():
    global previous_position

    try:
        data = requests.get(url).json() # Request from API
        lat = float(data["iss_position"]["latitude"])
        lon = float(data["iss_position"]["longitude"])
        time = data["timestamp"]
        utc_time = datetime.datetime.fromtimestamp(time) # Convert from UNIX to UTC time

        utctime_label.config(text=utc_time) # Apply new time to label
        lat_label.config(text=f"Lat: {lat}")
        lon_label.config(text=f"Lon: {lon}")

        dot_coords = find_position(lat, lon)
        dot_x = dot_coords[0]
        dot_y = dot_coords[1]

        if (dot_x != previous_position[0]) or (dot_y != previous_position[1]): # Only draw if new pixel coordinates are different
            dot = canvas.create_oval(dot_x, dot_y, dot_x+6, dot_y+6, fill="red")

        previous_position[0] = dot_x # Can be compared with next iteration's coordinates
        previous_position[1] = dot_y
   
    except Exception as e:
        utctime_label.config(text="None")
        lat_label.config(text=f"Lat: None")
        lon_label.config(text=f"Lon: None")
        print(e)

    root.after(2000, update) # 2 second delay

update()

root.mainloop()