from typing import List
from helpers import getPalNames, getPalByName
from typeClasses import PalDetail
import pydash
import json
import os

pals = getPalNames()

palInfos: List[PalDetail] = []


def getPal(pal, index):
    palInfos.append(getPalByName(pal.get("name"), index))


for index, pal in enumerate(pals, start=1):
    getPal(pal, index)

if len(palInfos):
    filename = "./result/pals.json"
    print(os.path.dirname(filename))
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        palInfos = [info for info in palInfos if info and info.get("key") is not None]
        jsonData = json.dumps(pydash.sort_by(palInfos, "key"), indent=2)
        file.write(jsonData)
