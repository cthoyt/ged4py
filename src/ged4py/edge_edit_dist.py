# -*- coding: UTF-8 -*-

import sys

from .abstract_graph_edit_dist import AbstractGraphEditDistance


class EdgeEditDistance(AbstractGraphEditDistance):
    """Calculates the graph edit distance between two edges.

    A node in this context is interpreted as a graph,
    and edges are interpreted as nodes.
    """

    def insert_cost(self, i, j):
        if i == j:
            return 1
        return sys.maxsize

    def delete_cost(self, i, j):
        if i == j:
            return 1
        return sys.maxsize

    def substitute_cost(self, edge1, edge2):
        if edge1 == edge2:
            return 0.
        return 1
