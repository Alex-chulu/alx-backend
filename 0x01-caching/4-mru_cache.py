#!/usr/bin/env python3
"""MRUCache module"""

from base_caching import BaseCaching
from collections import OrderedDict

class MRUCache(BaseCaching):
    """MRUCache class inherits from BaseCaching and implements a caching system
    using the Most Recently Used (MRU) algorithm.
    """

    def __init__(self):
        """Initialize the MRUCache class"""
        super().__init__()
        self.order = OrderedDict()

    def put(self, key, item):
        """Add an item in the cache using the MRU algorithm.

        Args:
            key: The key of the item to be added.
            item: The item to be added in the cache.

        Returns:
            None
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.order.move_to_end(key)
            else:
                if len(self.cache_data) >= self.MAX_ITEMS:
                    # Discard the most recently used item (MRU)
                    mru_key = next(reversed(self.order))
                    print("DISCARD: {}".format(mru_key))
                    del self.cache_data[mru_key]
                    del self.order[mru_key]
            self.cache_data[key] = item
            self.order[key] = None

    def get(self, key):
        """Get an item by key.

        Args:
            key: The key to retrieve the item from the cache.

        Returns:
            The item corresponding to the key, or None if key is not found.
        """
        if key in self.cache_data:
            self.order.move_to_end(key)
            return self.cache_data[key]
        else:
            return None
