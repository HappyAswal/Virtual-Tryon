import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk
import requests
import io

def get_color_name(rgb):
    
    url = f"https://www.thecolorapi.com/id?rgb=rgb({rgb[0]},{rgb[1]},{rgb[2]})"
    try:
        response = requests.get(url).json()
        return response.get("name", {}).get("value", "Unknown")
    except:
        return "Unknown"

def upload_image():
    
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    image = cv2.imread(file_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    detected_colors = detect_colors(image)
    display_image(image, detected_colors)

def detect_colors(image):
    
    height, width, _ = image.shape
    
    
    upper_center = image[int(0.35 * height), int(width / 2)]  # Middle of upper 70%
    lower_center = image[int(0.85 * height), int(width / 2)]  # Middle of lower 30%
    
    return tuple(upper_center), tuple(lower_center)

def display_image(image, colors):
    """
    Display the image and the detected colors in the GUI.
    """
    img = Image.fromarray(image)
    img.thumbnail((300, 300))
    img_tk = ImageTk.PhotoImage(img)

    canvas.create_image(150, 150, anchor=tk.CENTER, image=img_tk)
    canvas.image = img_tk

    shirt_name = get_color_name(colors[0])
    pants_name = get_color_name(colors[1])

    result_label.config(text=f"Shirt Color: {shirt_name}\nPants Color: {pants_name}")

    shirt_color_display.config(
        bg=f'#{colors[0][0]:02x}{colors[0][1]:02x}{colors[0][2]:02x}'
    )
    pants_color_display.config(
        bg=f'#{colors[1][0]:02x}{colors[1][1]:02x}{colors[1][2]:02x}'
    )

# GUI Setup
root = tk.Tk()
root.title("Shirt & Pants Color Detector")
root.configure(bg="white")

canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()

upload_btn = tk.Button(root, text="Upload Image", command=upload_image)
upload_btn.pack()

result_label = tk.Label(root, text="Shirt Color: N/A\nPants Color: N/A")
result_label.pack()

shirt_color_display = tk.Label(root, text="", width=20, height=2)
shirt_color_display.pack()

pants_color_display = tk.Label(root, text="", width=20, height=2)
pants_color_display.pack()

root.mainloop()