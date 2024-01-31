#!/usr/bin/python3
""" LRUCache module """
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache class that inherits from BaseCaching """

    def __init__(self):
        """ Initialize LRUCache """
        super().__init__()
        self.order_used = []

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS:
                lru_key = self.order_used.pop(0)
                del self.cache_data[lru_key]
                print("DISCARD: {}".format(lru_key))
            self.cache_data[key] = item
            self.order_used.append(key)

    def get(self, key):
        """ Get an item by key """
        if key is not None:
            if key in self.order_used:
                self.order_used.remove(key)
                self.order_used.append(key)
            return self.cache_data.get(key)
