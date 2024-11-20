from pydantic import BaseModel, Field

from . import enums


class UserSubscriptionModel(BaseModel):
    type: enums.SubscriptionEnum
    end_timestamp: int

class UserModel(BaseModel):
    id: str
    tg_id: int
    subscription: UserSubscriptionModel | None


class SearchResultModel(BaseModel):
    id: str
    title: str
    image_url: str
    addition: str
    url: str
    entity_type: enums.EntityTypeEnum


class ShortInfoRatingModel(BaseModel):
    source: str
    rating: str

class ShortInfoModel(BaseModel):
    OPTIONAL_STRING_FIELDS_NAMES: list[str] = Field(
        default = [
            "original_title",
            "age",
            "slogan",
            "release_date",
            "country",
            "director",
            "genre"
        ],
        exclude = True,
        repr = False
    )

    is_film: bool | None
    title: str
    original_title: str | None
    is_finished: bool | None
    description: str | None
    age: str | None
    ratings: list[ShortInfoRatingModel]
    slogan: str | None
    release_date: str | None
    country: str | None
    director: str | None
    genre: str | None
    cast_of_actors: list[str]


class TranslatorInfoModel(BaseModel):
    id: str
    title: str
    additional_arguments: dict[str, str]


class DirectURLsModel(BaseModel):
    seasons: dict[str, str] | None
    episodes: dict[str, dict[str, str]] | None
    urls: dict[str, str] | None
    subtitles: dict[str, str] | None
    subtitle_languages: dict[str, str] | None
