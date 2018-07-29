# -*- coding: UTF-8 -*-

import sys

from networkx import __version__ as nxv

from .abstract_graph_edit_dist import AbstractGraphEditDistance
from .edge_edit_dist import EdgeEditDistance
from .edge_graph import EdgeGraph


def _get_edges(graph, node):
    if float(nxv) < 2:
        return list(graph.edge[node].keys())

    return list(graph.edges(node))


class GraphEditDistance(AbstractGraphEditDistance):

    def insert_cost(self, i, j):
        if i == j:
            return 1
        return sys.maxsize

    def delete_cost(self, i, j):
        if i == j:
            return 1
        return sys.maxsize

    def substitute_cost(self, node_1, node_2):
        return self._relabel_cost(node_1, node_2) + self._edge_diff(node_1, node_2)

    @staticmethod
    def _relabel_cost(node_1, node_2):
        if node_1 == node_2:
            return 0.
        return 1.

    def _edge_diff(self, node_1, node_2):
        edges_1 = _get_edges(self.g, node_1)
        edges_2 = _get_edges(self.h, node_2)

        if len(edges_1) == 0 or len(edges_2) == 0:
            return max(len(edges_1), len(edges_2))

        edge_graph_1 = EdgeGraph(node_1, edges_1)
        edge_graph_2 = EdgeGraph(node_2, edges_2)

        return EdgeEditDistance.compare(edge_graph_1, edge_graph_2)
