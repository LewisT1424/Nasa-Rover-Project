from typing import TypedDict, NotRequired

class ManifestParams(TypedDict):
    api_key: str

class SolParams(TypedDict):
    sol: NotRequired[int]
    camera: NotRequired[str]
    page: NotRequired[int]
    api_key: str