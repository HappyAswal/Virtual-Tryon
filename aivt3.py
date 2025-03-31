import cv2
import requests
import tkinter as tk
from tkinter import filedialog, messagebox, DISABLED, NORMAL
from PIL import Image, ImageTk
import os

# Background removal API key (Replace with your actual key)
API_KEY = "CH7P3e23E7TiUhD9fYLVHKXF"  
API_URL = "https://api.remove.bg/v1.0/removebg"

# Function to capture an image using a webcam
def capture_image():
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        cv2.imshow("Press 'Space' to capture, 'Esc' to exit", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # Spacebar to capture
            image_path = "user_image.jpg"
            cv2.imwrite(image_path, frame)
            break
        elif key == 27:  # ESC to exit
            cam.release()
            cv2.destroyAllWindows()
            return None

    cam.release()
    cv2.destroyAllWindows()
    return image_path

# Function to upload an image from the device
def upload_image():
    file_path = filedialog.askopenfilename(title="Select Image",
                                           filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    return file_path

# Function to remove background using the API
def remove_bg(image_path):
    with open(image_path, "rb") as img_file:
        headers = {"x-api-key": API_KEY}
        files = {"image_file": img_file}
        response = requests.post(API_URL, headers=headers, files=files)

        if response.status_code == 200 and response.headers["Content-Type"].startswith("image"):
            output_path = "no_bg_" + os.path.basename(image_path)
            with open(output_path, "wb") as out_file:
                out_file.write(response.content)
            return output_path
        else:
            messagebox.showerror("Error", "Background removal failed")
            return None

# Function to overlay clothing onto the person’s image
def overlay_images(person_img, clothes_img):
    global final_output_path
    person = Image.open(person_img).convert("RGBA")
    clothes = Image.open(clothes_img).convert("RGBA")

    # Resize clothing to fit the person's body (adjust manually if needed)
    clothes = clothes.resize((person.width, int(person.height / 2)))

    # Paste clothing onto the lower half of the person's image
    person.paste(clothes, (0, person.height // 2), clothes)
    final_output_path = "final_output.png"
    person.save(final_output_path)
    messagebox.showinfo("Success", f"Final image saved as {final_output_path}")

# Function to display the final result
def show_result():
    if os.path.exists(final_output_path):
        img = Image.open(final_output_path)
        img.show()
    else:
        messagebox.showerror("Error", "No result image found!")

# GUI Interface
def main():
    root = tk.Tk()
    root.title("Virtual Try-On")
    root.geometry("400x350")
    root.configure(bg="#f0f0f0")

    title_label = tk.Label(root, text="Virtual Try-On", font=("Arial", 16, "bold"), bg="#f0f0f0")
    title_label.pack(pady=10)

    button_style = {"font": ("Arial", 12), "padx": 10, "pady": 5, "width": 20, "bg": "#4CAF50", "fg": "white"}
    
    def update_buttons():
        if person_image:
            upload_btn.config(state=DISABLED, bg="#a0a0a0")
            capture_btn.config(state=DISABLED, bg="#a0a0a0")
        else:
            upload_btn.config(state=NORMAL, bg="#4CAF50")
            capture_btn.config(state=NORMAL, bg="#4CAF50")
    
    def select_person_image():
        global person_image
        person_image = upload_image()
        if person_image:
            messagebox.showinfo("Success", "User image selected successfully!")
            update_buttons()
    
    def capture_person_image():
        global person_image
        person_image = capture_image()
        if person_image:
            messagebox.showinfo("Success", "Image captured successfully!")
            update_buttons()
    
    def process_images():
        if not person_image:
            messagebox.showerror("Error", "Please select or capture your image first!")
            return
        
        clothes_image = upload_image()
        if clothes_image:
            clothes_no_bg = remove_bg(clothes_image)
            if clothes_no_bg:
                overlay_images(person_image, clothes_no_bg)
    
    upload_btn = tk.Button(root, text="Upload Your Image", command=select_person_image, **button_style)
    upload_btn.pack(pady=5)
    
    capture_btn = tk.Button(root, text="Capture Image", command=capture_person_image, **button_style)
    capture_btn.pack(pady=5)
    
    tk.Button(root, text="Upload Clothing Image", command=process_images, **button_style).pack(pady=5)
    tk.Button(root, text="Show Result", command=show_result, **button_style).pack(pady=5)
    tk.Button(root, text="Exit", command=root.quit, **{**button_style, "bg": "#d9534f"}).pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    person_image = None
    final_output_path = "final_output.png"
    main()
