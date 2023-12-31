"""rdfdf-rules for testing.
"""

from rdfdf.helpers.rdfdf_utils import genhash

import langcodes
from rdflib import URIRef, Literal, Graph
from rdflib.namespace import Namespace, RDF, RDFS

CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm#")
CRMCLS = Namespace("https://clscor.io/ontologies/CRMcls/")


def rule_corpus_name(subject_field, object_field, store):
    """Rule."""
    subject = subject_field.lower()
    subject_uri = URIRef(f"https://{subject}.clscor.io/entity/corpus/title/full")
    full_title_uri = URIRef("https://core.clscor.io/entity/type/full_title")
    corpus_uri = URIRef(f"https://{subject}.clscor.io/entity/corpus")

    triples = [
        (
            full_title_uri,
            CRM.P2i_is_type_of,
            subject_uri
        ),
        (
            corpus_uri,
            CRM.P1_is_identified_by,
            subject_uri
        ),
        (
            subject_uri,
            RDF.type,
            CRM.E41_Appellation
        ),
        (
            subject_uri,
            CRM.P1i_identifies,
            corpus_uri
        ),
        (
            subject_uri,
            CRM.P2_has_type,
            full_title_uri
        ),
        (
            subject_uri,
            RDF.value,
            Literal(object_field)
        )
    ]

    graph = Graph()

    for triple in triples:
        graph.add(triple)

    return graph



def _rule_corpus_link_corpus_name(subject_field, object_field, store):
    """corpusName rule for rule_corpus_link
    """

    store["corpus_name"] = object_field


def rule_corpus_link(subject_field, object_field, store):

    subject = subject_field.lower()
    corpus_website_uri = URIRef("https://core.clscor.io/entity/type/linkType/corpus-website")
    corpus_uri = URIRef(f"https://{subject}.clscor.io/entity/corpus")

    triples = [
        (
            corpus_website_uri,
            CRM.P2i_is_type_of,
            URIRef(object_field)
        ),
        (
            corpus_uri,
            RDF.type,
            CRMCLS.X1_Corpus
        ),
        (
            corpus_uri,
            CRM.P1_is_identified_by,
            URIRef(object_field)
        ),
        (
            URIRef(object_field),
            CRM.P1i_identifies,
            corpus_uri
        ),
        (
            URIRef(object_field),
            CRM.P2_has_type,
            corpus_website_uri
        ),
        (
            URIRef(object_field),
            RDF.value,
            Literal(f"Link to the {store['corpus_name']} website.")
        )

    ]

    graph = Graph()

    for triple in triples:
        graph.add(triple)

    return graph


def rule_corpus_license(subject_field, object_field, store):

    subject = subject_field.lower()
    corpus_uri = URIRef(f"https://{subject}.clscor.io/entity/corpus")
    license_uri = URIRef(f"https://{subject}.clscor.io/entity/corpus/license1")
    cc4_license_uri = URIRef("http://creativecommons.org/licenses/by-sa/4.0/")
    cc1_license_uri = URIRef("http://creativecommons.org/licenses/nc/1.0/")

    triples = [
        (
            corpus_uri,
            CRM.P104_is_subject_to,
            license_uri
        ),
        (
            license_uri,
            RDF.type,
            CRM.E30_Right
        ),
        (
            license_uri,
            RDFS.label,
            Literal("License of 'rem' [Right]: CC BY-SA 4.0")
        ),
        (
            license_uri,
            CRM.P2_has_type,
            cc4_license_uri
        ),
        (
            license_uri,
            CRM.P104i_applies_to,
            corpus_uri
        ),
        (
            cc4_license_uri,
            RDF.type,
            CRM.E55_Type
        ),
        (
            cc4_license_uri,
            RDFS.label,
            Literal("CC BY-SA 4.0")
        ),
        (
            cc1_license_uri,
            RDF.type,
            CRM.E55_Type
        ),
        (
            cc1_license_uri,
            RDFS.label,
            Literal("CC NC 1.0")
        ),
    ]

    graph = Graph()

    for triple in triples:
        graph.add(triple)

    return graph


