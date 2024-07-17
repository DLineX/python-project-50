import json


from pathlib import Path


from typing import Union, Dict, Any


from yaml import load, FullLoader


def get_extension(path: Union[str, Path]) -> str:
    return str(path).split(".")[-1]


def parse(data: str, extension: str) -> Dict[str, Any]:
    if extension in ("yml", "yaml"):
        return load(data, Loader=FullLoader) or {}
    if extension == "json":
        return json.loads(data)
    raise RuntimeError("Unknown file format")
