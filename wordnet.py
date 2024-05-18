import requests
from bs4 import BeautifulSoup


def getWordNet(word: str) -> dict:
    URL = f"https://www.cfilt.iitb.ac.in/indowordnet/wordnet?langno=12&query={word}"

    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")

    sysID = soup.find("td", id="s_id").get_text()
    POS = soup.find("td", id="pos").get_text()

    synonyms_table = soup.find("td", id="synonyms")
    synonyms_links = synonyms_table.find_all("a")

    synonyms = []
    for link in synonyms_links:
        synonym_text = link.get_text()
        cleaned_synonym = synonym_text.strip(",").strip(" ")
        synonyms.append(cleaned_synonym)

    return {word: {"sysID": int(sysID), "POS": POS.lower(), "synonyms": synonyms}}
