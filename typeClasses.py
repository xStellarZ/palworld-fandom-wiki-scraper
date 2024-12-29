from typing import TypedDict, List


class PalSimple(TypedDict):
    id: str
    name: str


class Suitability(TypedDict):
    type: str
    image: str
    level: int


class PartnerSkill(TypedDict):
    name: str
    icon: str
    description: str


class Elements(TypedDict):
    name: str
    image: str


class Skills(TypedDict):
    level: int
    name: str
    type: str
    cooldown: int
    power: int
    description: str


class PalDetail(TypedDict):
    id: int
    key: str
    image: str
    name: str
    wiki: str
    types: List[Elements]
    imageWiki: str
    suitability: List[Suitability]
    drops: List[str]
    aura: PartnerSkill
    description: str
    skills: List[Skills]
