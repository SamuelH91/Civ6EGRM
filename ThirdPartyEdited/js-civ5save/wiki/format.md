**Note: these are notes taken during research. For a more up-to-date description of the Civ5Save file format, see [../src/Civ5SavePropertyDefinitions.js](../src/Civ5SavePropertyDefinitions.js)**

| Section | Type | Sample values | Notes |
| --- | --- | --- | --- |
| 1 |  |  |  |
|  | String | Must be `CIV5` | File signature |
|  | 32-bit integer | 8 | Save game version:<br>4 = 1.0.0 - 1.0.0.17<br>5 = 1.0.0.62 - 1.0.1.221<br>7 = 1.0.1.332 - 1.0.1.383<br>8 = 1.0.1.511+ |
|  | String | `1.0.2.13 (341540)`<br>`1.0.3.18 (379995)`<br>`1.0.3.80 (389545)`<br>`1.0.3.142 (395070)`<br>`1.0.3.144 (395131)`<br>`1.0.3.279(130961)` | Civ 5 version |
|  | String | `379995`<br>`395131`<br>`403694` | Civ 5 build |
|  | 32-bit integer | | Current turn |
|  | 8-bit integer | | Game mode:<br>0 = Single player<br>1 = Multiplayer<br>2 = Hotseat |
|  | String | `CIVILIZATION_IROQUOIS`<br>`CIVILIZATION_MOROCCO` | Player 1 civilization |
|  | String | `HANDICAP_CHIEFTAIN`<br>`HANDICAP_SETTLER` | Difficulty |
|  | String | `ERA_ANCIENT` | Starting era |
|  | String | `ERA_ANCIENT`<br>`ERA_RENAISSANCE` | Current era |
|  | String | `GAMESPEED_STANDARD`<br>`GAMESPEED_QUICK` | Game pace |
|  | String | `WORLDSIZE_DUEL`<br>`WORLDSIZE_SMALL` | Map size |
|  | String | `Assets\Maps\Continents.lua`<br>`Assets\Maps\Earth_Duel.Civ5Map` | Map |
| 2 |  |  | `civilizations` in the SDK?? |
| 3 |  |  | Player names (for human players) (`nicknames` in the SDK) |
| 4 |  |  | Player statuses (`slotStatus` in the SDK) |
| 5 |  |  | `slotClaims` in the SDK?? |
| 6 |  |  | `teamTypes` in the SDK?? |
| 7 |  |  | Player difficulties? (`handicapTypes` in the SDK) |
| 8 |  |  | Player civilizations (`civilizationKeys` in the SDK) |
| 9 |  |  | Leaders (`leaderKeys` in the SDK) |
| 14 |  |  | Climate |
| 17 |  |  | Player difficulties? |
| 18 |  |  | Player difficulties? |
| 19* |  |  |  |
|  | 32-bit integer | 0<br>330<br>500 | Max turns |
| 20* |  |  | City states |
| 23* |  |  |  |
|  | Integer |  | Turn timer length |
| 25* |  |  |  |
|  |  |  | Player colours |
|  |  |  | Multiplayer private game |
| 26* |  |  | Sea level |
| 29* |  |  |  |
|  | Boolean |  | Victory conditions |
| 30* |  |  | Various map and game options |
| 33* |  |  | zlib compressed data starts with `0100 789c` |

Notes:
---
- Sections are separated by `4000 0000`
- Within each section, string values are prefixed by their length as a little-endian 32-bit integer. For example:  
  `1400 0000 4349 5649 4c49 5a41 5449 4f4e 5f4d 4f52 4f43 434f`
  - `1400 0000` = 0x14 (little endian) = 20 bytes
  - `4349...` = `CIVILIZATION_MOROCCO` (20 bytes long)
- *Savegames contain different number of sections depending on the build/version
  - Build 395070 (version 1.0.3.142)+
    - Contains 33 sections
    - Section 18 is an additional section that contains mostly 0xff
  - Build ?????? - 389545 (version 1.0.3.80)
    - Contains 32 sections
- Somewhere around build 230620 the savegame format had some major changes, including the addition of the game version and build near the beginning of the file
- Starting with build 310700 the player colours are written as strings instead of hex values. Player civilizations and leaders are also added to the file as strings.

Relationship between time victory and max turns
---
- If time victory is checked and max turns is set to greater than 0, the game will end at max turns
- If time victory is unchecked and max turns is set to greater than 0, the game will end at max turns but it will say that time victory is disabled
- If time victory is checked and max turns is set to 0, the game will end based on the game speed (quick: 330 turns, standard: 500 turns, etc)

Builds and versions
---
| Build | Version |
| --- | --- |
| 98650  | 1.0 |
| 200405 | 1.0.0.7 |
| 201080 | 1.0.0.17 |
| 203896 | 1.0.0.62 |
| 210752 | 1.0.1.135 |
| 217984 | 1.0.1.217 |
| 218015 | 1.0.1.221 |
| 230620 | 1.0.1.332 |
|        | 1.0.1.348 |
| 237603 | 1.0.1.383 |
| 262623 | 1.0.1.511 |
| 310700 | 1.0.1.674 |
| 322813 | 1.0.1.705 |
| 341540 | 1.0.2.13 |
| 379995 | 1.0.3.18 |
| 388272 | 1.0.3.70 |
| 395070 | 1.0.3.142 |
| 403694 | 1.0.3.279 |


## SDK
- CvGameCoreSource/CvGameCoreDLL_Expansion2/CvPreGame.cpp
    - Might help in determining some of the overall structure of the savegame (e.g. slotStatus)
- CvGameCoreSource/CvGameCoreDLLUtil/include/CvEnums.h
    - Contains some enums and values, which may or may not help in determining values for specific properties (e.g. SlotStatus)
- CvGameCoreSource/CvGameCoreDLL_Expansion2/CvInfos.cpp
    - Contains some advanced types, which may be serialized directly into the savegame (e.g. CvWorldInfo)


References:
---
- File format
  - https://github.com/rivarolle/civ5-saveparser
  - https://github.com/omni-resources/civ5-save-parser
  - https://github.com/urbanski/010_Civ5Save/blob/master/civ5.bt
- Victory conditions/max turns
  - https://gaming.stackexchange.com/a/273907/154341
- Multiplayer turn types
  - http://blog.frank-mich.com/civilization-v-how-to-change-turn-type-of-a-started-game/
- Multiplayer private/public
  - https://github.com/Canardlaquay/Civ5SavePrivate/blob/master/Civ5PrivateSave/Form1.cs
  - https://github.com/Renophaston/DefectiveCivSavePrivatizer/blob/master/main.c
- Multiplayer pitboss setting
  - https://github.com/Bownairo/Civ5SaveEditor/blob/master/SaveEditor.c
- Multiplayer turn timer
  - https://steamcommunity.com/app/8930/discussions/0/864973761026018000/#c619568192863618582
- Multiplayer password and player status
  - https://github.com/omni-resources/civ5-save-parser
- Patch notes for various versions
  - http://www.kynosarges.org/misc/Civ5PatchNotes.txt