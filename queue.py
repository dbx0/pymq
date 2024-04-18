import logging
import os

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("queue.log"),
        logging.StreamHandler()
    ]
)

from messages import MessageQueue
from listeners import TCPListener
from database import Database

from dotenv import load_dotenv
load_dotenv('.env')

HOST = os.getenv("QUEUE_HOST")
PORT = int(os.getenv("QUEUE_PORT"))

if __name__ == "__main__":

    db = Database()
    
    message_queue = MessageQueue(db)

    logger.info(f"Starting message queue at {HOST}:{PORT}")
    listener = TCPListener(message_queue, HOST, PORT, db)
    listener.start()
