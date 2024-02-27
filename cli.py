import asyncio

from rezka_api_sdk import RezkaAPI, models, enums


class ShortInfoAttrsTexts:
    original_title: str = " ({})"
    age: str = "[{}]"
    rating: str = "  - {source} - {rating}"
    slogan: str = "\nSlogan: {}"
    release_date: str = "\nRelease date: {}"
    country: str = "\nCountry: {}"
    director: str = "\nDirector: {}"
    genre: str = "\nGenre: {}"


def short_info_value(key: str, format_value: str | None) -> str:
    if not format_value:
        return ""

    return getattr(ShortInfoAttrsTexts, key).format(format_value)


async def main() -> None:
    from prettytable import PrettyTable

    rezka_api = RezkaAPI("<your API key>")

    pt = PrettyTable()

    search_results = await rezka_api.search(
        query = input("Search query: ")
    )

    print()

    pt.field_names = ["index", "id", "entity_type", "title", "url"]

    pt.add_rows([
        [index, search_result.id, search_result.entity_type.value, search_result.title, search_result.url]
        for index, search_result in enumerate(search_results, 0)
    ])

    print(pt)

    pt.clear()

    search_result = search_results[int(input("Select search result by index: "))]
    url = search_result.url

    print()

    short_info, translators = await rezka_api.get_info_and_translators(url)

    print(
        (
            "Short info:\n"
            "Title: {title}{original_title} {age}\n"
            "Ratings:\n"
            "{ratings}{slogan}{release_date}{country}{director}{genre}"
        ).format(
            title = short_info.title,
            ratings = "\n".join([
                ShortInfoAttrsTexts.rating.format(
                    source = rating.source,
                    rating = rating.rating
                )
                for rating in short_info.ratings
            ]),
            **{
                field_name: short_info_value(
                    key = field_name,
                    format_value = getattr(short_info, field_name)
                )
                for field_name in short_info.OPTIONAL_STRING_FIELDS_NAMES
            }
        )
    )

    print()

    pt.field_names = ["index", "id", "translator"]

    pt.add_rows([
        [index, translator.id, translator.title]
        for index, translator in enumerate(translators, 0)
    ])

    print(pt)

    pt.clear()

    translator: models.TranslatorInfoModel = translators[int(input("Select translator by index: "))]
    print()

    is_film: bool = search_result.entity_type == enums.EntityTypeEnum.films

    item_id: str = search_result.id
    translator_id: str = translator.id

    direct_urls: models.DirectURLsModel = await rezka_api.get_direct_urls(
        id = item_id,
        translator_id = translator_id,
        is_film = is_film,
        translator_additional_arguments = translator.additional_arguments
    )

    season_id: str | None = None
    episode_id: str | None = None

    if direct_urls.seasons or direct_urls.episodes:
        pt.field_names = ["id", "season"]

        pt.add_rows([
            [season_id, season_title]
            for season_id, season_title in direct_urls.seasons.items()
        ])

        print(pt)

        pt.clear()

        season_id = input("Select season by id: ")
        print()

        pt.field_names = ["id", "episode"]

        pt.add_rows([
            [episode_id, episode_title]
            for episode_id, episode_title in direct_urls.episodes[season_id].items()
        ])

        print(pt)

        pt.clear()

        episode_id = input("Select episode by id: ")
        print()

    if season_id or episode_id:
        direct_urls = await rezka_api.get_direct_urls(
            id = item_id,
            translator_id = translator_id,
            is_film = is_film,
            translator_additional_arguments = translator.additional_arguments,
            season_id = season_id,
            episode_id = episode_id
        )

    if direct_urls.urls:
        for quelity, direct_url in direct_urls.urls.items():
            print("{}: {}".format(
                quelity,
                direct_url
            ))

        print()

    if direct_urls.subtitles:
        print("Subtitles:")

        for subtitle_name, subtitle_url in direct_urls.subtitles.items():
            print("\t{}: {}".format(
                subtitle_name,
                subtitle_url
            ))


asyncio.run(main())
