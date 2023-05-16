"""Pytest entry point for corpusTable tests
"""

from rdflib import Graph
from rdflib.compare import isomorphic

import rdfdf

import helpers.importers

from table_partitions import (
    rem_partition,
    greekdracor_partition
)

# for custom importer see helpers.importers
from target_graphs import (
    target_corpus_acronym,
    target_corpus_api,
    target_corpus_license,
    target_corpus_link,
    target_corpus_name,
    # target_corpus_language # ?
)

from rules import (
    # rule_corpus_acronym,
    # rule_corpus_api,
    # rule_corpus_license,
    rule_corpus_link,
    _rule_corpus_link_corpus_name,
    rule_corpus_name,
    # rule_corpus_language # ?
)


def test_corpus_acronym():
    """rdfdf conversion test.
    Checks for graph isomorphism between an rdfdf-generated graph and a target graph.
    """
    pass
    
def test_corpus_api():
    """rdfdf conversion test.
    Checks for graph isomorphism between an rdfdf-generated graph and a target graph.
    """
    pass

def test_corpus_license():
    """rdfdf conversion test.
    Checks for graph isomorphism between an rdfdf-generated graph and a target graph.
    """
    pass

def test_corpus_link():
    """rdfdf conversion test.
    Checks for graph isomorphism between an rdfdf-generated graph and a target graph.
    """

    _actual_conversion = rdfdf.DFGraphConverter(
        dataframe=greekdracor_partition,
        subject_column="corpusAcronym",
        column_rules={
            "corpusName": _rule_corpus_link_corpus_name,
            "corpusLink": rule_corpus_link
        }
    )

    actual_corpus_link = _actual_conversion.to_graph()

    assert isomorphic(actual_corpus_link, target_corpus_link)

# still AssertionError -> fix rule
test_corpus_link()
    

def test_corpus_name():
    """rdfdf conversion test.
    Checks for graph isomorphism between an rdfdf-generated graph and a target graph.
    """
    
    _actual_conversion = rdfdf.DFGraphConverter(
        dataframe=rem_partition,
        subject_column="corpusAcronym",
        column_rules={"corpusName": rule_corpus_name}
    )
    
    actual_corpus_name = _actual_conversion.to_graph()

    assert isomorphic(actual_corpus_name, target_corpus_name)



