import socket
import json

# Replace with listener hostname, port, and secret token
HOST = "localhost"
PORT = 8080
SECRET_TOKEN = "<your token>"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    # Send authentication token
    sock.sendall(SECRET_TOKEN.encode() + b"\n")
    data = sock.recv(1024).decode()

    if data != "Authentication successful\n":
        print("Authentication failed")
        exit()

    while True:
        # Request a message
        sock.sendall(b"get_message\n")
        data = sock.recv(1024).decode()

        if data == "No messages available\n":
            print("No messages in queue")
            break

        # Parse JSON response (assuming listener sends message in JSON format)
        message = json.loads(data[:-1])
        print(f"Received message: {message}")