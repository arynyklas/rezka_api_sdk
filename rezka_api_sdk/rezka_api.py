import httpx

from . import models, constants
from .exceptions import RezkaAPIException


class HTTPMethods:
    GET: str = "GET"
    POST: str = "POST"


class RezkaAPI:
    API_URL: str = constants.API_URL
    SSL_VERIFY_NEEDED: bool = constants.SSL_VERIFY_NEEDED

    def __init__(self, api_key: str, **http_client_kwargs) -> None:
        self._http_client: httpx.AsyncClient = httpx.AsyncClient(
            headers = {
                "Authorization": "Bearer {}".format(api_key)
            },
            verify = self.SSL_VERIFY_NEEDED,
            **http_client_kwargs
        )

    async def _request(self, http_method: str, method: str, params: dict | None=None, json: dict | None=None, **kwargs) -> dict:
        response: httpx.Response = await self._http_client.request(
            method = http_method,
            url = self.API_URL + method,
            params = params,
            json = json,
            **kwargs
        )

        response_raw_data: dict | str

        try:
            response_raw_data = response.json()
        except Exception:
            response_raw_data = response.text

        if response.status_code != 200:
            description: str = None

            if isinstance(response_raw_data, dict):
                description = response_raw_data.get("description")

            if not description:
                description = response_raw_data

            raise RezkaAPIException(
                status_code = response.status_code,
                description = description
            )

        return response_raw_data

    async def get_me(self) -> models.UserModel:
        response_data: dict = await self._request(
            http_method = HTTPMethods.GET,
            method = "me"
        )

        return models.UserModel.model_validate(response_data)

    async def search(self, query: str) -> list[models.SearchResultModel]:
        response_data: dict = await self._request(
            http_method = HTTPMethods.GET,
            method = "search",
            params = dict(
                query = query
            )
        )

        return [
            models.SearchResultModel.model_validate(raw_search_result)
            for raw_search_result in response_data["results"]
        ]

    async def get_info_and_translators(self, url: str) -> tuple[models.ShortInfoModel, list[models.TranslatorInfoModel]]:
        response_data: dict = await self._request(
            http_method = HTTPMethods.GET,
            method = "info_and_translators",
            params = dict(
                url = url
            )
        )

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
            id: int | None=None,
            url: str | None=None,
            season_id: str | None=None,
            episode_id: str | None=None,
    ) -> models.DirectURLsModel:
        request_data: dict = dict(
            translator_id = translator_id,
            is_film = is_film,
            translator_additional_arguments = translator_additional_arguments
        )

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

        response_data: dict = await self._request(
            http_method = HTTPMethods.POST,
            method = "direct_urls",
            json = request_data
        )

        return models.DirectURLsModel.model_validate(response_data)
