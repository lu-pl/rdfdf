from rdfdf import DFGraphConverter

from helpers.rdfdf_utils import anaphoric

import pandas as pd

from rdflib import Namespace, Literal, Graph, URIRef
from rdflib.namespace import FOAF

example = Namespace("http://example.org/")

def name_rule(obj_value):
    graph = Graph().add(
        # (subject, FOAF.name, Literal(obj_value))
        (subject, URIRef("somepred"), Literal(obj_value))
    )

    return graph



test_field_rules = {
    ## old
    # "Name": (FOAF.name, Literal),
    
    ## new
    # "Name": lambda obj_value: Graph.add((subject, FOAF.name, Literal(obj_value))),
    "Name": name_rule
    
    # "Age": (example.age, Literal),
    # "Hobby": (example.hasHobby, lambda x: Literal(x.upper())),
    # "Address": (example.hasAddress, Literal),
}

# df = pd.read_csv("./tests/test_data/test.csv", sep=";")

# dfgraph = DFGraphConverter(
#     dataframe=df,
#     subject_column="Name",
#     subject_rule=example,
#     field_rules=test_field_rules,
# )

# list(dfgraph._generate_graphs())

name_rule = anaphoric(subject=URIRef("TestName"))(name_rule)
print(name_rule(obj_value="test"))


# graph = dfgraph.to_graph()
# print(graph.serialize(format="ttl"))
