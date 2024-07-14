import json


from typing import Dict, Any, Tuple, List, ItemsView


from gendiff.types import Node, NodeType


VALUE = 1


def get_sorted_nodes_with_changes(
    nodes: ItemsView[str, Node]
) -> List[Tuple[str, Node]]:
    return [
        (key, value)
        for (key, value) in sorted(nodes)
        if value.status != NodeType.UNCHANGED
    ]


def stringify_value(value: Any) -> str:
    if isinstance(value, Dict):
        return "[complex value]"
    return (
        f"'{value}'"
        if isinstance(value, str)
        else json.JSONEncoder().encode(value)
    )


def stringify_node(key_path: str, value: Node) -> str:
    if value.status == NodeType.CHANGED:
        from_, to_ = map(stringify_value, value.value)
        return f"Property '{key_path}' was updated. From {from_} to {to_}"
    elif value.status == NodeType.ADDED:
        return (
            f"Property '{key_path}' was "
            f"added with value: {stringify_value(value.value)}"
        )
    elif value.status == NodeType.REMOVED:
        return f"Property '{key_path}' was removed"
    elif value.status == NodeType.NESTED:
        result = []
        for key_, value_ in get_sorted_nodes_with_changes(value.value.items()):
            key_path_ = ".".join((key_path, key_))
            result.append(stringify_node(key_path_, value_))
        return "\n".join(result)


def to_plain(diff_dict: Dict[str, Node]) -> str:
    return "\n".join(
        [
            stringify_node(key, value)
            for key, value in get_sorted_nodes_with_changes(diff_dict.items())
        ]
    )
