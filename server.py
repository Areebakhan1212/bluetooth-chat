import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("0.0.0.0", 6000))

server.listen(1)

print("Waiting for connection...")

conn, addr = server.accept()

print("Connected:", addr)

def receive():
    while True:
        try:
            data = conn.recv(1024).decode()
            print("Friend:", data)
        except:
            break

threading.Thread(target=receive, daemon=True).start()

while True:
    msg = input("You: ")
    conn.send(msg.encode())