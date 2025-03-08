from enum import Enum as _Enum, auto as enum_auto

import typing


class BaseEnum(str, _Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[typing.Any]) -> str:
        return name.lower()


class SubscriptionEnum(BaseEnum):
    basic = enum_auto()
    silver = enum_auto()
    golden = enum_auto()
    platinum = enum_auto()
    custom = enum_auto()


class EntityTypeEnum(BaseEnum):
    films = enum_auto()
    series = enum_auto()
    animation = enum_auto()
    cartoons = enum_auto()
