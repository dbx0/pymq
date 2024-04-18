from database import DatabaseCache
import logging
import os
logger = logging.getLogger(__name__)

class MessageQueue:

	def __init__(self, db):
		self.db = db
		self.db_cache = DatabaseCache(db, f"""
            with sized as (
				select *, sum(length(content)) over (order by id) as running_bytes
					from messages
					where read = 0
					ORDER BY timestamp asc
				)
			select id, content, sender, recipient, timestamp
			from sized
			where running_bytes < {os.getenv("CACHE_MEMORY_LIMIT")}  * 1024 * 1024;
        """) #this query limits the cache size in memory

	def add_message(self, content, sender, recipient):
		logger.info(f"Adding new message by {sender} to {recipient}: {content}")
		self.db.insert("INSERT INTO messages (content, sender, recipient) VALUES (%s, %s, %s)", (content, sender, recipient))

	def get_next_message(self, recipient):
		logger.info(f"Retrieving last message in queue for {recipient}")
		message = self.db.select("""
			SELECT id, content, sender, recipient, timestamp
			FROM messages
			WHERE read = 0
			AND recipient = %s
			ORDER BY id ASC
			LIMIT 1
		""", (recipient,))

		if message:
			logger.debug(f"Setting message as READ! Message id = {message[0]}")
			self.db.update("UPDATE messages SET read = 1 WHERE id = %s", (message[0],))
			return {
				"id": message[0],
				"content": message[1],
				"sender": message[2],
				"recipient": message[3],
				"timestamp": message[4]
			}
		else:
			return None
		
	def get_next_message_cached(self, recipient):
		logger.info(f"Retrieving last message in queue for {recipient} from cache")

		message = self.db_cache.query("recipient", recipient)

		if message:
			if type(message) == dict:
				message = list(message.values())

			logger.debug(f"Moving message to retrieved_messages: message_id = {message[0]}")
			self.db.update("UPDATE messages SET read = 1 WHERE id = %s", (message[0],))
			return {
				"id": message[0],
				"content": message[1],
				"sender": message[2],
				"recipient": message[3],
				"timestamp": message[4]
			}
		else:
			return None