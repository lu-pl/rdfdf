# rdfdf

rdfdf - Functionality for rule-based pandas.DataFrame/rdflib.Graph conversion.

For representation of tabular data in rdf see Allemang, Hendler: Semnantic Web for the Working Ontologist. 2011, 40ff.

> This project is in an early stage of development and should be used with caution

## Requirements

* python >= 3.10

## Usage

For now rdfdf provides a `DFGraphConverter` class for rule-based pandas.DataFrame to rdflib.Graph conversion. 

A `GraphDFConverter` class for rule-based rdflib.Graph to pandas.DataFrame conversion will be implemented shortly.

### DFGraphConverter

Unlike [rdfpandas](https://github.com/cadmiumkitty/rdfpandas/) which requires URIRefs as column headers (and otherwise creates invalid rdf with e.g. literals as predicates etc.), rdfdf computes URIRefs (or Literals for triple objects) based on rules.

### GraphDFConverter
todo

## Contribution

Please feel free to open issues or pull requests.

