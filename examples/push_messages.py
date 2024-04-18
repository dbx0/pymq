import socket
import json

# Replace with listener hostname, port, and secret token
HOST = "localhost"
PORT = 8080
SECRET_TOKEN = "<your token>"
RECIPIENT = "another_client"
MESSAGE = {"type": "text_message", "submitter": "example_code", "data": {"message": "hello world", "planet": "earth"}}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    # Send authentication token
    sock.sendall(SECRET_TOKEN.encode() + b"\n")
    data = sock.recv(1024).decode()

    print(data)
    if data != "Authentication successful\n":
        print("Authentication failed")
        exit()

    command = f"push_message {RECIPIENT}"
    sock.sendall(command.encode() + b"\n")
    data = sock.recv(1024).decode()

    if data == "Waiting message\n":
        message = json.dumps(MESSAGE)
        sock.sendall(message.encode() + b"\n")

    data = sock.recv(1024).decode()

    if data == "Message added to queue\n":
        print("Message added to queue")

