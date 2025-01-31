import json


from typing import Dict, Any, Union


from gendiff.types import Node, NodeType


INDENT = "    "


def stringify_value(value: Union[Any, Dict], depth: int) -> str:
    if isinstance(value, Dict):
        result = ["{"]
        for key_, value_ in sorted(value.items()):
            result.append(
                f"{INDENT * (depth + 1)}{key_}: "
                f"{stringify_value(value_, depth + 1)}"
            )
        result.append(f"{INDENT * depth}}}")
        return "\n".join(result)
    return value \
        if isinstance(value, str) else json.JSONEncoder().encode(value)


def stringify_node(key: str, value: Node, depth: int) -> str:
    if value.status == NodeType.UNCHANGED:
        return f"{INDENT * depth}{key}: {stringify_value(value.value, depth)}"

    elif value.status == NodeType.NESTED:
        result = [f"{INDENT * depth}{key}: {{"]
        for key_, value_ in sorted(value.value.items()):
            result.append(stringify_node(key_, value_, depth + 1))
        result.append(f"{INDENT * depth}}}")
        return "\n".join(result)

    elif value.status in (
        NodeType.REMOVED,
        NodeType.ADDED,
        NodeType.CHANGED,
    ):
        result = []
        marks = tuple(value.status.value)
        values = (
            value.value if isinstance(value.value, tuple) else (value.value,)
        )
        for mark, value_ in zip(marks, values):
            result.append(
                f"{INDENT * (depth - 1)}  {mark} {key}: "
                f"{stringify_value(value_, depth)}"
            )
        return "\n".join(result)


def to_stylish(diff_dict: Dict[str, Node]) -> str:
    result = ["{"]
    for key in sorted(diff_dict.keys()):
        result.append(stringify_node(key, diff_dict[key], 1))
    result.append("}")
    return "\n".join(result)
