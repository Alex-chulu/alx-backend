#!/usr/bin/env python3
""" Pagination function """

from typing import Tuple

def index_range(page: int, page_size: int) -> tuple[int, int]:
    """
    Calculate the start and end index for a given page and page size.

    Args:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        tuple: A tuple containing the start index and end index.
    """
    return ((page - 1) * page_size, page * page_size)

