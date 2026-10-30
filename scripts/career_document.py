"""Load the canonical YAML career database without losing duplicate-key errors."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class CareerDocumentError(RuntimeError):
    """Raised when a career YAML document cannot be loaded safely."""


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_mapping(
    loader: UniqueKeyLoader,
    node: yaml.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as error:
            raise CareerDocumentError(
                f"invalid unhashable mapping key at line {key_node.start_mark.line + 1}"
            ) from error
        if duplicate:
            raise CareerDocumentError(
                f"duplicate key {key!r} at line {key_node.start_mark.line + 1}"
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


def load_document(path: Path) -> dict[str, Any]:
    """Load a career YAML file and require a mapping at its root."""
    try:
        document = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except CareerDocumentError:
        raise
    except (OSError, yaml.YAMLError) as error:
        raise CareerDocumentError(f"invalid career YAML: {error}") from error
    if document is None:
        return {}
    if not isinstance(document, dict):
        raise CareerDocumentError("career database must be a YAML mapping")
    return document
