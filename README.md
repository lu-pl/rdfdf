# rdfdf

rdfdf - Functionality for *rule-based* `pandas.DataFrame` - `rdflib.Graph` conversion.

For representation of tabular data in RDF see Allemang, Hendler: Semantic Web for the Working Ontologist. 2011, 40ff.

> This project is in an early stage of development and should be used with caution

## Requirements

* python >= 3.10

## Usage

For now rdfdf provides a `DFGraphConverter` class for rule-based pandas.DataFrame to rdflib.Graph conversion. 

A `GraphDFConverter` class for rule-based `rdflib.Graph` to `pandas.DataFrame` conversion will be implemented shortly.

### DFGraphConverter

Unlike [rdfpandas](https://github.com/cadmiumkitty/rdfpandas/) which requires URIRefs as column headers (and otherwise just creates invalid RDF with e.g. literals as predicates), rdfdf computes URIRefs (or Literals for triple objects) based on rules.

DFGraphConverter iterates over a dataframe and constructs RDF triples by
- for every row
  - for every rule in field_rules
    - looking up the field_rules key for the current row and creating a predicate-object pair from the field_rules value
     - applying the subject_rule to the subject_column field of the current row and adding the subject to the predicate-object pair.
	 
Since what triples actually are created is dependent on the field_rules, also partial table conversion is possible.

`./tests/test_data/test.csv`
```
```

```	
from rdfdf import DFGraphConverter
```	

### GraphDFConverter
todo

## Contribution

Please feel free to open issues or pull requests.

