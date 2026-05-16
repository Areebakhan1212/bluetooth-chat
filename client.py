import socket
import threading

ip = input("Enter server IP: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connecting...")

client.connect((ip, 6000))

print("Connected to server!")

def receive():
    while True:
        try:
            data = client.recv(1024).decode()
            print("Friend:", data)
        except:
            break

threading.Thread(target=receive, daemon=True).start()

while True:
    msg = input("You: ")
    client.send(msg.encode())