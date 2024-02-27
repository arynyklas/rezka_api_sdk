from enum import Enum as _Enum, auto as enum_auto


class BaseEnum(str, _Enum):
    def _generate_next_value_(name: str, *_):
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
