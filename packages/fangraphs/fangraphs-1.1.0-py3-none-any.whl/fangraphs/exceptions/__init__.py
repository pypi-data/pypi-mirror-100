#! python3
# FanGraphs/exceptions.py

"""
Warning and exceptions
"""


class FilterUpdateIncapability(Warning):
    """
    Raised when the filter queries cannot be updated.
    This usually occurs when no filter queries have been configured since the last update.
    """
    def __init__(self):
        self.message = "No filter query configurations to update"
        super().__init__(self.message)


class InvalidFilterGroup(Exception):
    """
    Raised when an invalid filter group is used.
    """
    def __init__(self, group):
        """
        :param group: The filter group used
        """
        self.group = group
        self.message = f"No filter group names '{self.group}' could be found"
        super().__init__(self.message)


class InvalidFilterQuery(Exception):
    """
    Raised when an invalid filter query is used.
    """
    def __init__(self, query):
        """
        :param query: The filter query used
        """
        self.query = query
        self.message = f"No filter named '{self.query}' could be found"
        super().__init__(self.message)


class InvalidFilterOption(Exception):
    """
    Raised when a filter query is configured to a nonexistend option.
    """
    def __init__(self, option):
        """
        :param option: The option which the filter query was configured to
        """
        self.option = option
        self.message = f"Could not configure to '{self.option}'"
        super().__init__(self.message)


class InvalidQuickSplit(Exception):
    """
    Raised when an invalid quick split is used.
    """
    def __init__(self, quick_split):
        """
        :param quick_split: The quick split used
        """
        self.quick_split = quick_split
        self.message = f"No quick split '{self.quick_split}` could be found"
        super().__init__(self.message)
