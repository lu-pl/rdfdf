import pandas as pd

from rdflib import URIRef, Graph, Namespace, Literal
from rdflib.namespace import RDF

from rdfdf import DFGraphConverter


CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")

table = [
    {
        "id": "rem",
        "full_title": "Reference corpus Middle High German"
    }
]

df = pd.DataFrame(data=table)


def full_title_rule():
    
    graph = Graph()
    subject_uri = URIRef(f"https://{__subject__}.clscor.io/entity/corpus/title/full")

    triples = [
        (
            subject_uri,
            RDF.type,
            CRM.E41_Appellation
        ),
        (
            subject_uri,
            CRM.P1_identifies,
            URIRef(f"https://{__subject__}.clscor.io/entity/corpus")
        ),
        # inverse
        (
            URIRef(f"https://{__subject__}.clscor.io/entity/corpus"),
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

    for triple in triples:
        graph.add(triple)

    return graph

    
column_rules = {
    "full_title": full_title_rule
}

dfgraph = DFGraphConverter(
    dataframe=df,
    subject_column="id",
    column_rules=column_rules,
)

graph = dfgraph.to_graph()
print(graph.serialize(format="ttl"))
