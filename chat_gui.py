import tkinter as tk
from tkinter import filedialog
import socket
import threading
from datetime import datetime

# ---------------- CONNECTION ----------------

mode = input("server or client: ")

PORT = 6000

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

    chat_box.insert(
        tk.END,
        "You (" + time + "): " + msg + "\n"
    )

    chat_box.see(tk.END)

    sock.send(msg.encode())

    entry.delete(0, tk.END)

# ---------------- RECEIVE MESSAGE ----------------

def receive_messages():

    while True:

        try:

            data = sock.recv(1024).decode()

            time = datetime.now().strftime("%H:%M")

            chat_box.insert(
                tk.END,
                "Friend (" + time + "): " + data + "\n"
            )

            chat_box.see(tk.END)

        except:
            break

# ---------------- SEND FILE ----------------

def send_file():

    file_path = filedialog.askopenfilename()

    if file_path == "":
        return

    file = open(file_path, "rb")

    data = file.read()

    sock.send(data)

    file.close()

    chat_box.insert(
        tk.END,
        "You sent a file\n"
    )

    chat_box.see(tk.END)

# ---------------- THREAD ----------------

threading.Thread(
    target=receive_messages,
    daemon=True
).start()

# ---------------- BUTTONS ----------------

send_button = tk.Button(
    window,
    text="Send",
    command=send_message
)

send_button.pack(side=tk.RIGHT, padx=5)

file_button = tk.Button(
    window,
    text="Attach File",
    command=send_file
)

file_button.pack(side=tk.RIGHT, padx=5)

# ---------------- START GUI ----------------

window.mainloop()