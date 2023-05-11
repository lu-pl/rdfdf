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

`DFGraphConverter` iterates over a dataframe and constructs RDF triples by constructing a generator of subgraphs ('field graphs') and then merging all subgraphs with an `rdflib.Graph` component.

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

- **column_rules**: A mapping of column names to callables responsible for creating subgraphs ('field graphs'). As mentioned these callables have access to `__subject__` and `__object__` references.

- **graph**: Optional; allows to set the internal rdflib.Graph component.

#### Example:

For basic examples see [example_1](`./tests/examples/example_1.py`) and [example_2](`./tests/examples/example_2.py`).

A slightly more involved example:

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

```python
# ./tests/examples/example_3.py

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

Note that this is rather verbose and could probably be expressed more concisely with Python ontology abstractions like [pydantic-cidoc-crm](https://pypi.org/project/pydantic-cidoc-crm/).


### GraphDFConverter
[todo]

## Contribution

Please feel free to open issues or pull requests.

