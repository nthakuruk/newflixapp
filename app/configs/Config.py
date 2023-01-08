import os

import yaml

from utils.Singleton import Singleton


class Config(metaclass=Singleton):
    def __init__(self):
        with open(os.path.join("configs", "config.yaml"), 'r') as stream:
            self.__dict__.update(yaml.safe_load(stream))
