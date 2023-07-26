#!/usr/bin/env python3
""" BasicCache module
"""

from base_caching import BaseCaching

class BasicCache(BaseCaching):
    """ BasicCache class inherits from BaseCaching and implements a caching system
    without a limit on the number of items.
    """

    def put(self, key, item):
        """ Add an item in the cache.

        Args:
            key: The key of the item to be added.
            item: The item to be added in the cache.

        Returns:
            None
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key.

        Args:
            key: The key to retrieve the item from the cache.

        Returns:
            The item corresponding to the key, or None if key is not found.
        """
        return self.cache_data.get(key) if key is not None else None
