"""KD Tree Node class
"""
class Node2D():
    """KD-Tree Node"""
    def __init__(self, data, left = None, right=None):
        self._left = left
        self._right = right
        self._data = data  # cell position (lat, lon, cell_index)

    def __str__(self):
        """Pretty-print the node data"""
        return f'({self._data})'

    def __repr__(self):
        """Define the repr string."""
        return f'(Node2D, \'{self._data}\', left={self._left}, right={self._right})'

    @property
    def data(self):
        """Return the data of the current node"""
        return self._data

    @property
    def left(self):
        """Return the left node"""
        return self._left

    @property
    def right(self):
        """Return the right node"""
        return self._right
