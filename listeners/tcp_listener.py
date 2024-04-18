import socket
import json
import logging
logger = logging.getLogger(__name__)
from datetime import datetime

class TCPListener:

    def __init__(self, message_queue, host, port, db):
        self.message_queue = message_queue
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.db = db

    def start(self):
        logger.info(f"TCP listener started on {self.host}:{self.port}")
        while True:
            print("a")
            conn, addr = self.sock.accept()
            logger.info(f"Connection stablished by {addr}")
            self.handle_connection(conn, addr)

    def handle_connection(self, conn, addr):
        try:
            #authentication
            data = conn.recv(1024).decode()

            sender = self.validate_token(data.strip())
            if not sender:
                logger.warn(f"Tentative connection with invalid token by {addr}")
                conn.sendall(b"Invalid token\n")
                conn.close()
                return

            logger.info(f"Authentication successful by {sender}: {addr}")
            conn.sendall(b"Authentication successful\n")

            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break  #client disconnected

                data = data.strip().lower()

                if data == "get_message":
                    logger.info(f"get_message called by {sender}{addr}")
                    
                    cached_message = self.message_queue.get_next_message_cached(sender)

                    if cached_message is None:
                        message = self.message_queue.get_next_message(sender)
                    else:
                        message = cached_message
            
                    if message:
                        #lambda function to convert datetime to str https://stackoverflow.com/a/77540303/4048585
                        conn.sendall(json.dumps(message, default=lambda o: o.__str__() if isinstance(o, datetime) else None).encode() + b"\n")
                    else:
                        conn.sendall(b"No messages available\n")
                elif data.startswith("push_message"):
                    recipient = data.split(' ')[1]

                    logger.info(f"push_message called by {sender}{addr} to {recipient}")
                    conn.sendall(b"Waiting message\n")
                    data = conn.recv(1024).decode()

                    if not data:
                        break

                    if data:
                        message = data.strip()
                        if message:
                            logger.info(f"push_message \"{message}\" by {sender}{addr}")
                            self.message_queue.add_message(message, sender, recipient)
                            conn.sendall(b"Message added to queue\n")
                else:
                    logger.info(f"Invalid command \"{data}\" called by {sender}{addr}")
                    conn.sendall(b"Invalid command\n")

        except ConnectionError:
            logger.error(f"Connection error with {addr}")
            print(f"Connection error with {addr}")

        finally:
            conn.close()

    def validate_token(self, token):
        result = self.db.select("SELECT username FROM valid_tokens WHERE token = %s", (token,))

        return result[0] if result else None