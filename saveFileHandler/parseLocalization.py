import xml.etree.ElementTree as ET
import os
from watchdog.utils.dirsnapshot import DirectorySnapshot
import json
import codecs

vanillapath = os.path.expanduser("G:\SteamLibrary\steamapps\common\Sid Meier's Civilization VI\Base\Assets\Text")
dlcpath = os.path.expanduser("G:\SteamLibrary\steamapps\common\Sid Meier's Civilization VI\DLC")

info = "\
# This file is autogenerated by parseLocalization.py (set correct paths there) from following files\n\
# Civ/leader names can be found from SteamLibrary\steamapps\common\Sid Meier's Civilization VI\Base\Assets\Text\n\
# Vanilla_<language>.xml\n\
\n\
# xml tags needed:\n\
# <Replace Tag=\"LOC_LEADER_<LEADER>_NAME\" Language=\"<language>\">\n\
# <Replace Tag=\"LOC_CIVILIZATION_<CIV>_NAME\" Language=\"<language>\">\n\
# <Replace Tag=\"LOC_CITY_NAME_<CITY>\" Language=\"<language>\">\n\
\n\
# And for DLCs\n\
# from SteamLibrary\steamapps\common\Sid Meier's Civilization VI\DLC\<DLC>\Text\n\
# <DLC>_Translations_ConfigText.xml\n\n"

targetLanguages = ["ru_RU", "de_DE", "es_ES", "fr_FR", "it_IT", "ja_JP", "ko_KR", "pl_PL", "pt_BR"]
civNameExtra = "_FRONTEND"
civNameStart = "LOC_CIVILIZATION_"
leaderNameStart = "LOC_LEADER_"
leaderNameExtra = "TRAIT"
cityName0 = "LOC_CITY_"
cityName = "LOC_CITY_NAME_"
dlcFileEnd = "_Translations_ConfigText.xml"
dlcFileEnd2 = "_Translations_Text.xml"
dlcFileEnd3 = "_Translations_Major_Text.xml"
vanillaFileStart = "Vanilla_"
ignored_names = [
    "LOC_CITY_BANNER_",
    "LOC_CITY_STATE_",
    "LOC_CITY_STATES_",
    "LOC_CITY_SACKED_",
    "LOC_CITY_RECENTLY_",
    "LOC_CITY_YIELD_",
    "LOC_CITY_BELONGS_",
    "LOC_CITY_GOLD_",
    "LOC_CITY_PANEL_POWER_",
    "LOC_CITY_GET_",
]
xmlfile = ".xml"
nameEnd = "_NAME"
civNameExtraLen = len(civNameExtra)
civNameStartLen = len(civNameStart)
leaderNameStartLen = len(leaderNameStart)
leaderNameExtraLen = len(leaderNameExtra)
cityNameLen = len(cityName)
cityNameLen0 = len(cityName0)
dlcFileEndLen = len(dlcFileEnd)
dlcFileEndLen2 = len(dlcFileEnd2)
dlcFileEndLen3 = len(dlcFileEnd3)
vanillaFileStartLen = len(vanillaFileStart)
xmlfileLen = len(xmlfile)
nameEndLen = len(nameEnd)

leaders = {}
civs = {}
citys = {}


def add_tag_to_dict(replaceTag, dictionary, tag, language):
    if tag[-civNameExtraLen:] == civNameExtra:  # Remove "_FRONTEND"
        tag = tag[:-civNameExtraLen]
    civName = replaceTag.find("Text").text.split('|')[0]
    if tag in dictionary:
        dictionary[tag][language] = civName
    else:
        dictionary[tag] = {}
        dictionary[tag][language] = civName


def parse_xml(path, targetLanguage, vanilla=False):
    tree = ET.parse(path)
    root = tree.getroot()
    LocalizedText = root[0]

    for replaceTag in LocalizedText:
        attributes = replaceTag.attrib
        language = attributes["Language"]
        if language == targetLanguage:
            tag = attributes["Tag"]
            if tag[:civNameStartLen] == civNameStart:
                if tag[-nameEndLen:] == nameEnd:
                    tag = tag[civNameStartLen:-nameEndLen]
                    add_tag_to_dict(replaceTag, civs, tag, language)
            elif tag[:leaderNameStartLen] == leaderNameStart:
                tag = tag[leaderNameStartLen:]
                if tag[:leaderNameExtraLen] != leaderNameExtra:
                    if tag[-nameEndLen:] == nameEnd:
                        tag = tag[:-nameEndLen]
                        add_tag_to_dict(replaceTag, leaders, tag, language)
            elif tag[:cityNameLen0] == cityName0:  # Vietnam fix
                if tag[:cityNameLen] == cityName:
                    tag = tag[cityNameLen:]
                    add_tag_to_dict(replaceTag, citys, tag, language)
                else:
                    if not vanilla:
                        for ignored in ignored_names:
                            if ignored == tag[:len(ignored)]:
                                break
                        else:
                            tag = tag[cityNameLen0:]
                            add_tag_to_dict(replaceTag, citys, tag, language)

snapshotVanilla = DirectorySnapshot(vanillapath, False)
for i, path in enumerate(snapshotVanilla.paths):
    if path[-xmlfileLen:] == xmlfile:
        head, tail = os.path.split(path)
        if tail[:vanillaFileStartLen] == vanillaFileStart:
            targetLanguage = tail[vanillaFileStartLen:-xmlfileLen]
            if targetLanguage in targetLanguages:
                parse_xml(path, targetLanguage, vanilla=True)

snapshot = DirectorySnapshot(dlcpath, True)
for i, path in enumerate(snapshot.paths):
    if path[-dlcFileEndLen:] == dlcFileEnd:
        # print(path)
        for targetLanguage in targetLanguages:
            parse_xml(path, targetLanguage)
    elif path[-dlcFileEndLen2:] == dlcFileEnd2:
        # print(path)
        for targetLanguage in targetLanguages:
            parse_xml(path, targetLanguage)
    elif path[-dlcFileEndLen3:] == dlcFileEnd3:
        # print(path)
        for targetLanguage in targetLanguages:
            parse_xml(path, targetLanguage)

with codecs.open("civLocalization.py", "w", "utf-8") as stream:   # or utf-8
    stream.write(info)
    stream.write("CIV_LEADER_NAMES = ")
    stream.write(json.dumps(leaders, indent=4, ensure_ascii=False, sort_keys=True))
    stream.write("\n\n")
    stream.write("CIV_NAMES = ")
    stream.write(json.dumps(civs, indent=4, ensure_ascii=False, sort_keys=True))
    stream.write("\n\n")
    stream.write("CITY_NAMES = ")
    stream.write(json.dumps(citys, indent=4, ensure_ascii=False, sort_keys=True))
    stream.write("\n\n")

print("Autogeneration done!!!")