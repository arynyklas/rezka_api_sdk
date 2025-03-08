class RezkaAPIException(Exception):
    def __init__(self, status_code: int, description: str | None) -> None:
        self.status_code = status_code
        self.description = description

    def __str__(self) -> str:
        return "Rezka API error: {}, {}".format(
            self.status_code,
            self.description
        )

    __repr__ = __str__
