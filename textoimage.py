import tkinter as tk
import pyscreenshot
import pytesseract
from PIL import ImageDraw
import pyperclip
from threading import Thread

import socket
import json

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# define a thread for remote control






def capture_and_ocr(coordinates=None):
    try:

        if coordinates is not None:
            # Get the coordinates from the entry fields
            x1 = int(coordinates['x1'])
            y1 = int(coordinates['y1'])
            x2 = int(coordinates['x2'])
            y2 = int(coordinates['y2'])
            
            # set the entry fields to the coordinates
            entry_x1.delete(0, tk.END)
            entry_x1.insert(0, x1)
            entry_y1.delete(0, tk.END)
            entry_y1.insert(0, y1)
            entry_x2.delete(0, tk.END)
            entry_x2.insert(0, x2)
            entry_y2.delete(0, tk.END)
            entry_y2.insert(0, y2)
        else:
            
            
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
        return text
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



def remote_control():
    server_socket.listen(5)
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} has been established!")
        received_data = client_socket.recv(8192 )
        decoded_data = received_data.decode()

        # Convert the received JSON data to a dictionary
        received_dict = json.loads(decoded_data)
        print('Received from client:', received_dict)

        received_dict['status'] = 'success'
        received_dict['text'] = capture_and_ocr(received_dict['coordinates'])
        # Send the received data back to the client
        client_socket.sendall(json.dumps(received_dict).encode())       
        # Close the client socket after sending data back
        client_socket.close()


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
t1 = Thread(target=remote_control)
t1.start()
# Start the GUI
root.mainloop()

# Close the socket
server_socket.close()
t1.join()