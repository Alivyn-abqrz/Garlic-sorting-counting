import tkinter as tk
import cv2
import subprocess
from PIL import Image, ImageTk

# Initialize root window
root = tk.Tk()
root.attributes('-fullscreen', True)
root.overrideredirect(True)

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Create canvas for background
canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0, bg="black")
canvas.pack(fill="both", expand=True)

# Load and set background image
bg_image = Image.open("images/Sort-count.png").resize((screen_width, screen_height))
bg_tk_image = ImageTk.PhotoImage(bg_image)
canvas.create_image(0, 0, anchor="nw", image=bg_tk_image)

# Store images to prevent garbage collection
canvas.images = [bg_tk_image]

# Open Camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Camera Feed Dimensions
cam_width, cam_height = 900, 390  # Adjust these values

# Function to update camera feed
def update_camera():
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (cam_width, cam_height))  # Resize frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        # Adjust camera position (x, y)
        cam_x = (screen_width - cam_width) // 2  # Center horizontally
        cam_y = 60  # Move it down by changing this value

        # Display the camera feed
        canvas.create_image(cam_x, cam_y, anchor="nw", image=imgtk)
        canvas.imgtk = imgtk  # Store reference

    canvas.after(10, update_camera)

update_camera()

# Function to go back to main.py
def go_back():
    cap.release()  # Release the camera
    root.after(3000, root.destroy)  # Wait 3 seconds
    subprocess.Popen(["python", "main.py"])  # Reopen main.py

# Create Back Button at the bottom-right corner
button_width = 100
button_height = 40
back_button_x = screen_width - button_width - 50  # 50px padding from right
back_button_y = screen_height - button_height - 50  # 50px padding from bottom

back_button = tk.Button(
    root, text="Back", font=("Arial", 14, "bold"),
    command=go_back, bg="#64432f", fg="white",
    width=10, relief="raised", bd=3, cursor="hand2"
)
back_button.place(x=back_button_x, y=back_button_y)

# Hover effect
def on_hover(event):
    back_button.config(bg="#7d5a44")  # Lighter color on hover

def on_leave(event):
    back_button.config(bg="#64432f")  # Revert to normal color

# Bind hover events
back_button.bind("<Enter>", on_hover)
back_button.bind("<Leave>", on_leave)

# Exit fullscreen on 'Esc'
def close_app(event):
    cap.release()
    root.destroy()

root.bind("<Escape>", close_app)

root.mainloop()