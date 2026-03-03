import re
import networkx as nx
from typing import Dict, List

class SimpleGraphRAG:
    """
    A lightweight Graph RAG implementation for Pull Request Context.
    Constructs a dependency graph by analyzing basic file references and imports, 
    giving the LLM structural awareness (Retrieval-Augmented Generation via Graph).
    """
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_graph_from_diffs(self, diffs: List[str], filenames: List[str]):
        """Parses git diffs to extract naive python/js dependency relationships."""
        for filename, diff_content in zip(filenames, diffs):
            self.graph.add_node(filename)
            # Naively match Python imports and general file references in diffs
            imports = re.findall(r'^(?:\+|-)?\s*(?:from|import)\s+([a-zA-Z0-9_\.]+)', diff_content, re.MULTILINE)
            for imp in imports:
                self.graph.add_edge(filename, imp)

    def retrieve_context(self, filename: str, depth: int = 1) -> str:
        """Retrieves adjacent nodes to augment the LLM prompt with architectural context."""
        if filename not in self.graph:
            return "No extended graph architecture context available for this file."
        
        related_nodes = list(nx.single_source_shortest_path_length(self.graph, filename, cutoff=depth).keys())
        if len(related_nodes) <= 1:
            return f"Graph Context: '{filename}' has no detectable dependencies in this PR."
            
        context = f"Graph Context: According to the dependency graph, '{filename}' is closely coupled with: {', '.join([n for n in related_nodes if n != filename])}."
        return context
