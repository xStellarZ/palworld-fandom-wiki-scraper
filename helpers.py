import requests
from bs4 import BeautifulSoup, Tag
from typing import List
from constants import URL
from typeClasses import PalSimple, PalDetail, Suitability
import pydash
import traceback


def lowercaseFirstLetter(str: str):
    return str.replace(str[0], str[0].lower(), 1)


def getPalNames():
    web = requests.get(URL + "/Palpedia")
    html = BeautifulSoup(web.content, "html.parser")

    tables = html.select("table.fandom-table")

    pals: List[PalSimple] = []
    for table in tables[:2]:
        rows = table.find("tbody").find_all("tr")[1:]
        for row in rows:
            id = row.find_all("td")[0].text.strip()
            name_tag = row.find_all("td")[2].find("a") or row.find_all("td")[2].find("span")
            name = name_tag.text.strip()
            pals.append({"id": id, "name": name})

    print(pals)
    return pals

def getPalByName(name: str, id: int) -> PalDetail:
    try:
        web = requests.get(URL + "/" + name.replace(" ", "_"))
        html = BeautifulSoup(web.content, "html.parser")

        stats_header = html.find("h2", text="Stats")

        # if page does not exist, set defaults.
        # TODO: use ALT_URL as an alternative data source
        if stats_header is None:
            return {
                "id": id,
                "key": "",
                "image": "",
                "name": name,
                "wiki": "",
                "types": [],
                "imageWiki": "",
                "suitability": [],
                "drops": [],
                "aura": {},
                "description": "",
                "skills": []
            }

        # name
        name = html.find("span", class_="mw-page-title-main").text

        # wiki
        wiki = (URL + "/" + name).replace(" ", "_")

        # key
        stats = html.find("h2", text="Stats").parent.findAll(recursive=False)
        key = stats[1].find_all()[1].text.replace("#", "")

        # image
        image = f"/public/images/paldeck/{key}.png"

        print(f"{name}, {id}\n")

        # types
        elementsTags: List[Tag] = stats[2].find("div").find_all("a", text=True)

        baseElementImagePath = "/public/images/elements/"

        elementsList = [
            {
                "name": lowercaseFirstLetter(tag.text),
                "image": f"{baseElementImagePath}{lowercaseFirstLetter(tag.text)}.png"
            }
            for tag in elementsTags
        ]

        # drops
        drops_parent = html.find(attrs={"data-source": "drops"})
        if drops_parent:
            drops_div = drops_parent.find("div")  # Find the div inside the parent
            if drops_div:
                dropsTags = drops_div.find_all(["a", "span"], text=True)
            else:
                dropsTags = []
        else:
            dropsTags = []

        drops = pydash.map_(dropsTags, lambda tag: tag.text.lower().replace(" ", "_"))

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
        suitabilityList = []
        baseImagePath = "/public/images/works/"

        for text in workSuitabilityTexts:
            splittedText = text.split(" ")
            if splittedText[-1].isdigit():
                #suitability = lowercaseFirstLetter("".join(splittedText[0:-1]))
                suitability = "_".join(splittedText[0:-1]).lower()
                level = int(splittedText[-1])
            else:
                suitability = lowercaseFirstLetter(text.replace(" ", ""))
                level = 0

            if level > 0:
                suitabilityList.append({
                    "type": suitability,
                    "image": f"{baseImagePath}{suitability}.png",
                    "level": level
                })

        # imageWiki
        imageWiki = html.find(attrs={"class": "deckentrytitle"}).find('a').attrs['href']

        # partner skill
        partnerSkillGroup = html.find("h2", text="Partner Skill").parent
        description = partnerSkillGroup.find_all("section")[2].find_all("div")[-1]

        for br_tag in description.find_all("br"):
            br_tag.replace_with("\n")

        description_text = description.get_text(separator="\n").strip()

        description_text = '\n'.join([line.strip() for line in description_text.split('\n') if line.strip()])

        partnerSkill = {
            "name": partnerSkillGroup.find("div", text=True).text.lower().replace(" ", "_"),
            "description": description_text
        }

        # description
        descriptionDiv = html.find(attrs={"class": "decktext"})
        description = descriptionDiv.text

        # skills
        skillsTable = html.find(attrs={"id": "Active_Skills"}).find_next("table")
        skillRows = skillsTable.find_all("tr")

        skills = []
        for i in range(0, len(skillRows), 2):
            levelRow = skillRows[i]
            descriptionRow = skillRows[i + 1]

            level = int(levelRow.find("th").text.strip().replace("Lv", ""))

            skillTypeTag = levelRow.find("a", title=True)
            skillType = skillTypeTag['title'].strip().lower()
            b_tags = levelRow.find_all("b")
            if len(b_tags) > 1:
                tag = b_tags[1].find(["a", "span"])

                if tag and tag.text:
                    skillName = tag.text.strip().lower().replace(" ", "_")

            cooldown = int(
                levelRow.find_all("td", style="text-align:center;")[0].text.replace("CT:", "").replace("s", "").strip())
            power = int(levelRow.find_all("td", style="text-align:center;")[1].text.replace("Power:", "").strip())

            skillDescription = descriptionRow.find("td").text.strip()

            skill = {
                "level": level,
                "name": skillName,
                "type": skillType,
                "cooldown": cooldown,
                "power": power,
                "description": skillDescription
            }
            skills.append(skill)

        return {
            "id": id,
            "key": key,
            "image": image,
            "name": name,
            "wiki": wiki,
            "types": elementsList,
            "imageWiki": imageWiki,
            "suitability": suitabilityList,
            "drops": drops,
            "aura": partnerSkill,
            "description": description,
            "skills": skills
        }
    except:
        print(f"Exception for {name}:\n")
        traceback.print_exc()
        return None
