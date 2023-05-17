"""rdfdf-rules for testing.
"""

from rdflib import URIRef, Literal, Graph
from rdflib.namespace import Namespace, RDF, RDFS

CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm#")
CRMCLS = Namespace("https://clscor.io/ontologies/CRMcls/")

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



def _rule_corpus_link_corpus_name():
    """corpusName rule for rule_corpus_link
    """

    __store__["corpus_name"] = __object__

    
def rule_corpus_link():
    
    subject = __subject__.lower()
    
    triples = [
        (
            URIRef("https://core.clscor.io/entity/type/linkType/corpus-website"),
            CRM.P2i_is_type_of,
            URIRef(__object__)
        ),
        (
            URIRef(f"https://{subject}.clscor.io/entity/corpus"),
            RDF.type,
            CRMCLS.X1_Corpus
        ),
        (
            URIRef(f"https://{subject}.clscor.io/entity/corpus"),
            CRM.P1_is_identified_by,
            URIRef(__object__)
        ),
        (
            URIRef(__object__),
            CRM.P1i_identifies,
            URIRef(f"https://{subject}.clscor.io/entity/corpus"),
        ),
        (
            URIRef(__object__),
            CRM.P2_has_type,
            URIRef("https://core.clscor.io/entity/type/linkType/corpus-website"),
        ),
        (
            URIRef(__object__),
            RDF.value,
            Literal(f"Link to the {__store__['corpus_name']} website.")
        )
        
    ]

    graph = Graph()

    for triple in triples:
        graph.add(triple)

    return graph


def rule_corpus_license():
    
    subject = __subject__.lower()
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
    


