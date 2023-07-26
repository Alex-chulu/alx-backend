#!/usr/bin/env python3
"""FIFOCache module"""

from base_caching import BaseCaching

class FIFOCache(BaseCaching):
    """FIFOCache class inherits from BaseCaching and implements a caching system
    using the First-In-First-Out (FIFO) algorithm.
    """

    def __init__(self):
        """Initialize the FIFOCache class"""
        super().__init__()

    def put(self, key, item):
        """Add an item in the cache using the FIFO algorithm.

        Args:
            key: The key of the item to be added.
            item: The item to be added in the cache.

        Returns:
            None
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS:
                # Discard the first item (FIFO)
                first_key = next(iter(self.cache_data))
                print("DISCARD: {}".format(first_key))
                del self.cache_data[first_key]
            self.cache_data[key] = item

    def get(self, key):
        """Get an item by key.

        Args:
            key: The key to retrieve the item from the cache.

        Returns:
            The item corresponding to the key, or None if key is not found.
        """
        return self.cache_data.get(key) if key is not None else None
