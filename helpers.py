import requests
from bs4 import BeautifulSoup, Tag
from typing import List
from constants import URL
from typeClasses import PalSimple, PalDetail, Suitability
import pydash


def lowercaseFirstLetter(str: str):
    return str.replace(str[0], str[0].lower(), 1)


def getPalNames():
    web = requests.get(URL + "/Paldeck")
    html = BeautifulSoup(web.content, "html.parser")

    tables = html.select("table.fandom-table")

    pals: List[PalSimple] = []
    for table in tables[:2]:
        rows = table.find("tbody").find_all("tr")[1:]
        for row in rows:
            id = row.find_all("td")[0].text
            name = row.find_all("td")[2].find("a").text
            pals.append({"id": id, "name": name})
    return pals


def getPalByName(name: str) -> PalDetail:
    try:
        web = requests.get(URL + "/" + name.replace(" ", "_"))
        html = BeautifulSoup(web.content, "html.parser")

        # name
        name = html.find("span", class_="mw-page-title-main").text

        stats = html.find("h2", text="Stats").parent.findAll(recursive=False)
        # id
        id = stats[1].find_all()[1].text.replace("#", "")
        # elements
        elementsTags: List[Tag] = stats[2].find("div").find_all("a", text=True)
        elements = pydash.map_(elementsTags, lambda tag: lowercaseFirstLetter(tag.text))
        # drops
        dropsTags: List[Tag] = stats[3].find("div").find_all("a", text=True)
        drops = pydash.map_(dropsTags, lambda tag: tag.text)
        # foods
        foods: List[Tag] = len(stats[4].find("div").find_all("img", alt="Food on icon"))
        # suitability
        workSuitability = pydash.flat_map(
            html.find("h2", text="Work Suitability")
            .find_next_sibling()
            .find_all("section", recursive=False),
            lambda tag: tag.find_all("div"),
        )
        workSuitabilityTexts = pydash.map_(
            workSuitability, lambda tag: tag.text.strip()
        )
        workSuitabilityDict: Suitability = {}
        for text in workSuitabilityTexts:
            splittedText = text.split(" ")
            if splittedText[-1].isdigit():
                suitability = lowercaseFirstLetter("".join(splittedText[0:-1]))
                level = splittedText[-1]
                workSuitabilityDict[suitability] = int(level)
            else:
                suitability = lowercaseFirstLetter(text.replace(" ", ""))
                workSuitabilityDict[suitability] = 0
        # image
        image = html.find("aside").find("figure").find("a").find("img").attrs["src"]
        # partner skill
        partnerSkillGroup = html.find("h2", text="Partner Skill").parent
        partnerSkill = {
            "name": partnerSkillGroup.find("div", text=True).text,
            "icon": partnerSkillGroup.find("section")
            .find("a")
            .find("img")
            .attrs["data-src"],
            "description": partnerSkillGroup.find_all("section")[2]
            .find_all("div")[-1]
            .text,
        }

        return {
            "id": id,
            "name": name,
            "elements": elements,
            "drops": drops,
            "foods": foods,
            "suitability": workSuitabilityDict,
            "image": image,
            "partnerSkill": partnerSkill,
        }
    except:
        print("Failed: ", name)
        return None
