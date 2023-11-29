import tkinter as tk
import pyscreenshot
import pytesseract
from PIL import Image, ImageDraw
import pyperclip
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_and_ocr():
    try:

        # Get the coordinates from the entry fields
        x1 = int(entry_x1.get())
        y1 = int(entry_y1.get())
        x2 = int(entry_x2.get())
        y2 = int(entry_y2.get())
        
        print("Capturing screenshot from (" + str(x1) + ", " + str(y1) + ") to (" + str(x2) + ", " + str(y2) + ")")
        # Capture the screenshot based on entered coordinates
        root.lower()
        screenshot = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
        root.wm_attributes("-topmost", True)

        # Perform OCR using PyTesseract
        text = pytesseract.image_to_string(screenshot)
        pyperclip.copy(text)
        # Display OCR result or do further processing
        print("OCR Result:")
        print(text)
    except ValueError:
        print("Please enter valid integer values for coordinates.")

def show_area():

    # Capture the entire screen
    screenshot = pyscreenshot.grab()

    # Create a drawing object
    draw = ImageDraw.Draw(screenshot)

    # Define the coordinates for the rectangle (left, top, right, bottom)
    x1 = int(entry_x1.get())
    y1 = int(entry_y1.get())
    x2 = int(entry_x2.get())
    y2 = int(entry_y2.get())
    
    # Draw a rectangle on the screenshot
    draw.rectangle((x1, y1, x2, y2), outline="red", width=2)

    # Display the modified screenshot
    screenshot.show()

# Create a tkinter window set its title and size

root = tk.Tk()
root.geometry("175x210")
root.title("Screenshot OCR")
root.wm_attributes("-topmost", True)
# Create entry fields for coordinates
label_x1 = tk.Label(root, text="X1:")
label_x1.pack()
entry_x1 = tk.Entry(root)
entry_x1.pack()

label_y1 = tk.Label(root, text="Y1:")
label_y1.pack()
entry_y1 = tk.Entry(root)
entry_y1.pack()

label_x2 = tk.Label(root, text="X2:")
label_x2.pack()
entry_x2 = tk.Entry(root)
entry_x2.pack()

label_y2 = tk.Label(root, text="Y2:")
label_y2.pack()
entry_y2 = tk.Entry(root)
entry_y2.pack()

# Set default values for coordinates
entry_x1.insert(0, "400")
entry_y1.insert(0, "200")
entry_x2.insert(0, "1800")
entry_y2.insert(0, "800")

# Create buttons for capture and clear fields
capture_button = tk.Button(root, text="Capture and OCR", command=capture_and_ocr)
capture_button.pack()

clear_button = tk.Button(root, text="Show Area", command=show_area)
clear_button.pack()

# Start the GUI
root.mainloop()