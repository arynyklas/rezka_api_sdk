from enum import Enum, auto as enum_auto
from httpx import AsyncClient

import typing

from . import models
from .exceptions import RezkaAPIException


DICT_STR_ANY_T = dict[str, typing.Any]


class HTTPMethods(Enum):
    GET = enum_auto()
    POST = enum_auto()


class RezkaAPI:
    API_URL = "https://rezka_api.sek.su/api/"
    SSL_VERIFY_NEEDED = False

    def __init__(self, api_key: str, **http_client_kwargs: typing.Any) -> None:
        self._http_client = AsyncClient(
            headers = {
                "Authorization": "Bearer {}".format(api_key)
            },
            verify = self.SSL_VERIFY_NEEDED,
            **http_client_kwargs  # type: ignore
        )

    async def _request(
        self,
        http_method: HTTPMethods,
        method: str,
        params: DICT_STR_ANY_T | None = None,
        json: DICT_STR_ANY_T | None = None,
        **kwargs: typing.Any
    ) -> DICT_STR_ANY_T | str:
        response = await self._http_client.request(
            method = http_method.name,
            url = self.API_URL + method,
            params = params,
            json = json,
            **kwargs
        )

        response_raw_data: DICT_STR_ANY_T | str

        try:
            response_raw_data = response.json()
        except Exception:
            response_raw_data = response.text

        if response.status_code != 200:
            description: str | None = None

            if isinstance(response_raw_data, dict):
                description = response_raw_data.get("description")

            if not description and isinstance(response_raw_data, str):
                description = response_raw_data

            raise RezkaAPIException(
                status_code = response.status_code,
                description = description
            )

        return response_raw_data

    async def get_me(self) -> models.UserModel:
        response_data = typing.cast(DICT_STR_ANY_T, await self._request(
            http_method = HTTPMethods.GET,
            method = "me"
        ))

        return models.UserModel.model_validate(response_data)

    async def search(self, query: str) -> list[models.SearchResultModel]:
        response_data = typing.cast(DICT_STR_ANY_T, await self._request(
            http_method = HTTPMethods.GET,
            method = "search",
            params = {
                "query": query
            }
        ))

        return [
            models.SearchResultModel.model_validate(raw_search_result)
            for raw_search_result in response_data["results"]
        ]

    async def get_info_and_translators(self, url: str) -> tuple[models.ShortInfoModel, list[models.TranslatorInfoModel]]:
        response_data = typing.cast(DICT_STR_ANY_T, await self._request(
            http_method = HTTPMethods.GET,
            method = "info_and_translators",
            params = dict(
                url = url
            )
        ))

        return (
            models.ShortInfoModel.model_validate(response_data["short_info"]),
            [
                models.TranslatorInfoModel.model_validate(raw_translator_info)
                for raw_translator_info in response_data["translators"]
            ]
        )

    async def get_direct_urls(
        self,
        translator_id: str,
        is_film: bool,
        translator_additional_arguments: dict[str, str],
        id: int | str | None=None,
        url: str | None=None,
        season_id: int | str | None=None,
        episode_id: int | str | None=None
    ) -> models.DirectURLsModel:
        request_data: DICT_STR_ANY_T = {
            "translator_id": translator_id,
            "is_film": is_film,
            "translator_additional_arguments": translator_additional_arguments
        }

        if id:
            request_data["id"] = id
        elif url:
            request_data["url"] = url
        else:
            raise ValueError("Needed to pass item's id or url")

        if not is_film:
            if season_id:
                request_data["season_id"] = season_id

            if episode_id:
                if not season_id:
                    raise ValueError("Needed to pass season_id with episode_id")

                request_data["episode_id"] = episode_id

        response_data = typing.cast(DICT_STR_ANY_T, await self._request(
            http_method = HTTPMethods.POST,
            method = "direct_urls",
            json = request_data
        ))

        return models.DirectURLsModel.model_validate(response_data)
