import asyncio
import typing

from rezka_api_sdk import RezkaAPI, RezkaAPIException, enums


class ShortInfoAttrsTexts:
    original_title = " ({})"
    age            = "[{}]"
    rating         = "  - {source} - {rating}"
    slogan         = "\nSlogan: {}"
    release_date   = "\nRelease date: {}"
    country        = "\nCountry: {}"
    director       = "\nDirector: {}"
    genre          = "\nGenre: {}"


def short_info_value(key: str, format_value: str | None) -> str:
    if not format_value:
        return ""

    return getattr(ShortInfoAttrsTexts, key).format(format_value)


def input_int(prompt: str, min_value: int, max_value: int) -> int:
    prompt = "> " + prompt

    while True:
        try:
            value = int(input(prompt).strip())

            if min_value <= value <= max_value:
                return value

        except ValueError:
            pass

        print("Invalid value. Please enter a number from {} to {}".format(min_value, max_value))

def input_from_list(prompt: str, items: typing.Iterable[str]) -> str:
    prompt = "> " + prompt

    while True:
        value = input(prompt).strip()

        if value in items:
            return value

        print("Invalid value. Please enter one of the following: {}".format(", ".join(items)))


table_format = "rounded_grid"


async def main() -> None:
    try:
        from tabulate import tabulate  # type: ignore

    except ImportError:
        print("Please install dev dependencies to run this example")

        return

    while True:
        api_key = input("API Key: ").strip()

        if not api_key:
            continue

        rezka_api = RezkaAPI(api_key)

        try:
            me_response = await rezka_api.get_me()

        except RezkaAPIException as ex:
            if ex.status_code == 403:
                print("Invalid API key!")

                continue

            raise

        break

    print("Authorized as user with owner Telegram ID: {}".format(me_response.tg_id) + "\n")

    search_results = await rezka_api.search(
        query = input("Search query: ")
    )

    print()

    print(tabulate(
        [
            (number, search_result.id, search_result.entity_type.value, search_result.title, search_result.url)
            for number, search_result in enumerate(search_results, 1)
        ],
        headers = ["Number", "ID", "Entity type", "Title", "URL"],
        tablefmt = table_format
    ))

    search_result = search_results[input_int(
        prompt = "Select search result by number: ",
        min_value = 1,
        max_value = len(search_results)
    ) - 1]

    url = search_result.url

    print()

    short_info, translators = await rezka_api.get_info_and_translators(url)

    print((
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
    ))

    print()

    print(tabulate(
        [
            (number, translator.id, translator.title)
            for number, translator in enumerate(translators, 1)
        ],
        headers = ["Number", "ID", "Translator title"],
        tablefmt = table_format
    ))

    translator = translators[input_int(
        prompt = "Select translator by number: ",
        min_value = 1,
        max_value = len(translators)
    ) - 1]

    print()

    is_film = search_result.entity_type == enums.EntityTypeEnum.films

    item_id = search_result.id
    translator_id = translator.id

    direct_urls = await rezka_api.get_direct_urls(
        id = item_id,
        translator_id = translator_id,
        is_film = is_film,
        translator_additional_arguments = translator.additional_arguments
    )

    season_id: str | None = None
    episode_id: str | None = None

    if direct_urls.seasons and direct_urls.episodes:
        print(tabulate(
            [
                (season_id, season_title)
                for season_id, season_title in direct_urls.seasons.items()
            ],
            headers = ["ID", "Season"],
            tablefmt = table_format
        ))

        season_id = input_from_list(
            prompt = "Select season by id: ",
            items = direct_urls.seasons.keys()
        )

        print()

        print(tabulate(
            [
                (episode_id, episode_title)
                for episode_id, episode_title in direct_urls.episodes[season_id].items()
            ],
            headers = ["ID", "Episode"],
            tablefmt = table_format
        ))

        episode_id = input_from_list(
            prompt = "Select episode by id: ",
            items = direct_urls.episodes[season_id].keys()
        )

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
        print("Direct URLs:")

        for quelity, direct_url in reversed(direct_urls.urls.items()):
            print("\t" + f"{quelity}: {direct_url}")

        print()

    if direct_urls.subtitles:
        print("Subtitles:")

        for subtitle_name, subtitle_url in direct_urls.subtitles.items():
            print("\t" + f"{subtitle_name}: {subtitle_url}")

    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
