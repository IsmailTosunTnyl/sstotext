import tkinter as tk
import socket
import json
import pyperclip

def send_json_data():
    # Get the coordinates from the entry fields or use default values
    x1_val = int(entry_x1.get() or 100)
    y1_val = int(entry_y1.get() or 200)
    x2_val = int(entry_x2.get() or 1800)
    y2_val = int(entry_y2.get() or 800)
    
    # Get the IP address from the entry field or use default 'localhost'
    ip_address = entry_ip.get() or 'localhost'

    # Sample dictionary to send
    data_to_send = {
        'command': 'SS',
        'coordinates': {'x1': x1_val, 'y1': y1_val, 'x2': x2_val, 'y2': y2_val}
    }

    # Convert dictionary to JSON bytes
    json_data = json.dumps(data_to_send).encode()

    try:
        # Create a socket and connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_address, 12345))

        # Send the JSON data
        client_socket.sendall(json_data)

        # Receive echoed data from the server
        received_data = client_socket.recv(8192)
        decoded_data = received_data.decode()

        decoded_dict = json.loads(decoded_data)
        print('Received from server:', decoded_dict)
        pyperclip.copy(decoded_dict['text'])
        # Close the socket
        client_socket.close()
    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running.")

# Create the tkinter window
root = tk.Tk()
root.title("Send JSON Data")

# Entry field for IP address with default value 'localhost'
label_ip = tk.Label(root, text="Server IP Address:")
label_ip.pack()
entry_ip = tk.Entry(root)
entry_ip.insert(0, "localhost")  # Default value for IP address
entry_ip.pack()

# Entry fields for coordinates with default values
label_x1 = tk.Label(root, text="X1:")
label_x1.pack()
entry_x1 = tk.Entry(root)
entry_x1.insert(0, "100")  # Default value for x1
entry_x1.pack()

label_y1 = tk.Label(root, text="Y1:")
label_y1.pack()
entry_y1 = tk.Entry(root)
entry_y1.insert(0, "200")  # Default value for y1
entry_y1.pack()

label_x2 = tk.Label(root, text="X2:")
label_x2.pack()
entry_x2 = tk.Entry(root)
entry_x2.insert(0, "1800")  # Default value for x2
entry_x2.pack()

label_y2 = tk.Label(root, text="Y2:")
label_y2.pack()
entry_y2 = tk.Entry(root)
entry_y2.insert(0, "800")  # Default value for y2
entry_y2.pack()

# Function to trigger when the button is clicked
def button_click():
    send_json_data()

# Create a button in the window
send_button = tk.Button(root, text="Get Data", command=button_click)
send_button.pack()

# Start the GUI
root.geometry("180x250")
root.mainloop()
