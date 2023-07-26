#!/usr/bin/env python3
"""LFUCache module"""

from base_caching import BaseCaching
from collections import OrderedDict

class LFUCache(BaseCaching):
    """LFUCache class inherits from BaseCaching and implements a caching system
    using the Least Frequently Used (LFU) algorithm.
    """

    def __init__(self):
        """Initialize the LFUCache class"""
        super().__init__()
        self.frequency = {}
        self.lru_order = OrderedDict()

    def put(self, key, item):
        """Add an item in the cache using the LFU algorithm.

        Args:
            key: The key of the item to be added.
            item: The item to be added in the cache.

        Returns:
            None
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.cache_data[key] = item
                self.frequency[key] += 1
                self.lru_order.move_to_end(key)
            else:
                if len(self.cache_data) >= self.MAX_ITEMS:
                    lfu_key = min(self.frequency, key=self.frequency.get)
                    if list(self.frequency.values()).count(self.frequency[lfu_key]) > 1:
                        lru_key = next(iter(self.lru_order))
                        lfu_key = min(self.lru_order, key=self.lru_order.get)
                        if self.frequency[lfu_key] == self.frequency[lru_key]:
                            lfu_key = lru_key
                    print("DISCARD: {}".format(lfu_key))
                    del self.cache_data[lfu_key]
                    del self.frequency[lfu_key]
                    del self.lru_order[lfu_key]
                self.cache_data[key] = item
                self.frequency[key] = 1
                self.lru_order[key] = None

    def get(self, key):
        """Get an item by key.

        Args:
            key: The key to retrieve the item from the cache.

        Returns:
            The item corresponding to the key, or None if key is not found.
        """
        if key in self.cache_data:
            self.frequency[key] += 1
            self.lru_order.move_to_end(key)
            return self.cache_data[key]
        else:
            return None
