# rdfdf

rdfdf - Functionality for *rule-based* `pandas.DataFrame` - `rdflib.Graph` conversion.

For representation of tabular data in RDF see Allemang, Hendler: Semantic Web for the Working Ontologist. 2011, 40ff.

> This project is in an early stage of development and should be used with caution

## Requirements

* python >= 3.10

## Usage

For now rdfdf provides a `DFGraphConverter` class for rule-based `pandas.DataFrame` to `rdflib.Graph conversion`. 

A `GraphDFConverter` class for rule-based `rdflib.Graph` to `pandas.DataFrame` conversion will be implemented shortly.

### DFGraphConverter

Unlike [rdfpandas](https://github.com/cadmiumkitty/rdfpandas/) which requires URIRefs as column headers (and otherwise just creates invalid RDF with e.g. literals as predicates), rdfdf computes URIRefs (or Literals for triple objects) based on rules.

DFGraphConverter iterates over a dataframe and constructs RDF triples by
- for every row
  - for every rule in field_rules
    - looking up the field_rules key for the current row and creating a predicate-object pair from the field_rules value
     - applying the subject_rule to the subject_column field of the current row and prepending the subject to the predicate-object pair.
	 
Since what triples actually are created is dependent on the field_rules, also partial table conversion is easily possible.

#### Example

Example data (`./tests/test_data/test.csv`):
```csv
"Name";"Address";"Place";"Country";"Age";"Hobby";"Favourite Colour" 
"John";"Dam 52";"Amsterdam";"The Netherlands";"32";"Fishing";"Blue"
"Jenny";"Leidseplein 2";"Amsterdam";"The Netherlands";"12";"Dancing";"Mauve"
"Jill";"52W Street 5";"Amsterdam";"United States of America";"28";"Carpentry";"Cyan"
"Jake";"12E Street 98";"Amsterdam";"United States of America";"42";"Ballet";"Purple"
```

```python
# example.py

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
```	

This generates the following RDF:
```turtle
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix ns1: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ns1:Jake ns1:age 42 ;
    ns1:hasAddress "12E Street 98" ;
    ns1:hasHobby "BALLET" ;
    foaf:name "Jake" .

ns1:Jenny ns1:age 12 ;
    ns1:hasAddress "Leidseplein 2" ;
    ns1:hasHobby "DANCING" ;
    foaf:name "Jenny" .

ns1:Jill ns1:age 28 ;
    ns1:hasAddress "52W Street 5" ;
    ns1:hasHobby "CARPENTRY" ;
    foaf:name "Jill" .

ns1:John ns1:age 32 ;
    ns1:hasAddress "Dam 52" ;
    ns1:hasHobby "FISHING" ;
    foaf:name "John" .
```
Note that fields of the `subject_column` can also be used as keys in the field_rules mapping (here "Name").

### GraphDFConverter
todo

## Contribution

Please feel free to open issues or pull requests.

