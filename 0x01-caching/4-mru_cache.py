#!/usr/bin/python3
""" MRUCache module """
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache class that inherits from BaseCaching """

    def __init__(self):
        """ Initialize MRUCache """
        super().__init__()
        self.order_used = []

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS:
                mru_key = self.order_used.pop()
                del self.cache_data[mru_key]
                print("DISCARD: {}".format(mru_key))
            self.cache_data[key] = item
            self.order_used.append(key)

    def get(self, key):
        """ Get an item by key """
        if key is not None:
            if key in self.order_used:
                self.order_used.remove(key)
                self.order_used.append(key)
            return self.cache_data.get(key)
