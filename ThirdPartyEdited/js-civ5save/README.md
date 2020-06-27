[![Build Status](https://travis-ci.org/bmaupin/js-civ5save.svg?branch=master)](https://travis-ci.org/bmaupin/js-civ5save)
[![Coverage Status](https://coveralls.io/repos/github/bmaupin/js-civ5save/badge.svg?branch=master)](https://coveralls.io/github/bmaupin/js-civ5save?branch=master)
[![NPM version](https://badge.fury.io/js/civ5save.svg)](https://www.npmjs.com/package/civ5save)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/bmaupin/js-civ5save/blob/master/LICENSE)
[![Documentation](https://bmaupin.github.io/js-civ5save/badge.svg)](https://bmaupin.github.io/js-civ5save/identifiers.html)
---

### Features
- [Documented API](https://bmaupin.github.io/js-civ5save/identifiers.html)
- Support for reading general game information (difficulty, turn number, player civilizations and statuses, etc.)
- Support for reading and writing victory types (time, science, etc.)
- Support for reading and writing advanced options (policy saving, promotion saving, etc.)
- Support for reading and writing hidden options (always peace, always war, etc.)
- Support for reading and writing certain multiplayer options (pitboss, private game, turn mode, turn timer)

For an example of actual usage, see https://github.com/bmaupin/civ5save-editor


### Goals
- Support for properties which can be changed by modifying the uncompressed header of the file
- Support for all versions of the base game, including DLC and expansion packs
- Support for the latest version only of mods (at least the most popular ones)


### Non-goals
- Support for properties which can be changed in game (e.g. quick combat)
- Support for properties which have no effect when changed after a game's started
- Support for properties in the compressed section of the file
- Support for anything other than the latest version of a particular mod
- Support for other Civilization games


### Installation

    npm install civ5save


### Development

    git clone https://github.com/bmaupin/js-civ5save.git
    cd js-civ5save
    npm install


### Testing

    npm test


### Building (includes documentation)

    npm run build


### Credits

#### References
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
