#!/usr/bin/env python3
"""Copy index_range from the previous task and the following class into your code"""
import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> tuple:
    """
    Calculate the start and end index for a given page and page size.

    Args:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        tuple: A tuple containing the start index and end index.
    """
    if page <= 0 or page_size <= 0:
        raise ValueError("Page and page_size must be positive integers.")

    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Get the paginated data from the dataset.

        Args:
            page (int): The page number (1-indexed). Default is 1.
            page_size (int): The number of items per page. Default is 10.

        Returns:
            List[List]: The paginated data as a list of rows.
        """
        assert isinstance(page, int) and page > 0, "Page must be a positive integer."
        assert isinstance(page_size, int) and page_size > 0, "Page_size must be a positive integer."

        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()

        if start_index >= len(dataset) or start_index < 0:
            return []

        return dataset[start_index:end_index]
