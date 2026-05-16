import tkinter as tk
from tkinter import filedialog
import socket
import threading
from datetime import datetime

# ---------------- CONNECTION ----------------

mode = input("server or client: ")
PORT = 6003

if mode == "server":

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", PORT))
    server.listen(1)

    print("Waiting for connection...")
    conn, addr = server.accept()

    sock = conn
    print("Connected!")

else:

    ip = input("Enter server IP: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, PORT))

    sock = client
    print("Connected!")

# ---------------- GUI ----------------

window = tk.Tk()
window.title("Bluetooth Chat")
window.geometry("500x600")

chat_box = tk.Text(window, height=25, width=55)
chat_box.pack(pady=10)

entry = tk.Entry(window, width=35)
entry.pack(side=tk.LEFT, padx=10, pady=10)

# ---------------- SEND MESSAGE ----------------

def send_message():

    msg = entry.get()

    if msg == "":
        return

    time = datetime.now().strftime("%H:%M")

    chat_box.insert(tk.END, f"You ({time}): {msg}\n")
    chat_box.see(tk.END)

    sock.send(("TEXT:" + msg).encode())
    entry.delete(0, tk.END)

# ---------------- RECEIVE MESSAGE ----------------

def receive_messages():

    while True:
        try:
            data = sock.recv(4096)

            # DELIVERY RECEIPT
            if data == b"DELIVERED":
                chat_box.insert(tk.END, "✔ Message Delivered\n")
                chat_box.see(tk.END)
                continue

            text = data.decode(errors="ignore")

            # TEXT MESSAGE
            if text.startswith("TEXT:"):

                msg = text[5:]
                time = datetime.now().strftime("%H:%M")

                chat_box.insert(
                    tk.END,
                    f"Friend ({time}): {msg}\n"
                )

                chat_box.see(tk.END)

                sock.send(b"DELIVERED")
                continue

            # FILE MESSAGE
            if text.startswith("FILE:"):

                file_data = data[5:]

                with open("received_file", "wb") as f:
                    f.write(file_data)

                chat_box.insert(tk.END, "📁 File Received\n")
                chat_box.see(tk.END)
                continue

        except:
            break

# ---------------- SEND FILE ----------------

def send_file():

    file_path = filedialog.askopenfilename()

    if file_path == "":
        return

    file = open(file_path, "rb")
    data = file.read()

    sock.send(b"FILE:" + data)

    file.close()

    time = datetime.now().strftime("%H:%M")

    chat_box.insert(tk.END, f"You sent a file ({time})\n")
    chat_box.see(tk.END)

# ---------------- THREAD ----------------

threading.Thread(target=receive_messages, daemon=True).start()

# ---------------- BUTTONS ----------------

send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT, padx=5)

file_button = tk.Button(window, text="Attach File", command=send_file)
file_button.pack(side=tk.RIGHT, padx=5)

# ---------------- START ----------------

window.mainloop()