# -*- coding: UTF-8 -*-

from __future__ import print_function

from abc import ABC, abstractmethod

import numpy as np
from networkx import __version__ as nxv
from scipy.optimize import linear_sum_assignment


def _get_nodes(graph):
    if float(nxv) < 2:
        return graph.nodes()

    return list(graph.nodes())


class AbstractGraphEditDistance(ABC):
    def __init__(self, g, h):
        self.g = g
        self.h = h

        self.cost_matrix = self._create_cost_matrix()
        self.edit_costs = self._calculate_edit_costs()
        self.distance = sum(self.edit_costs)

    def normalized_distance(self):
        """Return the graph edit distance between graph g1 & g2.

        The distance is normalized on the size of the two graphs.
        This is done to avoid favorisation towards smaller graphs
        """
        return self.distance * 2 / (len(self.g) + len(self.h))

    def _calculate_edit_costs(self):
        row_ind, col_ind = linear_sum_assignment(self.cost_matrix)
        return [
            self.cost_matrix[i][j]
            for i, j in zip(row_ind, col_ind)
        ]

    def _create_cost_matrix(self):
        """
        Creates a |N+M| X |N+M| cost matrix between all nodes in
        graphs g1 and g2
        Each cost represents the cost of substituting,
        deleting or inserting a node
        The cost matrix consists of four regions:

        substitute 	| insert costs
        -------------------------------
        delete 		| delete -> delete

        The delete -> delete region is filled with zeros
        """
        n = len(self.g)
        m = len(self.h)
        cost_matrix = np.zeros((n + m, n + m))

        nodes_1 = _get_nodes(self.g)
        nodes_2 = _get_nodes(self.h)

        for i in range(n):
            for j in range(m):
                cost_matrix[i, j] = self.substitute_cost(nodes_1[i], nodes_2[j])

        for i in range(m):
            for j in range(m):
                cost_matrix[i + n, j] = self.insert_cost(i, j)

        for i in range(n):
            for j in range(n):
                cost_matrix[j, i + m] = self.delete_cost(i, j)

        return cost_matrix

    @abstractmethod
    def insert_cost(self, i, j):
        raise NotImplementedError

    @abstractmethod
    def delete_cost(self, i, j):
        raise NotImplementedError

    @abstractmethod
    def substitute_cost(self, nodes1, nodes2):
        raise NotImplementedError

    def __str__(self):
        return str(self._create_cost_matrix())

    def print_matrix(self):
        print(self)

    @classmethod
    def compare(cls, g, h):
        ged = cls(g, h)
        return ged.normalized_distance()
