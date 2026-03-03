import unittest
from src.graph_rag import GraphRAG

class TestGraphRAG(unittest.TestCase):
    def test_add_node(self):
        g = GraphRAG()
        g.add_entity('repo', 'Codebase')
        self.assertIn('repo', g.graph.nodes)

if __name__ == '__main__':
    unittest.main()
