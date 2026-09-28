from typing import TypedDict, Optional, List


class Anime(TypedDict, total=False):
    id: str
    malId: Optional[str]
    name: str
    russian: Optional[str]
    english: Optional[str]
    japanese: Optional[str]