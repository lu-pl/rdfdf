""" Dataframe to graph conversion example with state sharing
"""

import pandas as pd
from rdfdf import DFGraphConverter
from rdflib import Namespace, Literal, Graph, URIRef
from rdflib.namespace import FOAF, RDF

example_ns = Namespace("http://example.org/")

def name_rule():
    graph = Graph()
    
    graph.add((__subject__, RDF.type, FOAF.Person)) \
         .add((__subject__, FOAF.name, Literal(__object__)))
    
    return graph

def age_rule():
    graph = Graph()
    graph.add((__subject__, example_ns.age, Literal(__object__)))

    return graph


def address_rule():
    __store__["address"] = __object__
    
def place_rule():
    __store__["place"] = __object__
    
def full_address_rule():
    _full_address = (
        f"{__store__['address']}, "
        f"{__store__['place']}, "
        f"{__object__}"
    )

    graph = Graph()
    graph.add((__subject__, example_ns.fullAddress, Literal(_full_address)))

    return graph
    

test_column_rules = {
    "Name": name_rule,
    "Age": age_rule,
    "Address": address_rule,
    "Place": place_rule,
    "Country": full_address_rule
}

df = pd.read_csv("../tests/test_data/test.csv", sep=";")

dfgraph = DFGraphConverter(
    dataframe=df,
    subject_column="Name",
    subject_rule=example_ns,
    column_rules=test_column_rules,
)

graph = dfgraph.to_graph()
print(graph.serialize(format="ttl"))
