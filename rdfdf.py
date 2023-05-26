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

    DFGraphConverter iterates over a dataframe and constructs RDF triples by constructing a generator of subgraphs ('field graphs');
    subgraphs are then merged with an rdflib.Graph component.

    For basic usage examples see https://gitlab.com/lupl/rdfdf.
    """

    store: dict = dict()

    def __init__(self,
                 dataframe: pd.DataFrame,
                 *,
                 subject_column: str,
                 subject_rule: Callable[[str], URIRef] | Namespace = None,
                 column_rules: Mapping[str, Callable[[], Graph | None]],
                 graph: Graph = None):

        self._df = dataframe
        self._subject_column = subject_column
        self._subject_rule = subject_rule
        self._column_rules = column_rules
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

            _subject = (
                self._apply_subject_rule(row)
                if self._subject_rule
                else row[self._subject_column]
            )

            for field, rule in self._column_rules.items():
                _object = row[field]

                # make bindings meaningful in rule callables
                rule = anaphoric(
                    __subject__=_subject,
                    __object__=_object,
                    __store__=self.store
                )(rule)

                field_rule_result = rule()

                # yield only rdflib.Graph instances
                if isinstance(field_rule_result, Graph):
                    yield field_rule_result
                continue

    def _merge_to_graph_component(self,
                                  graphs: Iterable[Graph]) -> Graph:
        """Loops over a graphs generator and merges every field_graph to the self._graph component.
        Returns the modified self._graph component.
        """

        # warning: this is not BNode-safe (yet)!!!
        # how to do BNode-safe graph merging?
        for graph in graphs:
            self._graph += graph

        return self._graph

    @property
    def graph(self):
        """Getter for the internal graph component.
        """
        return self._graph

    def to_graph(self) -> Graph:
        """rdflib.Graph.adds triples from _generate_triples and returns the graph component."""
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


# todo
class GraphDFConverter:
    """Rule-based rdflib.Graph to pandas.DataFrame converter.
    """
    ...
