"""rdfdf-rules for testing.
"""

from rdflib import URIRef, Literal, Graph
from rdflib.namespace import Namespace, RDF

CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")



def rule_corpus_name():
    
    lsubject = __subject__.lower()
    subject_uri = URIRef(f"https://{lsubject}.clscor.io/entity/corpus/title/full")

    triples = [
        (
            subject_uri,
            RDF.type,
            CRM.E41_Appellation
        ),
        (
            subject_uri,
            CRM.P1_identifies,
            URIRef(f"https://{lsubject}.clscor.io/entity/corpus")
        ),
        # inverse
        (
            URIRef(f"https://{lsubject}.clscor.io/entity/corpus"),
            CRM.P1_is_identified_by,
            subject_uri
        ),
        (
            subject_uri,
            CRM.P2_has_type,
            URIRef("https://core.clscor.io/entity/type/title/full")
        ),
        (
            subject_uri,
            URIRef("http://www.cidoc-crm.org/cidoc-crm/190_has_symbolic_content"),
            Literal(__object__)
        ),
    ]
    
    graph = Graph()

    for triple in triples:
        graph.add(triple)

    return graph

