from rdfdf import DFGraphConverter

import pandas as pd

from rdflib import Namespace, Literal
from rdflib.namespace import FOAF

example = Namespace("http://example.org/")

test_field_rules = {
    "Name": (FOAF.name, Literal),
    "Age": (example.age, Literal),
    "Hobby": (example.hasHobby, lambda x: Literal(x.upper())),
    "Address": (example.hasAddress, Literal),
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
