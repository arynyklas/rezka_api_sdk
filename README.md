# Rezka API SDK

[![PyPI Version](https://img.shields.io/pypi/v/rezka_api_sdk.svg)](https://pypi.org/project/rezka_api_sdk/)
[![Python Version](https://img.shields.io/pypi/pyversions/rezka_api_sdk.svg)](https://pypi.org/project/rezka_api_sdk/)

SDK for unofficial Rezka API.
Details about API [at Telegram](https://t.me/aryn_dev/138).


## Installation

You can install `rezka_api_sdk` using pip:

```bash
pip install rezka_api_sdk
```


## Usage

```python
from rezka_api_sdk import RezkaAPI, models

# Init API client
rezka_api = RezkaAPI("<your API key>")

# Get me, returns `models.UserModel`
await rezka_api.get_me()

# Search items, returns `list[SearchResultModel]`
await rezka_api.search("Top Gun: Maverick")

# Get short info about item and available translators, returns `tuple[ShortInfoModel, list[TranslatorInfoModel]]`
await rezka_api.get_info_and_translators("http://hdrezka1tqbbd.org/films/action/47946-top-gan-meverik-2022.html")


# Get direct urls
# NOTE: allowed to pass item's ID or URL
# Acceptable key arguments:
# 
# translator_id: int; required;
# is_film: bool; required;
# translator_additional_arguments: dict;  required; you can get it from `models.TranslatorInfoModel.additional_arguments`


# For films:
await rezka_api.get_direct_urls(
    id = 47946,
    translator_id = 56,
    is_film = True,
    translator_additional_arguments = {}
)


# For series:
await rezka_api.get_direct_urls(
    id = 646, # Breaking bad
    translator_id = 56,
    is_film = False,
    translator_additional_arguments = {},
    season_id = "1",
    episode_id = "1"
)
```

For user-friendly CLI example see [cli_example.py](cli_example.py).


## Stay updated

For the latest news and updates, follow my [Telegram Channel](https://t.me/aryn_dev).
