import time

class TimedDictionary():
    def __init__(self):
        self.db = {}
    
    def set(self, key, value, expiry_ms):
        expiry_time = time.time() + (expiry_ms / 1000)
        self.db[key] = (value, expiry_time)
    
    def get(self, key):
        if key not in self.db:
            return None
        value, expiry_time = self.db[key]
        if expiry_time > time.time():
            return value
        del self.db[key]
            