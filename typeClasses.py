from typing import TypedDict, List


class PalSimple(TypedDict):
    id: str
    name: str


class Suitability(TypedDict):
    kindling: int
    watering: int
    planting: int
    generatingElectricity: int
    handiwork: int
    gathering: int
    lumbering: int
    mining: int
    medicineProduction: int
    cooling: int
    transporting: int
    farming: int


class PartnerSkill(TypedDict):
    name: str
    icon: str
    description: str


class PalDetail(TypedDict):
    id: str
    name: str
    elements: List[str]
    drops: List[str]
    foods: int
    suitability: Suitability
    image: str
    partnerSkill: PartnerSkill
