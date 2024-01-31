from typing import List
from helpers import getPalNames, getPalByName
from typeClasses import PalDetail
import concurrent.futures
import pydash
import json
import os

pals = getPalNames()

palInfos: List[PalDetail] = []


def getPal(pal):
    palInfos.append(getPalByName(pal.get("name")))


with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(getPal, pals)

if len(palInfos):
    filename = "./result/pals.json"
    print(os.path.dirname(filename))
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        jsonData = json.dumps(pydash.sort_by(palInfos, "id"), indent=2)
        file.write(jsonData)
