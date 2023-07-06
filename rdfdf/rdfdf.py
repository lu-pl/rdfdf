"""rdfdf - Functionality for rule-based Dataframe to Graph conversion."""

import functools

from collections.abc import Iterable, Callable
from typing import Generator, Optional

import pandas as pd
from rdflib import Graph, URIRef, Namespace

from rdfdf.rdfdf_types import _RulesMapping


class DFGraphConverter:
    """Rule-based pandas.DataFrame to rdflib.Graph converter.

    DFGraphConverter iterates over a dataframe and constructs RDF triples
    by constructing a generator of subgraphs ('field graphs');
    subgraphs are then merged with an rdflib.Graph component.

    For basic usage examples see https://github.com/lu-pl/rdfdf.
    """

    store: dict = dict()

    def __init__(self,
                 dataframe: pd.DataFrame,
                 *,
                 subject_column: str,
                 subject_rule: Optional[
                     Callable[[str], URIRef] | Namespace
                 ] = None,
                 column_rules: _RulesMapping,
                 graph: Optional[Graph] = None):
        """Initialize a DFGraphConverter instance."""
        self._df = dataframe
        self._subject_column = subject_column
        self._subject_rule = subject_rule
        self._column_rules = column_rules
        # bug fix: this allows also empty but namespaced graphs
        self._graph = Graph() if graph is None else graph

    def _apply_subject_rule(self, row: pd.Series) -> URIRef:
        """Apply subject_rule to the subject_column of a pd.Series row.

        Conveniently allows to also pass an rdflib.Namespace
        (or generally Sequence types) as subject_rule.
        """
        try:
            # call
            _sub_uri = self._subject_rule(row[self._subject_column])
        except TypeError:
            # getitem
            _sub_uri = self._subject_rule[row[self._subject_column]]

        return _sub_uri

    def _generate_graphs(self) -> Generator[Graph, None, None]:
        """Loop over the table rows of the provided DataFrame.

        Generates and returns a Generator of graph objects for merging.
        """
        for _, row in self._df.iterrows():

            _subject = (
                self._apply_subject_rule(row)
                if self._subject_rule
                else row[self._subject_column]
            )

            for field, rule in self._column_rules.items():
                _object = row[field]

                field_rule_result = rule(
                    _subject,
                    _object,
                    self.store
                )

                # yield only rdflib.Graph instances
                if isinstance(field_rule_result, Graph):
                    yield field_rule_result
                continue

    def _merge_to_graph_component(self, graphs: Iterable[Graph]) -> Graph:
        """Merge subgraphs to main graph.

        Loops over a graphs generator and merges every field_graph with the
        self._graph component. Returns the modified self._graph component.
        """
        # warning: this is not BNode-safe (yet)!!!
        # todo: how to do BNode-safe graph merging?
        for graph in graphs:
            self._graph += graph

        return self._graph

    @property
    def graph(self):
        """Getter for the internal graph component."""
        return self._graph

    def to_graph(self) -> Graph:
        """Add triples from _generate_triples and return the graph component."""
        # generate subgraphs
        _graphs_generator = self._generate_graphs()

        # merge subgraphs to graph component
        self._merge_to_graph_component(_graphs_generator)

        return self._graph

    @functools.wraps(Graph.serialize)
    def serialize(self, *args, **kwargs):
        """Serialize triples from graph component.

        Proxy for rdflib.Graph.serialize.
        """
        if not self._graph:
            self.to_graph

        return self._graph.serialize(*args, **kwargs)
