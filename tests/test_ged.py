# -*- coding: utf-8 -*-

import unittest

import networkx as nx

from ged4py import GraphEditDistance


class TestGed(unittest.TestCase):
    """Tests for ged4py."""

    def test_it(self):
        g = nx.Graph()
        g.add_edge("A", "B")

        g.add_node("C", weight=1)
        h = g.copy()
        h.add_edge("A", "C")

        ged = GraphEditDistance(g, h)

        print('Cost matrix:\n')
        ged.print_matrix()
        print(f'Normalized distance: {ged.normalized_distance():.2f}')


if __name__ == '__main__':
    unittest.main()
