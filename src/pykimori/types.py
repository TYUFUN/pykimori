from typing import TypedDict, List, Optional
class DateInfo(TypedDict, total=False):
    year: Optional[int]
    month: Optional[int]
    day: Optional[int]
    date: Optional[str]
class Poster(TypedDict, total=False):
    id: str
    originalUrl: str
    mainUrl: str
class Genre(TypedDict, total=False):
    id: str
    name: str
    russian: str
    kind: str
class Studio(TypedDict, total=False):
    id: str
    name: str
    imageUrl: str
class ExternalLink(TypedDict, total=False):
    id: str
    kind: str
    url: str
    createdAt: str
    updatedAt: str
class Character(TypedDict, total=False):
    id: str
    name: str
    poster: Poster
class CharacterRole(TypedDict, total=False):
    id: str
    rolesRu: List[str]
    rolesEn: List[str]
    character: Character
class Anime(TypedDict, total=False):
    id: str
    malId: Optional[str]
    name: str
    russian: Optional[str]
    licenseNameRu: Optional[str]
    english: Optional[str]
    japanese: Optional[str]
    synonyms: List[str]
    kind: str
    rating: str
    score: float
    status: str
    episodes: int
    episodesAired: int
    duration: int
    airedOn: DateInfo
    releasedOn: DateInfo
    url: str
    season: str
    poster: Poster
    fansubbers: List[str]
    fandubbers: List[str]
    licensors: List[str]
    createdAt: str
    updatedAt: str
    nextEpisodeAt: Optional[str]
    isCensored: bool
    genres: List[Genre]
    studios: List[Studio]
    externalLinks: List[ExternalLink]
    characterRoles: List[CharacterRole]
    description: Optional[str]
    descriptionHtml: Optional[str]
    descriptionSource: Optional[str]