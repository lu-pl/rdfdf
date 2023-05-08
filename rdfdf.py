from collections.abc import Callable, Mapping
from typing import Generator

import pandas as pd
from rdflib import Graph, Literal, URIRef, Namespace

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
                 field_rules: Mapping[str, tuple[URIRef, Callable[[str], _TripleObject]]],
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
    

    def _apply_field_rules(self, row: pd.Series) -> Generator[tuple[URIRef, _TripleObject], None, None]:
        """Applies field_rules to a pd.Series row;
        thus constructs a generator of predicate-object tuples.
        """
        
        _field_rules = (
            (val[0], val[1](row[key]))
            for key, val in self._field_rules.items()
        )

        return _field_rules


    def _generate_triples(self) -> Generator[_TripleType, None, None]:
        """Generates triples after applying subject_rule and field_rules;
        constructs a generator of _TripleType ready for rdflib.Graph conversion.
        """

        _triples = (
            (self._apply_subject_rule(row), *field)
            for _, row in self._df.iterrows()
            for field in self._apply_field_rules(row)
            )
        
        ## loop version
        # for _, row in self._df.iterrows():
        #     for field in self._apply_field_rules(row):
        #         print((self._apply_subject_rule(row), *field))

        return _triples


    def to_graph(self) -> Graph:
        """rdflib.Graph.adds triples from _generate_triples and returns the graph component.
        """
        
        for triple in self._generate_triples():
            self._graph.add(triple)

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
    

    
test_ns = Namespace("http://sometest.org/")

test_field_rules = {
    "Hobby": (test_ns.hasHobby, lambda x: Literal(f"***{x}***")),
    "Address": (test_ns.hasAddress, Literal)
}


df = pd.read_csv("/home/upgrd/projects/python-projects/rdfdf/tests/test.csv~1", sep=";")

test_dfgraph = DFGraphConverter(
    dataframe=df,
    subject_column="Name",
    subject_rule=test_ns,
    field_rules=test_field_rules,
)

graph = test_dfgraph.to_graph()
print(graph.serialize(format="ttl"))
