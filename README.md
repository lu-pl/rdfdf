# rdfdf

rdfdf - Functionality for rule-based `pandas.DataFrame` - `rdflib.Graph` conversion.

For representation of tabular data in RDF see Allemang, Hendler: Semantic Web for the Working Ontologist. 2011, 40ff.

> This project is in an early stage of development and should be used with caution.

## Requirements

* python >= 3.10

## Usage

For now rdfdf provides a `DFGraphConverter` class for rule-based `pandas.DataFrame` to `rdflib.Graph conversion`. 

A `GraphDFConverter` class for rule-based `rdflib.Graph` to `pandas.DataFrame` conversion will be implemented shortly.

### DFGraphConverter

Unlike [rdfpandas](https://github.com/cadmiumkitty/rdfpandas/) which requires URIRefs as column headers (and otherwise just creates invalid RDF with e.g. literals as predicates), rdfdf *computes* URIRefs (or Literals for triple objects) based on rules.

`DFGraphConverter` iterates over a dataframe and constructs RDF triples by constructing a generator of subgraphs ('row graphs') and then merging all subgraphs with an rdflib.Graph component.

Subgraphs are generated by

- for every row
  - for every rule in `column_rules`
    - looking up the `column_rules` key for the current row and calling the corresponding `column_rules` value.
	
`column_rules` values must be callables which are responsible for generating and returning a graph for merging.
`column_rules` callables are of arity 0 but have access to subject and object values from the table [anaphorically](https://en.wikipedia.org/wiki/Anaphoric_macro) as `__subject__` and `__object__` respectively (see examples below).

#### Parameters:

- **dataframe**: A pandas.DataFrame to be converted.

- **subject_column**: Selects a table column by name to be regarded as the column of triple subjects.

- **subject_rule**: Optional; either a `Callable[[str], URIRef]` or an `rdflib.Namespace` which gets applied to every field of the subject_column; 
if supplied, `__subject__` in the `column_rules` will be what `subject_rule` computes it to be; otherwise `__subject__` will be just the raw field value of the current `subject_column` and must be handled manually in order to be become a valid triple subject (i.e. a URIRef).

- **column_rules**: A mapping of column names to callables responsible for creating subgraphs ('row graphs'). As mentioned these callables have access to `__subject__` and `__object__` references.

- **graph**: Optional; allows to set the internal rdflib.Graph component.

#### Examples:

A simple example with `subject_rule` supplied:

Example data (`./tests/test_data/test.csv`):
```csv
"Name";"Address";"Place";"Country";"Age";"Hobby";"Favourite Colour" 
"John";"Dam 52";"Amsterdam";"The Netherlands";"32";"Fishing";"Blue"
"Jenny";"Leidseplein 2";"Amsterdam";"The Netherlands";"12";"Dancing";"Mauve"
"Jill";"52W Street 5";"Amsterdam";"United States of America";"28";"Carpentry";"Cyan"
"Jake";"12E Street 98";"Amsterdam";"United States of America";"42";"Ballet";"Purple"
```

```python
# example_1.py

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
    

test_column_rules = {
    "Name": name_rule,
    "Age": age_rule
}

df = pd.read_csv("../test_data/test.csv", sep=";")

dfgraph = DFGraphConverter(
    dataframe=df,
    subject_column="Name",
    subject_rule=example_ns,
    column_rules=test_column_rules,
)

graph = dfgraph.to_graph()
print(graph.serialize(format="ttl"))
```

And the same example without `subject_rule` supplied, in which case `__subject__`s must be handled manually.

```python
# example_2.py

import pandas as pd
from rdfdf import DFGraphConverter
from rdflib import Namespace, Literal, Graph, URIRef
from rdflib.namespace import FOAF, RDF

example_ns = Namespace("http://example.org/")

def name_rule():
    
    graph = Graph()
    
    ## without subject_rule parameter; __subject__ must be handled manually
    graph.add((example_ns[__subject__], RDF.type, FOAF.Person)) \
         .add((example_ns[__subject__], FOAF.name, Literal(__object__)))
    
    return graph

def age_rule():
    
    graph = Graph()

    ## without subject_rule parameter; __subject__ must be handled manually
    graph.add((example_ns[__subject__], example_ns.age , Literal(__object__)))

    return graph
    

test_column_rules = {
    "Name": name_rule,
    "Age": age_rule
}


df = pd.read_csv("../test_data/test.csv", sep=";")

dfgraph = DFGraphConverter(
    dataframe=df,
    subject_column="Name",
    # subject_rule=example_ns,
    column_rules=test_column_rules,
)

graph = dfgraph.to_graph()
print(graph.serialize(format="ttl"))
```

Output for both examples:

```ttl
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix ns1: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ns1:Jake a foaf:Person ;
    ns1:age 42 ;
    foaf:name "Jake" .

ns1:Jenny a foaf:Person ;
    ns1:age 12 ;
    foaf:name "Jenny" .

ns1:Jill a foaf:Person ;
    ns1:age 28 ;
    foaf:name "Jill" .

ns1:John a foaf:Person ;
    ns1:age 32 ;
    foaf:name "John" .
```

[todo: more complex examples e.g. with [pydantic-cidoc-crm](https://pypi.org/project/pydantic-cidoc-crm/)]

### GraphDFConverter
[todo]

## Contribution

Please feel free to open issues or pull requests.

