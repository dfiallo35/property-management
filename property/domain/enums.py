from enum import Enum


class ConfigurationType(str, Enum):
    SELECT = "select"
    TEXT = "text"
    NUMBER = "number"
