#!/usr/bin/python3
""" FIFOCache module """
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache class that inherits from BaseCaching """
    def __init__(self):
        """ Initialize FIFOCache """
        super().__init__()
        self.item_queue = list()

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if key not in self.cache_data:
                if len(self.cache_data) >= self.MAX_ITEMS:
                    discarded_key = self.item_queue.pop()
                    del self.cache_data[discarded_key]
                    print("DISCARD: {}".format(discarded_key))
                self.item_queue.insert(0, key)

            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key """
        if key is not None:
            return self.cache_data.get(key)
