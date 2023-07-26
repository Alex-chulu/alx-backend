#!/usr/bin/env python3
"""LIFOCache module"""

from base_caching import BaseCaching

class LIFOCache(BaseCaching):
    """LIFOCache class inherits from BaseCaching and implements a caching system
    using the Last-In-First-Out (LIFO) algorithm.
    """

    def __init__(self):
        """Initialize the LIFOCache class"""
        super().__init__()

    def put(self, key, item):
        """Add an item in the cache using the LIFO algorithm.

        Args:
            key: The key of the item to be added.
            item: The item to be added in the cache.

        Returns:
            None
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS:
                # Discard the last item (LIFO)
                last_key = next(reversed(self.cache_data))
                print("DISCARD: {}".format(last_key))
                del self.cache_data[last_key]
            self.cache_data[key] = item

    def get(self, key):
        """Get an item by key.

        Args:
            key: The key to retrieve the item from the cache.

        Returns:
            The item corresponding to the key, or None if key is not found.
        """
        return self.cache_data.get(key) if key is not None else None