def rule_corpus_api(subject_field, object_field, store):

    subject = subject_field.lower()
    corpus_uri = URIRef(f"https://{subject}.clscor.io/entity/corpus")
    corpus_api_uri = URIRef("https://core.clscor.io/entity/type/linkType/corpus-api")
    dracor_api_uri = URIRef("https://dracor.org/doc/api")

    triples = [
        (
            corpus_api_uri,
            CRM.P2i_is_type_of,
            dracor_api_uri
        ),
        (
            corpus_uri,
            RDF.type,
            CRMCLS.X1_Corpus
        ),
        (
            corpus_uri,
            CRM.P1_is_identified_by,
            dracor_api_uri
        ),
        (
            dracor_api_uri,
            CRM.P1i_identifies,
            corpus_uri
        ),
        (
            dracor_api_uri,
            CRM.P2_has_type,
            corpus_api_uri
        ),
        (
            dracor_api_uri,
            RDF.value,
            Literal(f"Link to the {store['corpus_name']} API")
        )
    ]

    graph = Graph()

    for triple in triples:
        graph.add(triple)

    return graph


def rule_corpus_acronym(subject_field, object_field, store):

    subject = subject_field.lower()
    acronym_uri = URIRef(f"https://{subject}.clscor.io/entity/corpus/title/acronym")
    acronym_type_uri = URIRef("https://core.clscor.io/entity/type/acronym")
    corpus_uri = URIRef(f"https://{subject}.clscor.io/entity/corpus")

    triples = [
        (
            acronym_type_uri,
            CRM.P2i_is_type_of,
            acronym_uri
        ),
        (
            corpus_uri,
            CRM.P1_is_identified_by,
            acronym_uri
        ),
        (
            acronym_uri,
            RDF.type,
            CRM.E41_Appellation
        ),
        (
            acronym_uri,
            CRM.P1i_identifies,
            corpus_uri
        ),
        (
            acronym_uri,
            CRM.P2_has_type,
            acronym_type_uri
        ),
        (
            acronym_uri,
            RDF.value,
            Literal(subject_field)
        )
    ]

    graph = Graph()

    for triple in triples:
        graph.add(triple)

    return graph


def rule_corpus_language(subject_field, object_field, store):

    subject = subject_field.lower()
    lang_tag = langcodes.find(object_field).to_tag()
    lang_hash = genhash(object_field)
    lang_uri_name = URIRef(f"https://{subject}.clscor.io/entity/language/{lang_hash}/name")
    lang_uri = URIRef(f"https://{subject}.clscor.io/entity/language/{lang_hash}")

    vocabs_lang_uri = URIRef(f"https://vocabs.acdh.oeaw.ac.at/iso6391/{lang_tag}")
    corpus_uri = URIRef(f"https://{subject}.clscor.io/entity/corpus")

    triples = [
        (
            lang_uri_name,
            RDF.type,
            CRM.E41_Appellation
        ),
        (
            lang_uri_name,
            RDFS.label,
            Literal(f"{object_field} [Appellation of Language]")
        ),
        (
            lang_uri_name,
            CRM.P1i_identifies,
            lang_uri
        ),
        (
            lang_uri_name,
            RDF.value,
            Literal(f"{object_field}")
        ),
        (
            vocabs_lang_uri,
            CRM.P1i_identifies,
            lang_uri
        ),
        (
            lang_uri,
            RDF.type,
            CRM.E56_Language
        ),
        (
            lang_uri,
            RDFS.label,
            Literal(f"{object_field} [Language]")
        ),
        (
            lang_uri,
            CRM.P1_is_identified_by,
            lang_uri_name
        ),
        (
            lang_uri,
            CRM.P1_is_identified_by,
            vocabs_lang_uri
        ),
        (
            lang_uri,
            CRMCLS.Y2i_should_be_language_of_documents,
            corpus_uri
        ),
    ]

    graph = Graph()

    for triple in triples:
        graph.add(triple)

    return graph
