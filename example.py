from rdfdf import DFGraphConverter

from helpers.rdfdf_utils import anaphoric

import pandas as pd

from rdflib import Namespace, Literal, Graph, URIRef
from rdflib.namespace import FOAF, RDF

example = Namespace("http://example.org/")

def name_rule(obj_value):
    graph = Graph()
    
    graph.add(
        (subject, FOAF.name, Literal(obj_value))
    )
    
    graph.add(
        (subject, RDF.type, FOAF.Person)
    )

    return graph


test_field_rules = {
    "Name": name_rule,
}

df = pd.read_csv("./tests/test_data/test.csv", sep=";")

dfgraph = DFGraphConverter(
    dataframe=df,
    subject_column="Name",
    subject_rule=example,
    field_rules=test_field_rules,
)

graph = dfgraph.to_graph()
print(graph.serialize(format="ttl"))
