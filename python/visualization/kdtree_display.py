#!/usr/bin/env python
"""Print the KD-tree 
"""
from typing import List
from grid_filter import KDTree2D

class KDTreeDisplay():
    """A class to create a text representation of a KD-Tree
    """
    def __init__(self, kd2: KDTree2D):
        self.kd2 = kd2
        self.root = self.kd2.root
        self._tree_list = []
        #self.bfs()

    def bfs(self):
        """Perform a breadth first traversal of the tree"""
        node_queue = []
        node_queue.append(self.root)
        # Note: pop(0) from list is O(n), length of queue
        # a different data structure may be required for very large trees
        while len(node_queue) > 0:
            if node_queue[0].left is not None:
                node_queue.append(node_queue[0].left)
            if node_queue[0].right is not None:
                node_queue.append(node_queue[0].right)
            self._tree_list.append(node_queue[0])
            node_queue.pop(0)

    def _find_path(self, node, path, node_number: int):
        """Print the path up to a node value"""
        path.append(node)
        if node.data[2] == node_number:
            for i, p in enumerate(path):
                #print(f'{len(path)}: {path}')
                print(f'{i} -> {p}')
            return path
        else:
            if node.left is not None:
                self._find_path(node.left, path, node_number)
            if node.right is not None:
                self._find_path(node.right, path, node_number)
            path.pop(-1)

    def find_path(self, node_number: int):
        """call _find_path with starting with root node"""
        path_to_node = []
        self._find_path(self.root, path_to_node, node_number)
        #print("<<find_path>>", path_to_node)
        return path_to_node

    @property
    def tree_list(self)->List[int]:
        """Return the node list of the kd_tree"""
        return self._tree_list

