"""Pytest entry point for corpusTable tests
"""

import pytest

from rdflib import Graph
from rdflib.compare import isomorphic

import rdfdf

import helpers.importers

from table_partitions import (
    corpus_table,
    rem_partition,
    greekdracor_partition,
    fredracor_partition
)

# for custom importer see helpers.importers
from target_graphs import (
    target_corpus_acronym,
    target_corpus_api,
    target_corpus_license,
    target_corpus_link,
    target_corpus_name,
    target_corpus_language
)

from rules import (
    rule_corpus_acronym,
    rule_corpus_api,
    rule_corpus_license,
    rule_corpus_link,
    _rule_corpus_link_corpus_name,
    rule_corpus_name,
    rule_corpus_language
)

##################################################
##################################################
#### table partition tests

def test_corpus_license():
    """rdfdf conversion test.
    Checks for graph isomorphism between an rdfdf-generated graph and a target graph.
    """

    _actual_conversion = rdfdf.DFGraphConverter(
        dataframe=rem_partition,
        subject_column="corpusAcronym",
        # ! licence vs. license
        column_rules={"corpusLicence": rule_corpus_license}
    )

    actual_corpus_license = _actual_conversion.to_graph()

    assert isomorphic(actual_corpus_license, target_corpus_license)


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


def test_corpus_api():
    """rdfdf conversion test.
    Checks for graph isomorphism between an rdfdf-generated graph and a target graph.
    """

    _actual_conversion = rdfdf.DFGraphConverter(
        dataframe=greekdracor_partition,
        subject_column="corpusAcronym",
        column_rules={
            "corpusName": _rule_corpus_link_corpus_name,
            "corpusAPI": rule_corpus_api
        }
    )

    actual_corpus_api = _actual_conversion.to_graph()

    assert isomorphic(actual_corpus_api, target_corpus_api)


def test_corpus_acronym():
    """rdfdf conversion test.
    Checks for graph isomorphism between an rdfdf-generated graph and a target graph.
    """

    _actual_conversion = rdfdf.DFGraphConverter(
        dataframe=rem_partition,
        subject_column="corpusAcronym",
        column_rules={"corpusAcronym": rule_corpus_acronym}
    )

    actual_corpus_acronym = _actual_conversion.to_graph()

    assert isomorphic(actual_corpus_acronym, target_corpus_acronym)

def test_corpus_language ():
    """rdfdf conversion test.
    Checks for graph isomorphism between an rdfdf-generated graph and a target graph.
    """

    _actual_conversion = rdfdf.DFGraphConverter(
        dataframe=fredracor_partition,
        subject_column="corpusAcronym",
        column_rules={"corpusLanguage": rule_corpus_language}
    )

    actual_corpus_language = _actual_conversion.to_graph()

    assert isomorphic(actual_corpus_language, target_corpus_language)



##################################################
##################################################
#### full copurs_table tests

def test_full_corpus_license():
    """rdfdf full corpus_table conversion test.
    Just runs a single rule against the full table and checks if the graph is non-empty.
    """

    _actual_conversion = rdfdf.DFGraphConverter(
        dataframe=corpus_table,
        subject_column="corpusAcronym",
        # ! licence vs. license
        column_rules={"corpusLicence": rule_corpus_license}
    )

    actual_corpus_license = _actual_conversion.to_graph()

    assert actual_corpus_license


@pytest.mark.skip(reason="problem almost certainly not rdfdf but weird data in the link field")
def test_full_corpus_link():
    """rdfdf full corpus_table conversion test.
    Just runs a single rule against the full table and checks if the graph is non-empty.
    """

    _actual_conversion = rdfdf.DFGraphConverter(
        dataframe=corpus_table,
        subject_column="corpusAcronym",
        column_rules={
            "corpusName": _rule_corpus_link_corpus_name,
            "corpusLink": rule_corpus_link
        }
    )

    actual_corpus_link = _actual_conversion.to_graph()

    assert actual_corpus_link


def test_full_corpus_name():
    """rdfdf full corpus_table conversion test.
    Just runs a single rule against the full table and checks if the graph is non-empty.
    """

    _actual_conversion = rdfdf.DFGraphConverter(
        dataframe=corpus_table,
        subject_column="corpusAcronym",
        column_rules={"corpusName": rule_corpus_name}
    )

    actual_corpus_name = _actual_conversion.to_graph()

    assert actual_corpus_name


def test_full_corpus_api():
    """rdfdf full corpus_table conversion test.
    Just runs a single rule against the full table and checks if the graph is non-empty.
    """

    _actual_conversion = rdfdf.DFGraphConverter(
        dataframe=corpus_table,
        subject_column="corpusAcronym",
        column_rules={
            "corpusName": _rule_corpus_link_corpus_name,
            "corpusAPI": rule_corpus_api
        }
    )

    actual_corpus_api = _actual_conversion.to_graph()

    assert actual_corpus_api


def test_full_corpus_acronym():
    """rdfdf full corpus_table conversion test.
    Just runs a single rule against the full table and checks if the graph is non-empty.
    """

    _actual_conversion = rdfdf.DFGraphConverter(
        dataframe=corpus_table,
        subject_column="corpusAcronym",
        column_rules={"corpusAcronym": rule_corpus_acronym}
    )

    actual_corpus_acronym = _actual_conversion.to_graph()

    assert actual_corpus_acronym


@pytest.mark.skip(reason="ISO lang code conversion expectedly breaks on diachronic languages")
def test_full_corpus_language ():
    """rdfdf full corpus_table conversion test.
    Just runs a single rule against the full table and checks if the graph is non-empty.
    """

    _actual_conversion = rdfdf.DFGraphConverter(
        dataframe=corpus_table,
        subject_column="corpusAcronym",
        column_rules={"corpusLanguage": rule_corpus_language}
    )

    actual_corpus_language = _actual_conversion.to_graph()

    assert actual_corpus_language
