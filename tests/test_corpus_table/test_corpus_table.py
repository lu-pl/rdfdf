"""Pytest entry point for corpusTable tests
"""

from rdflib import Graph
from rdflib.compare import isomorphic

import rdfdf

import helpers.importers

from table_partitions import (
    rem_partition
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
    # rule_corpus_link,
    rule_corpus_name,
    # rule_corpus_language # ?
)


def test_corpus_acronym():
    pass
    
def test_corpus_api():
    pass

def test_corpus_license():
    pass

def test_corpus_link():
    pass

def test_corpus_name():
    # 1. create actual_graph according to rule with rdfdf.DFGraphConverter
    # 2. compare to target_graph: assert isomorphic(actual_graph, target_graph)
    
    ### translate to corpus_name properly (still refs to acronym)
    # actual_graph = rdfdf.DFGraphConverter(
    #     dataframe=rem_partition,
    #     subject_column="corpusAcronym",
    #     column_rules={"full_title": rule_corpus_name},
    # )

    # assert isomorphic(actual_graph, target_corpus_name)
    pass

    
## test
actual_graph = rdfdf.DFGraphConverter(
    dataframe=rem_partition,
    subject_column="corpusAcronym",
    column_rules={"corpusName": rule_corpus_name},
)

# print(actual_graph.to_graph().serialize(format="ttl"))

print(isomorphic(
        actual_graph.to_graph(),
        target_corpus_name))

