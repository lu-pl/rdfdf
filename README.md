
# rdfdf
![pipeline status](https://gitlab.com/lupl/rdfdf/badges/dev/pipeline.svg)
[![PyPI version](https://badge.fury.io/py/rdfdf.svg)](https://badge.fury.io/py/rdfdf)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

rdfdf - Functionality for rule-based `pandas.DataFrame` - `rdflib.Graph` conversion.

For representation of tabular data in RDF see Allemang, Hendler: Semantic Web for the Working Ontologist. 2011, 40ff.

> This project is in an early stage of development and should be used with caution.

## Requirements

* python >= 3.10

## Usage

For now rdfdf provides a `DFGraphConverter` class for rule-based `pandas.DataFrame` to `rdflib.Graph conversion`. 

Template-based conversion functionality might be available in the future.

### DFGraphConverter

Unlike [rdfpandas](https://github.com/cadmiumkitty/rdfpandas/) which requires URIRefs as column headers (and otherwise just creates invalid RDF with e.g. literals as predicates), rdfdf *computes* URIRefs (or Literals for triple objects) based on rules.

`DFGraphConverter` iterates over a dataframe and constructs RDF triples by constructing a generator of subgraphs ('field graphs') and then merging all subgraphs with an `rdflib.Graph` component.

Subgraphs are generated by

- for every row
  - for every rule in `column_rules`
    - looking up the `column_rules` key for the current row and calling the corresponding `column_rules` value.
	
`column_rules` values must be callables which are responsible for generating and returning a graph for merging. Note that rules actually don't need to return an instance of `rdflib.Graph` (e.g. if a rule just accesses `DFgraphConverter.store`; for an example of state sharing between rules see [below](https://github.com/lu-pl/rdfdf#more-involved-example)), in which case the result is skipped in the generator. 

`column_rules` values must be callables of arity 3; 
for every field for which a rule applies 
- the subject field value (specified in the `subject_column` parameter and possibly computed by `subject_rule` of `DFGraphConverter`), 
- the object field value (i.e. the current field value) and 
- `DFGraphConverter.store` (a class level attribute for state sharing between rules *and* `DFGraphConverter` instances)

get passed to the respective rule callable (see examples below).

#### Parameters:

- **dataframe**: A pandas.DataFrame to be converted.

- **subject_column**: Selects a table column by name to be regarded as the column of triple subjects.

- **subject_rule**: Optional; either a `Callable[[str], URIRef]` or an `rdflib.Namespace` which gets applied to every field of the subject_column; 
if supplied, `subject_field` in the `column_rules` will be what `subject_rule` computes it to be; otherwise `subject_field` will be just the raw field value of the current `subject_column` and must be handled manually in order to be become a valid triple subject (i.e. a URIRef).

- **column_rules**: A mapping of column names to callables responsible for creating subgraphs ('field graphs').

- **graph**: Optional; allows to set the internal rdflib.Graph component.

## Examples:

### Simple example

```python
import pandas as pd

from rdfdf.rdfdf import DFGraphConverter

from rdflib import URIRef, Graph, Namespace, Literal
from rdflib.namespace import RDF


# namespace definitions
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")

# bind namespace to graph component
nsgraph = Graph()
nsgraph.bind("crm", CRM)

# create a simple dataframe
table = [
    {
        "id": "rem",
        "full_title": "Reference corpus Middle High German"
    }
]

df = pd.DataFrame(data=table)


# rules
def full_title_rule(subject_field, object_field, store):

    title_uri = URIRef(f"https://{subject_field}.clscor.io/entity/corpus/title/full")
    corpus_uri = URIRef(f"https://{subject_field}.clscor.io/entity/corpus")

    triples = [
        (
            title_uri,
            RDF.type,
            CRM.E41_Appellation
        ),
        (
            title_uri,
            CRM.P1_identifies,
            corpus_uri
        ),
        # inverse
        (
            corpus_uri,
            CRM.P1_is_identified_by,
            title_uri
        ),
        (
            title_uri,
            CRM.P2_has_type,
            URIRef("https://core.clscor.io/entity/type/title/full")
        ),
        (
            title_uri,
            CRM['190_has_symbolic_content'],
            Literal(object_field)
        ),
    ]

    graph = Graph()

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
    graph=nsgraph
)

graph = dfgraph.to_graph()
print(graph.serialize(format="ttl"))
```

Output:

```ttl
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .

<https://rem.clscor.io/entity/corpus> crm:P1_is_identified_by <https://rem.clscor.io/entity/corpus/title/full> .

<https://rem.clscor.io/entity/corpus/title/full> a crm:E41_Appellation ;
    crm:190_has_symbolic_content "Reference corpus Middle High German" ;
    crm:P1_identifies <https://rem.clscor.io/entity/corpus> ;
    crm:P2_has_type <https://core.clscor.io/entity/type/title/full> .
```

### More involved example
For a more involved application of `rdfdf` (including extensive state sharing between rules) see the [CorTab](https://github.com/lu-pl/cortab) script.

## Contribution

Please feel free to open issues or pull requests.

