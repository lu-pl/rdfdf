
# rdfdf
![pipeline status](https://gitlab.com/lupl/rdfdf/badges/dev/pipeline.svg)

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

`DFGraphConverter` iterates over a dataframe and constructs RDF triples by constructing a generator of subgraphs ('field graphs') and then merging all subgraphs with an `rdflib.Graph` component.

Subgraphs are generated by

- for every row
  - for every rule in `column_rules`
    - looking up the `column_rules` key for the current row and calling the corresponding `column_rules` value.
	
`column_rules` values must be callables which are responsible for generating and returning a graph for merging. Note that rules actually don't need to return an instance of `rdflib.Graph` (e.g. if a rule just accesses `__store__`; see the [state sharing example](https://gitlab.com/lupl/rdfdf/-/tree/feature/state-sharing?ref_type=heads#state-sharing-example) below), in which case the result is skipped in the generator.

`column_rules` callables are of arity 0 but have access to subject and object values from the table [anaphorically](https://en.wikipedia.org/wiki/Anaphoric_macro) as `__subject__` and `__object__` respectively (see examples below).

Note that also `__store__` is available in rules; `__store__` references the class level attribute `store` (a dictionary), this makes state sharing between rules *and* `DFGraphConverter` instances possible.

#### Parameters:

- **dataframe**: A pandas.DataFrame to be converted.

- **subject_column**: Selects a table column by name to be regarded as the column of triple subjects.

- **subject_rule**: Optional; either a `Callable[[str], URIRef]` or an `rdflib.Namespace` which gets applied to every field of the subject_column; 
if supplied, `__subject__` in the `column_rules` will be what `subject_rule` computes it to be; otherwise `__subject__` will be just the raw field value of the current `subject_column` and must be handled manually in order to be become a valid triple subject (i.e. a URIRef).

- **column_rules**: A mapping of column names to callables responsible for creating subgraphs ('field graphs'). As mentioned these callables have access to `__subject__` and `__object__` references.

- **graph**: Optional; allows to set the internal rdflib.Graph component.

#### Examples:

See [examples](./examples/).

##### A slightly more involved example:

Example data:

```csv
"id";"full_title"
"rem";"Reference corpus Middle High German"
```

Desired output:

```rdf
<https://rem.clscor.io/entity/corpus> crm:P1_is_identified_by <https://rem.clscor.io/entity/corpus/title/full> . 

<https://rem.clscor.io/entity/corpus/title/full> a crm:E41_Appellation ; 
    crm:P1i_identifies <https://rem.clscor.io/entity/corpus> ; 
    crm:P2_has_type <https://core.clscor.io/entity/type/title/full> ; 
    crm:190_has_symbolic_content "Reference corpus Middle High German" .
```

[/examples/example_3.py](./examples/example_3.py):
```python
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
```

Note that the rule is rather verbose and could probably be expressed more concisely with Python ontology abstractions like [pydantic-cidoc-crm](https://pypi.org/project/pydantic-cidoc-crm/).

[todo: express above rule more concisely]

##### State sharing example

As mentioned, state can be shared between rules via the `__store__` binding and also between `DFGraphConverter` instances via the `store` class level attribute (which `__store__` actually references).

The following example constructs an RDF literal from multiple table fields:

[Test data](./tests/test_data/test.csv):
```csv
"Name";"Address";"Place";"Country";"Age";"Hobby";"Favourite Colour" 
"John";"Dam 52";"Amsterdam";"The Netherlands";"32";"Fishing";"Blue"
"Jenny";"Leidseplein 2";"Amsterdam";"The Netherlands";"12";"Dancing";"Mauve"
"Jill";"52W Street 5";"Amsterdam";"United States of America";"28";"Carpentry";"Cyan"
"Jake";"12E Street 98";"Amsterdam";"United States of America";"42";"Ballet";"Purple"
```

[/examples/example_4.py](./examples/example_4.py):
```python
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
```

Output
```ttl
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix ns1: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ns1:Jake a foaf:Person ;
    ns1:age 42 ;
    ns1:fullAddress "12E Street 98, Amsterdam, United States of America" ;
    foaf:name "Jake" .

ns1:Jenny a foaf:Person ;
    ns1:age 12 ;
    ns1:fullAddress "Leidseplein 2, Amsterdam, The Netherlands" ;
    foaf:name "Jenny" .

ns1:Jill a foaf:Person ;
    ns1:age 28 ;
    ns1:fullAddress "52W Street 5, Amsterdam, United States of America" ;
    foaf:name "Jill" .

ns1:John a foaf:Person ;
    ns1:age 32 ;
    ns1:fullAddress "Dam 52, Amsterdam, The Netherlands" ;
    foaf:name "John" .
```

Note that although `address_rule` and `place_rule` do not return graph instances but merely set up `__store__`, they obviously still must be connected to a table field in the `column_rules` mapping.

### GraphDFConverter
[todo]

## Contribution

Please feel free to open issues or pull requests.

