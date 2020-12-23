import yaml
from typing import Dict


def parse_from_file(path: str) -> Dict:
    config = None
    if path.endswith(".yaml"):
        return parse_from_yaml(path)
    return config


def parse_from_yaml(path: str) -> Dict:
    with open(path, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)

    return config
