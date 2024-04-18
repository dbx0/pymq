from threading import Timer
import time
import os

class DatabaseCache:
    def __init__(self, db, update_query):
        self.cache = []
        self.cache_update_time = time.time()
        self.update_interval = int(os.getenv("CACHE_UPDATE_INTERVAL"))
        self.db = db
        self.update_query = update_query
        self.update_cache()

    def update_cache(self):
        new_data = self.db.select_all_dict(self.update_query)

        self.cache = new_data
        self.cache_update_time = time.time()

        #schedule next update after update_interval seconds
        timer = Timer(self.update_interval, self.update_cache)
        timer.start()

    def get_data(self):
        #check if cache is empty or timed out
        current_time = time.time()
        if not self.cache or (current_time - self.cache_update_time) > self.update_interval:
            self.update_cache()
        return self.cache

    def query(self, key, value):
        if self.cache is None:
            return None
        for i, item in enumerate(self.cache):
            if item.get(key) == value:
                del self.cache[i]
                return item
        if not hasattr(self, 'update_timer') or not self.update_timer.is_alive():
            self.update_cache()
        return None