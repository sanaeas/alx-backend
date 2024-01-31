#!/usr/bin/python3
""" LFUCache module """
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache class that inherits from BaseCaching """
    def __init__(self):
        """ Initialize LFUCache """
        super().__init__()
        self.cache_data = {}
        self.key_frequencies = []

    def __reorder(self, mru_key):
        """ Reorder the items by the most used """
        max_pos = []
        mru_freq = 0
        mru_pos = 0
        ins_pos = 0

        for i, key_freq in enumerate(self.key_frequencies):
            if key_freq[0] == mru_key:
                mru_freq = key_freq[1] + 1
                mru_pos = i
                break
            elif len(max_pos) == 0:
                max_pos.append(i)
            elif key_freq[1] < self.key_frequencies[max_pos[-1]][1]:
                max_pos.append(i)
        max_pos.reverse()
        for pos in max_pos:
            if self.key_frequencies[pos][1] > mru_freq:
                break
            ins_pos = pos

        self.key_frequencies.pop(mru_pos)
        self.key_frequencies.insert(ins_pos, [mru_key, mru_freq])

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if key not in self.cache_data:
                if len(self.cache_data) >= self.MAX_ITEMS:
                    lfu_key, _ = self.key_frequencies[-1]
                    self.cache_data.pop(lfu_key)
                    self.key_frequencies.pop()
                    print("DISCARD:", lfu_key)
                self.cache_data[key] = item
                ins_index = len(self.key_frequencies)
                for i, key_freq in enumerate(self.key_frequencies):
                    if key_freq[1] == 0:
                        ins_index = i
                        break
                self.key_frequencies.insert(ins_index, [key, 0])
            else:
                self.cache_data[key] = item
                self.__reorder(key)

    def get(self, key):
        """ Get an item by key """
        if key is not None:
            if key in self.cache_data:
                self.__reorder(key)

        return self.cache_data.get(key)
