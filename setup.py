import pathlib
import re
import sys
import setuptools


LIBRARY_NAME = "rezka_api_sdk"

WORK_DIR = pathlib.Path(__file__).parent

MINIMAL_PY_VERSION = (3, 10)

MINIMAL_PY_VERSION_STR = ".".join(
    map(str, MINIMAL_PY_VERSION)
)

if sys.version_info < MINIMAL_PY_VERSION:
    raise RuntimeError(
        "{} works only with Python {}+".format(
            LIBRARY_NAME,
            MINIMAL_PY_VERSION_STR
        )
    )


def get_version():
    return re.findall(
        pattern = r"^__version__ = \"([^']+)\"\r?$",
        string = (WORK_DIR / LIBRARY_NAME / "__init__.py").read_text("utf-8"),
        flags = re.MULTILINE
    )[0]


setuptools.setup(
    name = LIBRARY_NAME,
    version = get_version(),
    packages = setuptools.find_packages(
        exclude = [
            "examples.*"
        ]
    ),
    url = "https://github.com/arynyklas/{}".format(LIBRARY_NAME),
    author = "Aryn Yklas",
    python_requires = ">={}".format(MINIMAL_PY_VERSION_STR),
    author_email = "arynyklas@gmail.com",
    description = "It is a library that allows you to interact with unofficial HDRezka API",
    long_description = (WORK_DIR / "README.md").read_text("utf-8"),
    long_description_content_type = "text/markdown",
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: {}".format(MINIMAL_PY_VERSION_STR)
    ],
    install_requires = [
        "httpx"
    ],
    include_package_data = False,
    keywords = [
        "rezka",
        "hdrezka",
        "films",
        "series"
    ]
)
