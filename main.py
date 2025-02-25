import tkinter as tk
import subprocess
from PIL import Image, ImageTk, ImageDraw

def create_rounded_button(canvas, x, y, width, height, radius, text, command):
    """Creates a rounded button on the canvas with hover and click effects."""
    # Store button state
    button_state = {"hover": False, "clicked": False}

    # Function to draw button
    def draw_button(fill_color):
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=fill_color, outline="#311c13", width=2)
        return ImageTk.PhotoImage(img)

    # Default button color
    normal_color = "#64432f"
    hover_color = "#7d5a44"
    click_color = "#503726"

    # Initial button image
    btn_image = draw_button(normal_color)

    # Create button image
    btn = canvas.create_image(x, y, anchor="nw", image=btn_image)
    
    # Store images in a dictionary instead of appending to a shared list
    btn_images = {"normal": btn_image, "hover": draw_button(hover_color), "click": draw_button(click_color)}
    canvas.images.append(btn_images)  # Store reference to prevent garbage collection

    # Create button text
    text_id = canvas.create_text(x + width // 2, y + height // 2, text=text, font=("Arial", 14, "bold"), fill="white")

    # Hover effect
    def on_hover(event):
        if not button_state["clicked"]:
            canvas.itemconfig(btn, image=btn_images["hover"])  # Change to hover image
            canvas.config(cursor="hand2")  # Change cursor to pointer
            button_state["hover"] = True

    # Remove hover effect
    def on_leave(event):
        if not button_state["clicked"]:
            canvas.itemconfig(btn, image=btn_images["normal"])  # Reset to normal image
            canvas.config(cursor="")  # Reset cursor
            button_state["hover"] = False

    # Click effect
    def on_click(event):
        button_state["clicked"] = True
        canvas.itemconfig(btn, image=btn_images["click"])  # Change to click image
        root.after(150, lambda: command())  # Run command after slight delay

    # Bind events
    canvas.tag_bind(btn, "<Enter>", on_hover)
    canvas.tag_bind(text_id, "<Enter>", on_hover)
    canvas.tag_bind(btn, "<Leave>", on_leave)
    canvas.tag_bind(text_id, "<Leave>", on_leave)
    canvas.tag_bind(btn, "<Button-1>", on_click)
    canvas.tag_bind(text_id, "<Button-1>", on_click)

def on_sorting_click():
    """Displays a loading message, waits 3 seconds, then closes the window."""
    loading_x = screen_width // 2   # Change this to adjust horizontally
    loading_y = screen_height - 300  # Change this to adjust vertically

    loading_text = canvas.create_text(loading_x, loading_y, 
                                      text="Loading...", font=("Arial", 24, "bold"), 
                                      fill="white")

    subprocess.Popen(["python", "cv.py"])  # Start cv.py process
    root.after(3000, lambda: (canvas.delete(loading_text), root.destroy()))  # Remove text & close



def on_counting_click():
    print("Counting Process Started!")

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
bg_image = Image.open("images/background.png").resize((screen_width, screen_height))
bg_tk_image = ImageTk.PhotoImage(bg_image)
canvas.create_image(0, 0, anchor="nw", image=bg_tk_image)

# Store images to prevent garbage collection
canvas.images = [bg_tk_image]  # List to hold all images (background + buttons)

# Button size
button_width = 200
button_height = 50
spacing = 100  # Increased gap between buttons

# X Positions (Horizontally Centered)
total_button_width = (2 * button_width) + spacing  # Total width of both buttons + spacing
start_x = (screen_width - total_button_width) // 2  # Start position for first button

# Y Position (Centered)
button_y = screen_height // 2 - (button_height // 2)

# Create "Sorting" button (Left)
create_rounded_button(canvas, x=start_x, y=button_y, width=button_width, height=button_height, radius=20, text="Sorting", command=on_sorting_click)

# Create "Counting" button (Right)
create_rounded_button(canvas, x=start_x + button_width + spacing, y=button_y, width=button_width, height=button_height, radius=20, text="Counting", command=on_counting_click)

# Exit fullscreen on 'Esc'
root.bind("<Escape>", lambda event: root.destroy())

root.mainloop()
