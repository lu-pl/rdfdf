"""Custom importer for RDF files.
"""

# from importlib.abc import Finder, Loader
from importlib.machinery import ModuleSpec

import pathlib
import sys

from rdflib import Graph


#### todo: make this general (try: Graph.parse)

class TurtleImporter:
    """Custom importer; allows to import ttl files as if they were modules.

    E.g. 'import some_rdf' looks for some_rdf.ttl in the import path,
    parses it into an rdflib.Graph instance and makes it available in the module namespace.
    """

    def __init__(self, ttl_path):

        self.ttl_path = ttl_path


    # maybe use spec_from_loader?
    @classmethod
    def find_spec(cls, name, path, target=None):

        *_, module_name = name.rpartition(".")
        ttl_file_name = f"{module_name}.ttl"

        directories = sys.path if path is None else path

        for directory in directories:
            ttl_path = pathlib.Path(directory) / ttl_file_name

            if ttl_path.exists():
                return ModuleSpec(name, cls(ttl_path))


    def create_module(self, spec):
        graph = Graph().parse(self.ttl_path)
        return graph

    def exec_module(self, module):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self.ttl_path)!r})"


# module level side-effect
sys.meta_path.append(TurtleImporter)
