import time

class TimedDictionary():
    def __init__(self):
        self.db = {}
    
    def set(self, key, value, expiry_time=float('inf')):
        if expiry_time != float('inf'):
            expiry_time = time.time() + (expiry_time / 1000)
        self.db[key] = (value, expiry_time)
    
    def get(self, key):
        if key not in self.db:
            return None
        value, expiry_time = self.store[key]
        if expiry_time > time.time():
            return value
        del self.db[key]
            