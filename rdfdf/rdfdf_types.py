"""Type definition for rdfdf"""

from collections.abc import Callable, MutableMapping
from typing import Any

from rdflib import Graph, URIRef, Literal

_Rule = Callable[[Any, Any, MutableMapping], Graph]
_RulesMapping = MutableMapping[str, _Rule]
_TripleObject = URIRef | Literal
_Triple = tuple[URIRef, URIRef, _TripleObject]
