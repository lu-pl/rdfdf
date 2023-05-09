from collections.abc import Callable, Mapping, Iterable
from typing import Generator

import pandas as pd
from rdflib import Graph, Literal, URIRef, Namespace

from helpers.rdfdf_utils import anaphoric

_TripleObject = URIRef | Literal
_FieldRules = Mapping[str, tuple[URIRef, Callable[[str], _TripleObject]]]
_TripleType = tuple[URIRef, URIRef, _TripleObject]


class DFGraphConverter:
    """Rule-based pandas.DataFrame to rdflib.Graph converter.
    
    Iterates over a dataframe and constructs rdf triples by
    
    for every row
      for every rule in field_rules
        - looking up the field_rules key for the current row and creating a predicate-object pair from the field_rules value
        - applying the subject_rule to the subject_column field of the current row and adding the subject to the predicate-object pair.

    For basic usage example see <repo>.
    For representation of tabular data in rdf see Allemang, Hendler: Semnantic Web for the Working Ontologist. 2011, 40ff.
    """
    
    def __init__(self,
                 dataframe: pd.DataFrame,
                 *,
                 subject_column: str,
                 subject_rule: Callable[[str], URIRef] | Namespace,
                 
                 # Callable gets passed the current column field value and is responsable for returning a Graph which then gets merged
                 field_rules: Mapping[str, Callable[[str], Graph]],
                 graph: Graph = None):
        
        self._df = dataframe
        self._subject_column = subject_column
        self._subject_rule = subject_rule
        self._field_rules = field_rules
        self._graph = graph or Graph()


    def _apply_subject_rule(self, row: pd.Series) -> URIRef:
        """Applies subject_rule to the subject_column of a pd.Series row;
        conveniently allows to also pass an rdflib.Namespace (or generally Sequence types) as subject_rule.
        """
        
        try:
            # call
            _sub_uri = self._subject_rule(row[self._subject_column])
        except TypeError:
            # getitem
            _sub_uri = self._subject_rule[row[self._subject_column]]

        return _sub_uri

    def _generate_graphs(self) -> Generator[Graph, None, None]:
        """Loops over the table rows of the provided DataFrame;
        generates and returns a Generator of graph objects for merging.
        """

        for _, row in self._df.iterrows():
            _subject = self._apply_subject_rule(row)

            for field, rule in self._field_rules.items():
                rule = anaphoric(subject=_subject)(rule)
                row_graph = rule(row[field])
                
                yield row_graph


    def _merge_to_graph_component(self,
                                  graphs: Iterable[Graph]) -> Graph:
        """Loops over a graphs generator and merges every graph to the self._graph component.
        Returns the modified self._graph component.
        """

        ## warning: this is not BNode-safe (yet)!!!
        for graph in graphs:
            self._graph += graph

        return self._graph

    
    @property
    def graph(self):
        return self._graph

    def to_graph(self) -> Graph:
        """rdflib.Graph.adds triples from _generate_triples and returns the graph component.
        """

        # generate subgraphs
        _graphs_generator = self._generate_graphs()

        # merge subgraphs to graph component
        self._merge_to_graph_component(_graphs_generator)
        
        return self._graph
            

    def serialize(self, *args, **kwargs):
        """Proxy for rdflib.Graph.serialize.
        """
        
        if not self._graph:
            self.to_graph
            
        return self._graph.serialize(*args, **kwargs)
        
    
## todo
class GraphDFConverter:
    """Rule-based rdflib.Graph to pandas.DataFrame converter.
    """
    ...
