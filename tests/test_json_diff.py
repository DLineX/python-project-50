from functools import partial


import pytest


from pytest import fixture


from gendiff.gendiff import generate_diff


from gendiff.views import JSON


from tests.fixture_paths import (
    JSON1_PATH,
    JSON2_PATH,
    YAML1_PATH,
    YAML2_PATH,
    EMPTY_YAML_PATH,
    EMPTY_JSON_PATH,
)

generate_diff = partial(generate_diff, format=JSON)


@fixture()
def expected_diff_for_file1_and_file2():
    return """{
    "common": {
        "follow": [
            "NodeType.ADDED",
            false
        ],
        "setting1": "Value 1",
        "setting2": [
            "NodeType.REMOVED",
            200
        ],
        "setting3": [
            "NodeType.CHANGED",
            [
                true,
                null
            ]
        ],
        "setting4": [
            "NodeType.ADDED",
            "blah blah"
        ],
        "setting5": [
            "NodeType.ADDED",
            {
                "key5": "value5"
            }
        ],
        "setting6": {
            "doge": {
                "wow": [
                    "NodeType.CHANGED",
                    [
                        "",
                        "so much"
                    ]
                ]
            },
            "key": "value",
            "ops": [
                "NodeType.ADDED",
                "vops"
            ]
        }
    },
    "group1": {
        "baz": [
            "NodeType.CHANGED",
            [
                "bas",
                "bars"
            ]
        ],
        "foo": "bar",
        "nest": [
            "NodeType.CHANGED",
            [
                {
                    "key": "value"
                },
                "str"
            ]
        ]
    },
    "group2": [
        "NodeType.REMOVED",
        {
            "abc": 12345,
            "deep": {
                "id": 45
            }
        }
    ],
    "group3": [
        "NodeType.ADDED",
        {
            "deep": {
                "id": {
                    "number": 45
                }
            },
            "fee": 100500
        }
    ]
}"""


@fixture()
def expected_diff_for_file1_and_empty():
    return """{
    "common": [
        "NodeType.REMOVED",
        {
            "setting1": "Value 1",
            "setting2": 200,
            "setting3": true,
            "setting6": {
                "doge": {
                    "wow": ""
                },
                "key": "value"
            }
        }
    ],
    "group1": [
        "NodeType.REMOVED",
        {
            "baz": "bas",
            "foo": "bar",
            "nest": {
                "key": "value"
            }
        }
    ],
    "group2": [
        "NodeType.REMOVED",
        {
            "abc": 12345,
            "deep": {
                "id": 45
            }
        }
    ]
}"""


@pytest.mark.parametrize(
    "path_to_file1,path_to_file2",
    [(JSON1_PATH, JSON2_PATH), (YAML1_PATH, YAML2_PATH)],
)
def test_gendiff_file1_and_file2(
    path_to_file1, path_to_file2, expected_diff_for_file1_and_file2
):
    diff = generate_diff(path_to_file1, path_to_file2)
    assert diff == expected_diff_for_file1_and_file2


@pytest.mark.parametrize(
    "path_to_file1,path_to_file2",
    [(JSON1_PATH, EMPTY_JSON_PATH), (YAML1_PATH, EMPTY_YAML_PATH)],
)
def test_gendiff_file1_and_empty(
    path_to_file1, path_to_file2, expected_diff_for_file1_and_empty
):
    diff = generate_diff(path_to_file1, path_to_file2)
    assert diff == expected_diff_for_file1_and_empty
