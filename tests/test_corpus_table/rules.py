"""rdfdf-rules for testing.
"""

from rdflib import URIRef, Literal, Graph
from rdflib.namespace import Namespace, RDF

CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm#")

def rule_corpus_name():
    
    subject = __subject__.lower()
    subject_uri = URIRef(f"https://{subject}.clscor.io/entity/corpus/title/full")

    triples = [
        (
            URIRef("https://core.clscor.io/entity/type/full_title"),
            CRM.P2i_is_type_of,
            subject_uri
        ),
        (
            URIRef(f"https://{subject}.clscor.io/entity/corpus"),
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
            URIRef(f"https://{subject}.clscor.io/entity/corpus")
        ),
        (
            subject_uri,
            CRM.P2_has_type,
            URIRef("https://core.clscor.io/entity/type/full_title"),
        ),
        (
            subject_uri,
            RDF.value,
            Literal("Reference corpus Middle High German")
        )
    ]
    
    graph = Graph()

    for triple in triples:
        graph.add(triple)

    return graph

