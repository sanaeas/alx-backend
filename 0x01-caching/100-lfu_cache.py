#!/usr/bin/python3
""" LFUCache module """
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache class that inherits from BaseCaching """
    def __init__(self):
        """ Initialize LFUCache """
        super().__init__()
        self.frequency = {}

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.frequency[key] += 1
            else:
                self.frequency[key] = 1

            if len(self.cache_data) >= self.MAX_ITEMS:
                lfu_keys = [k for k, v in self.frequency.items() if v == min(self.frequency.values())]
                
                if len(lfu_keys) > 1:
                    lru_key = min(self.cache_data, key=lambda k: self.cache_data[k])
                    lfu_keys = [lru_key]

                for lfu_key in lfu_keys:
                    del self.cache_data[lfu_key]
                    del self.frequency[lfu_key]
                    print("DISCARD: {}".format(lfu_key))

            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key """
        if key is not None:
            if key in self.cache_data:
                self.frequency[key] += 1
                return self.cache_data[key]
        return None
