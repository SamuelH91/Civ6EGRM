import Civ5Save from '../Civ5Save';

const path = require('path');

const TEST_SAVEGAME_V10017 = path.join(__dirname, 'resources', '1.0.0.17.Civ5Save');
const TEST_SAVEGAME_V101135 = path.join(__dirname, 'resources', '1.0.1.135.Civ5Save');
const TEST_SAVEGAME_V101221 = path.join(__dirname, 'resources', '1.0.1.221.Civ5Save');
const TEST_SAVEGAME_V10213 = path.join(__dirname, 'resources', '1.0.2.13.Civ5Save');
const TEST_SAVEGAME_V103279 = path.join(__dirname, 'resources', '1.0.3.279.Civ5Save');
const TEST_SAVEGAME_BROKEN = path.join(__dirname, 'resources', 'broken.Civ5Save');

const NEW_ALWAYS_PEACE = true;
const NEW_ALWAYS_WAR = true;
const NEW_COMPLETE_KILLS = false;
const NEW_CULTURAL_VICTORY = false;
const NEW_DIPLOMATIC_VICTORY = true;
const NEW_DOMINATION_VICTORY = true;
const NEW_LOCK_MODS = true;
const NEW_MAX_TURNS = 123;
const NEW_NEW_RANDOM_SEED = true;
const NEW_NO_BARBARIANS = false;
const NEW_NO_CHANGING_WAR_OR_PEACE = true;
const NEW_NO_CITY_RAZING = false;
const NEW_NO_CULTURE_OVERVIEW_UI = true;
const NEW_NO_ESPIONAGE = false;
const NEW_NO_HAPPINESS = true;
const NEW_NO_POLICIES = true;
const NEW_NO_RELIGION = false;
const NEW_NO_SCIENCE = true;
const NEW_NO_WORLD_CONGRESS = true;
const NEW_ONE_CITY_CHALLENGE = false;
const NEW_PITBOSS = false;
const NEW_POLICY_SAVING = false;
const NEW_PRIVATE_GAME = false;
const NEW_PROMOTION_SAVING = false;
const NEW_RAGING_BARBARIANS = false;
const NEW_RANDOM_PERSONALITIES = false;
const NEW_SCIENCE_VICTORY = false;
const NEW_TIME_VICTORY = true;
const NEW_TURN_TIMER_ENABLED = false;
const NEW_TURN_TIMER_VALUE = 321;
const NEW_TURN_MODE = Civ5Save.TURN_MODES.SIMULTANEOUS;

let savegame10017;
let savegame101135;
let savegame101221;
let savegame10213;
let savegame103279;

function getFileBlob(url) {
  return new Promise(function (resolve, reject) {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.responseType = 'blob';
    xhr.addEventListener('load', function() {
      resolve(xhr.response);
    });
    xhr.addEventListener('error', function() {
      reject(xhr.statusText);
    });
    xhr.send();
  });
}

test('Create new Civ5Save instances from file', async () => {
  let fileBlob = await getFileBlob(TEST_SAVEGAME_V10017);
  savegame10017 = await Civ5Save.fromFile(fileBlob);

  fileBlob = await getFileBlob(TEST_SAVEGAME_V101135);
  savegame101135 = await Civ5Save.fromFile(fileBlob);

  fileBlob = await getFileBlob(TEST_SAVEGAME_V101221);
  savegame101221 = await Civ5Save.fromFile(fileBlob);

  fileBlob = await getFileBlob(TEST_SAVEGAME_V10213);
  savegame10213 = await Civ5Save.fromFile(fileBlob);

  fileBlob = await getFileBlob(TEST_SAVEGAME_V103279);
  savegame103279 = await Civ5Save.fromFile(fileBlob);
}, 20000);

test('Get game build', () => {
  expect(savegame10017.gameBuild).toBe('201080');
  expect(savegame101135.gameBuild).toBe('210752');
  expect(savegame101221.gameBuild).toBe('218015');
  expect(savegame10213.gameBuild).toBe('341540');
  expect(savegame103279.gameBuild).toBe('403694');
});

test('Get game version', () => {
  expect(savegame10017.gameVersion).not.toBeDefined();
  expect(savegame101135.gameVersion).not.toBeDefined();
  expect(savegame101221.gameVersion).not.toBeDefined();
  expect(savegame10213.gameVersion).toBe('1.0.2.13 (341540)');
  expect(savegame103279.gameVersion).toBe('1.0.3.279(130961)');
});

test('Get current turn', () => {
  expect(savegame10017.currentTurn).toBe(19);
  expect(savegame101135.currentTurn).toBe(176);
  expect(savegame101221.currentTurn).toBe(52);
  expect(savegame10213.currentTurn).toBe(12);
  expect(savegame103279.currentTurn).toBe(264);
});

test('Get game mode', () => {
  expect(savegame10017.gameMode).not.toBeDefined();
  expect(savegame101135.gameMode).not.toBeDefined();
  expect(savegame101221.gameMode).not.toBeDefined();
  expect(savegame10213.gameMode).toBe(Civ5Save.GAME_MODES.SINGLE);
  expect(savegame103279.gameMode).toBe(Civ5Save.GAME_MODES.MULTI);
});

test('Get difficulty', () => {
  expect(savegame10017.difficulty).toBe('Chieftain');
  expect(savegame101135.difficulty).toBe('Warlord');
  expect(savegame101221.difficulty).toBe('Prince');
  expect(savegame10213.difficulty).toBe('Immortal');
  expect(savegame103279.difficulty).toBe('Settler');
});

test('Get starting era', () => {
  expect(savegame10017.startingEra).toBe('Ancient');
  expect(savegame101135.startingEra).toBe('Ancient');
  expect(savegame101221.startingEra).toBe('Medieval');
  expect(savegame10213.startingEra).toBe('Ancient');
  expect(savegame103279.startingEra).toBe('Future');
});

test('Get current era', () => {
  expect(savegame10017.currentEra).toBe('Ancient');
  expect(savegame101135.currentEra).toBe('Ancient');
  expect(savegame101221.currentEra).toBe('Renaissance');
  expect(savegame10213.currentEra).toBe('Ancient');
  expect(savegame103279.currentEra).toBe('Future');
});

test('Get game pace', () => {
  expect(savegame10017.gamePace).toBe('Standard');
  expect(savegame101135.gamePace).toBe('Marathon');
  expect(savegame101221.gamePace).toBe('Quick');
  expect(savegame10213.gamePace).toBe('Standard');
  expect(savegame103279.gamePace).toBe('Quick');
});

test('Get map size', () => {
  expect(savegame10017.mapSize).toBe('Small');
  expect(savegame101135.mapSize).toBe('Huge');
  expect(savegame101221.mapSize).toBe('Standard');
  expect(savegame10213.mapSize).toBe('Standard');
  expect(savegame103279.mapSize).toBe('Duel');
});

test('Get map file', () => {
  expect(savegame10017.mapFile).toBe('Continents');
  expect(savegame101135.mapFile).toBe('Pangaea');
  expect(savegame101221.mapFile).toBe('NewWorld Scenario MapScript');
  expect(savegame10213.mapFile).toBe('Pangaea');
  expect(savegame103279.mapFile).toBe('Earth Duel');
});

test('Get enabled DLC', () => {
  expect(savegame10017.enabledDLC).toEqual([]);
  expect(savegame101135.enabledDLC).toEqual([
    'Babylon',
    'Upgrade 1',
    'Mongolia'
  ]);
  expect(savegame101221.enabledDLC).toEqual([
    'Spain and Inca',
    'Polynesia',
    'Babylon',
    'Upgrade 1',
    'Mongolia'
  ]);
  expect(savegame10213.enabledDLC).toEqual([
    'Mongolia',
    'Spain and Inca',
    'Polynesia',
    'Denmark',
    'Korea',
    'Ancient Wonders',
    'Babylon',
    'Expansion - Gods and Kings',
    'Upgrade 1'
  ]);
  expect(savegame103279.enabledDLC).toEqual([
    'Mongolia',
    'Spain and Inca',
    'Polynesia',
    'Denmark',
    'Korea',
    'Ancient Wonders',
    'Civilization 5 Complete',
    'Babylon',
    'DLC_SP_Maps',
    'DLC_SP_Maps_2',
    'DLC_SP_Maps_3',
    'Expansion - Gods and Kings',
    'Expansion - Brave New World',
    'Upgrade 1'
  ]);
});

test('Get enabled Mods', () => {
  expect(savegame10017.enabledMods).toEqual([]);
  expect(savegame101135.enabledMods).toEqual([]);
  expect(savegame101221.enabledMods).toEqual([
    'Conquest of the New World',
  ]);
  expect(savegame10213.enabledMods).toEqual([]);
  expect(savegame103279.enabledMods).toEqual([]);
});

test('Get players', () => {
  expect(savegame10017.players).toEqual([
    {
      civilization: 'Persia',
      status: Civ5Save.PLAYER_STATUSES.HUMAN
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
  ]);
  expect(savegame101135.players).toEqual([
    {
      civilization: 'Arabia',
      status: Civ5Save.PLAYER_STATUSES.HUMAN
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.DEAD
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.DEAD
    },
  ]);
  expect(savegame101221.players).toEqual([
    {
      civilization: 'France',
      status: Civ5Save.PLAYER_STATUSES.HUMAN
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.DEAD
    },
    {
      civilization: undefined,
      status: Civ5Save.PLAYER_STATUSES.DEAD
    },
  ]);
  expect(savegame10213.players).toEqual([
    {
      civilization: 'Spain',
      status: Civ5Save.PLAYER_STATUSES.HUMAN
    },
    {
      civilization: 'Ottoman',
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: 'Greece',
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: 'Egypt',
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: 'Byzantium',
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: 'Austria',
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: 'Songhai',
      status: Civ5Save.PLAYER_STATUSES.AI
    },
    {
      civilization: 'Ethiopia',
      status: Civ5Save.PLAYER_STATUSES.AI
    },
  ]);
  expect(savegame103279.players).toEqual([
    {
      civilization: 'Denmark',
      status: Civ5Save.PLAYER_STATUSES.HUMAN
    },
    {
      civilization: 'Austria',
      status: Civ5Save.PLAYER_STATUSES.AI
    },
  ]);
});

test('Get always peace', () => {
  expect(savegame10017.alwaysPeace).toBe(false);
  expect(savegame101135.alwaysPeace).toBe(false);
  expect(savegame101221.alwaysPeace).toBe(false);
  expect(savegame10213.alwaysPeace).toBe(false);
  expect(savegame103279.alwaysPeace).toBe(false);
});

test('Set always peace', async () => {
  savegame10017.alwaysPeace = NEW_ALWAYS_PEACE;
  savegame101135.alwaysPeace = NEW_ALWAYS_PEACE;
  savegame101221.alwaysPeace = NEW_ALWAYS_PEACE;
  savegame10213.alwaysPeace = NEW_ALWAYS_PEACE;
  savegame103279.alwaysPeace = NEW_ALWAYS_PEACE;
  expect(savegame10017.alwaysPeace).toBe(NEW_ALWAYS_PEACE);
  expect(savegame101135.alwaysPeace).toBe(NEW_ALWAYS_PEACE);
  expect(savegame101221.alwaysPeace).toBe(NEW_ALWAYS_PEACE);
  expect(savegame10213.alwaysPeace).toBe(NEW_ALWAYS_PEACE);
  expect(savegame103279.alwaysPeace).toBe(NEW_ALWAYS_PEACE);
});

test('Get always war', () => {
  expect(savegame10017.alwaysWar).toBe(false);
  expect(savegame101135.alwaysWar).toBe(false);
  expect(savegame101221.alwaysWar).toBe(false);
  expect(savegame10213.alwaysWar).toBe(false);
  expect(savegame103279.alwaysWar).toBe(false);
});

test('Set always war', async () => {
  savegame10017.alwaysWar = NEW_ALWAYS_WAR;
  savegame101135.alwaysWar = NEW_ALWAYS_WAR;
  savegame101221.alwaysWar = NEW_ALWAYS_WAR;
  savegame10213.alwaysWar = NEW_ALWAYS_WAR;
  savegame103279.alwaysWar = NEW_ALWAYS_WAR;
  expect(savegame10017.alwaysWar).toBe(NEW_ALWAYS_WAR);
  expect(savegame101135.alwaysWar).toBe(NEW_ALWAYS_WAR);
  expect(savegame101221.alwaysWar).toBe(NEW_ALWAYS_WAR);
  expect(savegame10213.alwaysWar).toBe(NEW_ALWAYS_WAR);
  expect(savegame103279.alwaysWar).toBe(NEW_ALWAYS_WAR);
});

test('Get complete kills', () => {
  expect(savegame10017.completeKills).toBe(false);
  expect(savegame101135.completeKills).toBe(false);
  expect(savegame101221.completeKills).toBe(false);
  expect(savegame10213.completeKills).toBe(false);
  expect(savegame103279.completeKills).toBe(true);
});

test('Set complete kills', async () => {
  savegame10017.completeKills = NEW_COMPLETE_KILLS;
  savegame101135.completeKills = NEW_COMPLETE_KILLS;
  savegame101221.completeKills = NEW_COMPLETE_KILLS;
  savegame10213.completeKills = NEW_COMPLETE_KILLS;
  savegame103279.completeKills = NEW_COMPLETE_KILLS;
  expect(savegame10017.completeKills).toBe(NEW_COMPLETE_KILLS);
  expect(savegame101135.completeKills).toBe(NEW_COMPLETE_KILLS);
  expect(savegame101221.completeKills).toBe(NEW_COMPLETE_KILLS);
  expect(savegame10213.completeKills).toBe(NEW_COMPLETE_KILLS);
  expect(savegame103279.completeKills).toBe(NEW_COMPLETE_KILLS);
});

test('Get lock mods', () => {
  expect(savegame10017.lockMods).toBe(false);
  expect(savegame101135.lockMods).toBe(false);
  expect(savegame101221.lockMods).toBe(false);
  expect(savegame10213.lockMods).toBe(false);
  expect(savegame103279.lockMods).toBe(false);
});

test('Set lock mods', async () => {
  savegame10017.lockMods = NEW_LOCK_MODS;
  savegame101135.lockMods = NEW_LOCK_MODS;
  savegame101221.lockMods = NEW_LOCK_MODS;
  savegame10213.lockMods = NEW_LOCK_MODS;
  savegame103279.lockMods = NEW_LOCK_MODS;
  expect(savegame10017.lockMods).toBe(NEW_LOCK_MODS);
  expect(savegame101135.lockMods).toBe(NEW_LOCK_MODS);
  expect(savegame101221.lockMods).toBe(NEW_LOCK_MODS);
  expect(savegame10213.lockMods).toBe(NEW_LOCK_MODS);
  expect(savegame103279.lockMods).toBe(NEW_LOCK_MODS);
});

test('Get new random seed', () => {
  expect(savegame10017.newRandomSeed).toBe(false);
  expect(savegame101135.newRandomSeed).toBe(false);
  expect(savegame101221.newRandomSeed).toBe(false);
  expect(savegame10213.newRandomSeed).toBe(false);
  expect(savegame103279.newRandomSeed).toBe(false);
});

test('Set new random seed', async () => {
  savegame10017.newRandomSeed = NEW_NEW_RANDOM_SEED;
  savegame101135.newRandomSeed = NEW_NEW_RANDOM_SEED;
  savegame101221.newRandomSeed = NEW_NEW_RANDOM_SEED;
  savegame10213.newRandomSeed = NEW_NEW_RANDOM_SEED;
  savegame103279.newRandomSeed = NEW_NEW_RANDOM_SEED;
  expect(savegame10017.newRandomSeed).toBe(NEW_NEW_RANDOM_SEED);
  expect(savegame101135.newRandomSeed).toBe(NEW_NEW_RANDOM_SEED);
  expect(savegame101221.newRandomSeed).toBe(NEW_NEW_RANDOM_SEED);
  expect(savegame10213.newRandomSeed).toBe(NEW_NEW_RANDOM_SEED);
  expect(savegame103279.newRandomSeed).toBe(NEW_NEW_RANDOM_SEED);
});

test('Get no barbarians', () => {
  expect(savegame10017.noBarbarians).toBe(false);
  expect(savegame101135.noBarbarians).toBe(false);
  expect(savegame101221.noBarbarians).toBe(false);
  expect(savegame10213.noBarbarians).toBe(false);
  expect(savegame103279.noBarbarians).toBe(true);
});

test('Set no barbarians', async () => {
  savegame10017.noBarbarians = NEW_NO_BARBARIANS;
  savegame101135.noBarbarians = NEW_NO_BARBARIANS;
  savegame101221.noBarbarians = NEW_NO_BARBARIANS;
  savegame10213.noBarbarians = NEW_NO_BARBARIANS;
  savegame103279.noBarbarians = NEW_NO_BARBARIANS;
  expect(savegame10017.noBarbarians).toBe(NEW_NO_BARBARIANS);
  expect(savegame101135.noBarbarians).toBe(NEW_NO_BARBARIANS);
  expect(savegame101221.noBarbarians).toBe(NEW_NO_BARBARIANS);
  expect(savegame10213.noBarbarians).toBe(NEW_NO_BARBARIANS);
  expect(savegame103279.noBarbarians).toBe(NEW_NO_BARBARIANS);
});

test('Get no changing war or peace', () => {
  expect(savegame10017.noChangingWarPeace).toBe(false);
  expect(savegame101135.noChangingWarPeace).toBe(false);
  expect(savegame101221.noChangingWarPeace).toBe(false);
  expect(savegame10213.noChangingWarPeace).toBe(false);
  expect(savegame103279.noChangingWarPeace).toBe(false);
});

test('Set no changing war or peace', async () => {
  savegame10017.noChangingWarPeace = NEW_NO_CHANGING_WAR_OR_PEACE;
  savegame101135.noChangingWarPeace = NEW_NO_CHANGING_WAR_OR_PEACE;
  savegame101221.noChangingWarPeace = NEW_NO_CHANGING_WAR_OR_PEACE;
  savegame10213.noChangingWarPeace = NEW_NO_CHANGING_WAR_OR_PEACE;
  savegame103279.noChangingWarPeace = NEW_NO_CHANGING_WAR_OR_PEACE;
  expect(savegame10017.noChangingWarPeace).toBe(NEW_NO_CHANGING_WAR_OR_PEACE);
  expect(savegame101135.noChangingWarPeace).toBe(NEW_NO_CHANGING_WAR_OR_PEACE);
  expect(savegame101221.noChangingWarPeace).toBe(NEW_NO_CHANGING_WAR_OR_PEACE);
  expect(savegame10213.noChangingWarPeace).toBe(NEW_NO_CHANGING_WAR_OR_PEACE);
  expect(savegame103279.noChangingWarPeace).toBe(NEW_NO_CHANGING_WAR_OR_PEACE);
});

test('Get no city razing', () => {
  expect(savegame10017.noCityRazing).toBe(false);
  expect(savegame101135.noCityRazing).toBe(false);
  expect(savegame101221.noCityRazing).toBe(false);
  expect(savegame10213.noCityRazing).toBe(false);
  expect(savegame103279.noCityRazing).toBe(true);
});

test('Set no city razing', async () => {
  savegame10017.noCityRazing = NEW_NO_CITY_RAZING;
  savegame101135.noCityRazing = NEW_NO_CITY_RAZING;
  savegame101221.noCityRazing = NEW_NO_CITY_RAZING;
  savegame10213.noCityRazing = NEW_NO_CITY_RAZING;
  savegame103279.noCityRazing = NEW_NO_CITY_RAZING;
  expect(savegame10017.noCityRazing).toBe(NEW_NO_CITY_RAZING);
  expect(savegame101135.noCityRazing).toBe(NEW_NO_CITY_RAZING);
  expect(savegame101221.noCityRazing).toBe(NEW_NO_CITY_RAZING);
  expect(savegame10213.noCityRazing).toBe(NEW_NO_CITY_RAZING);
  expect(savegame103279.noCityRazing).toBe(NEW_NO_CITY_RAZING);
});

test('Get no culture overview UI', () => {
  expect(savegame10017.noCultureOverviewUI).toBe(false);
  expect(savegame101135.noCultureOverviewUI).toBe(false);
  expect(savegame101221.noCultureOverviewUI).toBe(false);
  expect(savegame10213.noCultureOverviewUI).toBe(false);
  expect(savegame103279.noCultureOverviewUI).toBe(false);
});

test('Set no culture overview UI', async () => {
  savegame10017.noCultureOverviewUI = NEW_NO_CULTURE_OVERVIEW_UI;
  savegame101135.noCultureOverviewUI = NEW_NO_CULTURE_OVERVIEW_UI;
  savegame101221.noCultureOverviewUI = NEW_NO_CULTURE_OVERVIEW_UI;
  savegame10213.noCultureOverviewUI = NEW_NO_CULTURE_OVERVIEW_UI;
  savegame103279.noCultureOverviewUI = NEW_NO_CULTURE_OVERVIEW_UI;
  expect(savegame10017.noCultureOverviewUI).toBe(NEW_NO_CULTURE_OVERVIEW_UI);
  expect(savegame101135.noCultureOverviewUI).toBe(NEW_NO_CULTURE_OVERVIEW_UI);
  expect(savegame101221.noCultureOverviewUI).toBe(NEW_NO_CULTURE_OVERVIEW_UI);
  expect(savegame10213.noCultureOverviewUI).toBe(NEW_NO_CULTURE_OVERVIEW_UI);
  expect(savegame103279.noCultureOverviewUI).toBe(NEW_NO_CULTURE_OVERVIEW_UI);
});

test('Get no espionage', () => {
  expect(savegame10017.noEspionage).toBe(false);
  expect(savegame101135.noEspionage).toBe(false);
  expect(savegame101221.noEspionage).toBe(false);
  expect(savegame10213.noEspionage).toBe(false);
  expect(savegame103279.noEspionage).toBe(true);
});

test('Set no espionage', async () => {
  savegame10017.noEspionage = NEW_NO_ESPIONAGE;
  savegame101135.noEspionage = NEW_NO_ESPIONAGE;
  savegame101221.noEspionage = NEW_NO_ESPIONAGE;
  savegame10213.noEspionage = NEW_NO_ESPIONAGE;
  savegame103279.noEspionage = NEW_NO_ESPIONAGE;
  expect(savegame10017.noEspionage).toBe(NEW_NO_ESPIONAGE);
  expect(savegame101135.noEspionage).toBe(NEW_NO_ESPIONAGE);
  expect(savegame101221.noEspionage).toBe(NEW_NO_ESPIONAGE);
  expect(savegame10213.noEspionage).toBe(NEW_NO_ESPIONAGE);
  expect(savegame103279.noEspionage).toBe(NEW_NO_ESPIONAGE);
});

test('Get no happiness', () => {
  expect(savegame10017.noHappiness).toBe(false);
  expect(savegame101135.noHappiness).toBe(false);
  expect(savegame101221.noHappiness).toBe(false);
  expect(savegame10213.noHappiness).toBe(false);
  expect(savegame103279.noHappiness).toBe(false);
});

test('Set no happiness', async () => {
  savegame10017.noHappiness = NEW_NO_HAPPINESS;
  savegame101135.noHappiness = NEW_NO_HAPPINESS;
  savegame101221.noHappiness = NEW_NO_HAPPINESS;
  savegame10213.noHappiness = NEW_NO_HAPPINESS;
  savegame103279.noHappiness = NEW_NO_HAPPINESS;
  expect(savegame10017.noHappiness).toBe(NEW_NO_HAPPINESS);
  expect(savegame101135.noHappiness).toBe(NEW_NO_HAPPINESS);
  expect(savegame101221.noHappiness).toBe(NEW_NO_HAPPINESS);
  expect(savegame10213.noHappiness).toBe(NEW_NO_HAPPINESS);
  expect(savegame103279.noHappiness).toBe(NEW_NO_HAPPINESS);
});

test('Get no policies', () => {
  expect(savegame10017.noPolicies).toBe(false);
  expect(savegame101135.noPolicies).toBe(false);
  expect(savegame101221.noPolicies).toBe(false);
  expect(savegame10213.noPolicies).toBe(false);
  expect(savegame103279.noPolicies).toBe(false);
});

test('Set no policies', async () => {
  savegame10017.noPolicies = NEW_NO_POLICIES;
  savegame101135.noPolicies = NEW_NO_POLICIES;
  savegame101221.noPolicies = NEW_NO_POLICIES;
  savegame10213.noPolicies = NEW_NO_POLICIES;
  savegame103279.noPolicies = NEW_NO_POLICIES;
  expect(savegame10017.noPolicies).toBe(NEW_NO_POLICIES);
  expect(savegame101135.noPolicies).toBe(NEW_NO_POLICIES);
  expect(savegame101221.noPolicies).toBe(NEW_NO_POLICIES);
  expect(savegame10213.noPolicies).toBe(NEW_NO_POLICIES);
  expect(savegame103279.noPolicies).toBe(NEW_NO_POLICIES);
});

test('Get no religion', () => {
  expect(savegame10017.noReligion).toBe(false);
  expect(savegame101135.noReligion).toBe(false);
  expect(savegame101221.noReligion).toBe(false);
  expect(savegame10213.noReligion).toBe(false);
  expect(savegame103279.noReligion).toBe(true);
});

test('Set no religion', async () => {
  savegame10017.noReligion = NEW_NO_RELIGION;
  savegame101135.noReligion = NEW_NO_RELIGION;
  savegame101221.noReligion = NEW_NO_RELIGION;
  savegame10213.noReligion = NEW_NO_RELIGION;
  savegame103279.noReligion = NEW_NO_RELIGION;
  expect(savegame10017.noReligion).toBe(NEW_NO_RELIGION);
  expect(savegame101135.noReligion).toBe(NEW_NO_RELIGION);
  expect(savegame101221.noReligion).toBe(NEW_NO_RELIGION);
  expect(savegame10213.noReligion).toBe(NEW_NO_RELIGION);
  expect(savegame103279.noReligion).toBe(NEW_NO_RELIGION);
});

test('Get no science', () => {
  expect(savegame10017.noScience).toBe(false);
  expect(savegame101135.noScience).toBe(false);
  expect(savegame101221.noScience).toBe(false);
  expect(savegame10213.noScience).toBe(false);
  expect(savegame103279.noScience).toBe(false);
});

test('Set no science', async () => {
  savegame10017.noScience = NEW_NO_SCIENCE;
  savegame101135.noScience = NEW_NO_SCIENCE;
  savegame101221.noScience = NEW_NO_SCIENCE;
  savegame10213.noScience = NEW_NO_SCIENCE;
  savegame103279.noScience = NEW_NO_SCIENCE;
  expect(savegame10017.noScience).toBe(NEW_NO_SCIENCE);
  expect(savegame101135.noScience).toBe(NEW_NO_SCIENCE);
  expect(savegame101221.noScience).toBe(NEW_NO_SCIENCE);
  expect(savegame10213.noScience).toBe(NEW_NO_SCIENCE);
  expect(savegame103279.noScience).toBe(NEW_NO_SCIENCE);
});

test('Get no world congress', () => {
  expect(savegame10017.noWorldCongress).toBe(false);
  expect(savegame101135.noWorldCongress).toBe(false);
  expect(savegame101221.noWorldCongress).toBe(false);
  expect(savegame10213.noWorldCongress).toBe(false);
  expect(savegame103279.noWorldCongress).toBe(false);
});

test('Set no world congress', async () => {
  savegame10017.noWorldCongress = NEW_NO_WORLD_CONGRESS;
  savegame101135.noWorldCongress = NEW_NO_WORLD_CONGRESS;
  savegame101221.noWorldCongress = NEW_NO_WORLD_CONGRESS;
  savegame10213.noWorldCongress = NEW_NO_WORLD_CONGRESS;
  savegame103279.noWorldCongress = NEW_NO_WORLD_CONGRESS;
  expect(savegame10017.noWorldCongress).toBe(NEW_NO_WORLD_CONGRESS);
  expect(savegame101135.noWorldCongress).toBe(NEW_NO_WORLD_CONGRESS);
  expect(savegame101221.noWorldCongress).toBe(NEW_NO_WORLD_CONGRESS);
  expect(savegame10213.noWorldCongress).toBe(NEW_NO_WORLD_CONGRESS);
  expect(savegame103279.noWorldCongress).toBe(NEW_NO_WORLD_CONGRESS);
});

test('Get one city challenge', () => {
  expect(savegame10017.oneCityChallenge).toBe(false);
  expect(savegame101135.oneCityChallenge).toBe(false);
  expect(savegame101221.oneCityChallenge).toBe(false);
  expect(savegame10213.oneCityChallenge).toBe(false);
  expect(savegame103279.oneCityChallenge).toBe(true);
});

test('Set one city challenge', async () => {
  savegame10017.oneCityChallenge = NEW_ONE_CITY_CHALLENGE;
  savegame101135.oneCityChallenge = NEW_ONE_CITY_CHALLENGE;
  savegame101221.oneCityChallenge = NEW_ONE_CITY_CHALLENGE;
  savegame10213.oneCityChallenge = NEW_ONE_CITY_CHALLENGE;
  savegame103279.oneCityChallenge = NEW_ONE_CITY_CHALLENGE;
  expect(savegame10017.oneCityChallenge).toBe(NEW_ONE_CITY_CHALLENGE);
  expect(savegame101135.oneCityChallenge).toBe(NEW_ONE_CITY_CHALLENGE);
  expect(savegame101221.oneCityChallenge).toBe(NEW_ONE_CITY_CHALLENGE);
  expect(savegame10213.oneCityChallenge).toBe(NEW_ONE_CITY_CHALLENGE);
  expect(savegame103279.oneCityChallenge).toBe(NEW_ONE_CITY_CHALLENGE);
});

test('Get pitboss', () => {
  expect(savegame10017.pitboss).toBe(false);
  expect(savegame101135.pitboss).toBe(false);
  expect(savegame101221.pitboss).toBe(false);
  expect(savegame10213.pitboss).toBe(false);
  expect(savegame103279.pitboss).toBe(true);
});

test('Set pitboss', async () => {
  savegame10017.pitboss = NEW_PITBOSS;
  savegame101135.pitboss = NEW_PITBOSS;
  savegame101221.pitboss = NEW_PITBOSS;
  savegame10213.pitboss = NEW_PITBOSS;
  savegame103279.pitboss = NEW_PITBOSS;
  expect(savegame10017.pitboss).toBe(NEW_PITBOSS);
  expect(savegame101135.pitboss).toBe(NEW_PITBOSS);
  expect(savegame101221.pitboss).toBe(NEW_PITBOSS);
  expect(savegame10213.pitboss).toBe(NEW_PITBOSS);
  expect(savegame103279.pitboss).toBe(NEW_PITBOSS);
});

test('Get policy saving', () => {
  expect(savegame10017.policySaving).toBe(false);
  expect(savegame101135.policySaving).toBe(false);
  expect(savegame101221.policySaving).toBe(false);
  expect(savegame10213.policySaving).toBe(false);
  expect(savegame103279.policySaving).toBe(true);
});

test('Set policy saving', async () => {
  savegame10017.policySaving = NEW_POLICY_SAVING;
  savegame101135.policySaving = NEW_POLICY_SAVING;
  savegame101221.policySaving = NEW_POLICY_SAVING;
  savegame10213.policySaving = NEW_POLICY_SAVING;
  savegame103279.policySaving = NEW_POLICY_SAVING;
  expect(savegame10017.policySaving).toBe(NEW_POLICY_SAVING);
  expect(savegame101135.policySaving).toBe(NEW_POLICY_SAVING);
  expect(savegame101221.policySaving).toBe(NEW_POLICY_SAVING);
  expect(savegame10213.policySaving).toBe(NEW_POLICY_SAVING);
  expect(savegame103279.policySaving).toBe(NEW_POLICY_SAVING);
});

test('Get promotion saving', () => {
  expect(savegame10017.promotionSaving).toBe(false);
  expect(savegame101135.promotionSaving).toBe(false);
  expect(savegame101221.promotionSaving).toBe(false);
  expect(savegame10213.promotionSaving).toBe(false);
  expect(savegame103279.promotionSaving).toBe(true);
});

test('Set promotion saving', async () => {
  savegame10017.promotionSaving = NEW_PROMOTION_SAVING;
  savegame101135.promotionSaving = NEW_PROMOTION_SAVING;
  savegame101221.promotionSaving = NEW_PROMOTION_SAVING;
  savegame10213.promotionSaving = NEW_PROMOTION_SAVING;
  savegame103279.promotionSaving = NEW_PROMOTION_SAVING;
  expect(savegame10017.promotionSaving).toBe(NEW_PROMOTION_SAVING);
  expect(savegame101135.promotionSaving).toBe(NEW_PROMOTION_SAVING);
  expect(savegame101221.promotionSaving).toBe(NEW_PROMOTION_SAVING);
  expect(savegame10213.promotionSaving).toBe(NEW_PROMOTION_SAVING);
  expect(savegame103279.promotionSaving).toBe(NEW_PROMOTION_SAVING);
});

test('Get raging barbarians', () => {
  expect(savegame10017.ragingBarbarians).toBe(false);
  expect(savegame101135.ragingBarbarians).toBe(false);
  expect(savegame101221.ragingBarbarians).toBe(false);
  expect(savegame10213.ragingBarbarians).toBe(false);
  expect(savegame103279.ragingBarbarians).toBe(true);
});

test('Set raging barbarians', async () => {
  savegame10017.ragingBarbarians = NEW_RAGING_BARBARIANS;
  savegame101135.ragingBarbarians = NEW_RAGING_BARBARIANS;
  savegame101221.ragingBarbarians = NEW_RAGING_BARBARIANS;
  savegame10213.ragingBarbarians = NEW_RAGING_BARBARIANS;
  savegame103279.ragingBarbarians = NEW_RAGING_BARBARIANS;
  expect(savegame10017.ragingBarbarians).toBe(NEW_RAGING_BARBARIANS);
  expect(savegame101135.ragingBarbarians).toBe(NEW_RAGING_BARBARIANS);
  expect(savegame101221.ragingBarbarians).toBe(NEW_RAGING_BARBARIANS);
  expect(savegame10213.ragingBarbarians).toBe(NEW_RAGING_BARBARIANS);
  expect(savegame103279.ragingBarbarians).toBe(NEW_RAGING_BARBARIANS);
});

test('Get random personalities', () => {
  expect(savegame10017.randomPersonalities).toBe(false);
  expect(savegame101135.randomPersonalities).toBe(false);
  expect(savegame101221.randomPersonalities).toBe(false);
  expect(savegame10213.randomPersonalities).toBe(false);
  expect(savegame103279.randomPersonalities).toBe(true);
});

test('Set random personalities', async () => {
  savegame10017.randomPersonalities = NEW_RANDOM_PERSONALITIES;
  savegame101135.randomPersonalities = NEW_RANDOM_PERSONALITIES;
  savegame101221.randomPersonalities = NEW_RANDOM_PERSONALITIES;
  savegame10213.randomPersonalities = NEW_RANDOM_PERSONALITIES;
  savegame103279.randomPersonalities = NEW_RANDOM_PERSONALITIES;
  expect(savegame10017.randomPersonalities).toBe(NEW_RANDOM_PERSONALITIES);
  expect(savegame101135.randomPersonalities).toBe(NEW_RANDOM_PERSONALITIES);
  expect(savegame101221.randomPersonalities).toBe(NEW_RANDOM_PERSONALITIES);
  expect(savegame10213.randomPersonalities).toBe(NEW_RANDOM_PERSONALITIES);
  expect(savegame103279.randomPersonalities).toBe(NEW_RANDOM_PERSONALITIES);
});

test('Get turn timer enabled', () => {
  expect(savegame10017.turnTimerEnabled).toBe(false);
  expect(savegame101135.turnTimerEnabled).toBe(false);
  expect(savegame101221.turnTimerEnabled).toBe(false);
  expect(savegame10213.turnTimerEnabled).toBe(false);
  expect(savegame103279.turnTimerEnabled).toBe(true);
});

test('Set turn timer enabled', async () => {
  savegame10017.turnTimerEnabled = NEW_TURN_TIMER_ENABLED;
  savegame101135.turnTimerEnabled = NEW_TURN_TIMER_ENABLED;
  savegame101221.turnTimerEnabled = NEW_TURN_TIMER_ENABLED;
  savegame10213.turnTimerEnabled = NEW_TURN_TIMER_ENABLED;
  savegame103279.turnTimerEnabled = NEW_TURN_TIMER_ENABLED;
  expect(savegame10017.turnTimerEnabled).toBe(NEW_TURN_TIMER_ENABLED);
  expect(savegame101135.turnTimerEnabled).toBe(NEW_TURN_TIMER_ENABLED);
  expect(savegame101221.turnTimerEnabled).toBe(NEW_TURN_TIMER_ENABLED);
  expect(savegame10213.turnTimerEnabled).toBe(NEW_TURN_TIMER_ENABLED);
  expect(savegame103279.turnTimerEnabled).toBe(NEW_TURN_TIMER_ENABLED);
});

test('Get turn mode', () => {
  expect(savegame10017.turnMode).toBe(Civ5Save.TURN_MODES.SEQUENTIAL);
  expect(savegame101135.turnMode).toBe(Civ5Save.TURN_MODES.SEQUENTIAL);
  expect(savegame101221.turnMode).toBe(Civ5Save.TURN_MODES.SEQUENTIAL);
  expect(savegame10213.turnMode).toBe(Civ5Save.TURN_MODES.SEQUENTIAL);
  expect(savegame103279.turnMode).toBe(Civ5Save.TURN_MODES.HYBRID);
});

test('Set turn mode', async () => {
  savegame10017.turnMode = Civ5Save.TURN_MODES.HYBRID;
  savegame101135.turnMode = Civ5Save.TURN_MODES.SIMULTANEOUS;
  savegame101221.turnMode = Civ5Save.TURN_MODES.SEQUENTIAL;
  savegame10213.turnMode = NEW_TURN_MODE;
  savegame103279.turnMode = NEW_TURN_MODE;
  expect(savegame10017.turnMode).toBe(Civ5Save.TURN_MODES.HYBRID);
  expect(savegame101135.turnMode).toBe(Civ5Save.TURN_MODES.SIMULTANEOUS);
  expect(savegame101221.turnMode).toBe(Civ5Save.TURN_MODES.SEQUENTIAL);
  expect(savegame10213.turnMode).toBe(NEW_TURN_MODE);
  expect(savegame103279.turnMode).toBe(NEW_TURN_MODE);
});

test('Get max turns', () => {
  expect(savegame10017.maxTurns).toBe(500);
  expect(savegame101135.maxTurns).toBe(1500);
  expect(savegame101221.maxTurns).toBe(100);
  expect(savegame10213.maxTurns).toBe(500);
  expect(savegame103279.maxTurns).toBe(0);
});

test('Set max turns', () => {
  savegame10017.maxTurns = NEW_MAX_TURNS;
  savegame101135.maxTurns = NEW_MAX_TURNS;
  savegame101221.maxTurns = NEW_MAX_TURNS;
  savegame10213.maxTurns = NEW_MAX_TURNS;
  savegame103279.maxTurns = NEW_MAX_TURNS;
  expect(savegame10017.maxTurns).toBe(NEW_MAX_TURNS);
  expect(savegame101135.maxTurns).toBe(NEW_MAX_TURNS);
  expect(savegame101221.maxTurns).toBe(NEW_MAX_TURNS);
  expect(savegame10213.maxTurns).toBe(NEW_MAX_TURNS);
  expect(savegame103279.maxTurns).toBe(NEW_MAX_TURNS);
});

test('Get turn timer length', () => {
  expect(savegame10017.turnTimerLength).toBe(0);
  expect(savegame101135.turnTimerLength).toBe(0);
  expect(savegame101221.turnTimerLength).toBe(0);
  expect(savegame10213.turnTimerLength).toBe(0);
  expect(savegame103279.turnTimerLength).toBe(123);
});

test('Set turn timer length', () => {
  savegame10017.turnTimerLength = NEW_TURN_TIMER_VALUE;
  savegame101135.turnTimerLength = NEW_TURN_TIMER_VALUE;
  savegame101221.turnTimerLength = NEW_TURN_TIMER_VALUE;
  savegame10213.turnTimerLength = NEW_TURN_TIMER_VALUE;
  savegame103279.turnTimerLength = NEW_TURN_TIMER_VALUE;
  expect(savegame10017.turnTimerLength).toBe(NEW_TURN_TIMER_VALUE);
  expect(savegame101135.turnTimerLength).toBe(NEW_TURN_TIMER_VALUE);
  expect(savegame101221.turnTimerLength).toBe(NEW_TURN_TIMER_VALUE);
  expect(savegame10213.turnTimerLength).toBe(NEW_TURN_TIMER_VALUE);
  expect(savegame103279.turnTimerLength).toBe(NEW_TURN_TIMER_VALUE);
});

test('Get private game', () => {
  expect(savegame10017.privateGame).not.toBeDefined();
  expect(savegame101135.privateGame).not.toBeDefined();
  expect(savegame101221.privateGame).not.toBeDefined();
  expect(savegame10213.privateGame).toBe(false);
  expect(savegame103279.privateGame).toBe(true);
});

test('Set private game', () => {
  savegame10213.privateGame = NEW_PRIVATE_GAME;
  savegame103279.privateGame = NEW_PRIVATE_GAME;
  expect(savegame10213.privateGame).toBe(NEW_PRIVATE_GAME);
  expect(savegame103279.privateGame).toBe(NEW_PRIVATE_GAME);
});

test('Get time victory', () => {
  expect(savegame10017.timeVictory).toBe(true);
  expect(savegame101135.timeVictory).toBe(true);
  expect(savegame101221.timeVictory).toBe(true);
  expect(savegame10213.timeVictory).toBe(true);
  expect(savegame103279.timeVictory).toBe(false);
});

test('Set time victory', () => {
  savegame10017.timeVictory = NEW_TIME_VICTORY;
  savegame101135.timeVictory = NEW_TIME_VICTORY;
  savegame101221.timeVictory = NEW_TIME_VICTORY;
  savegame10213.timeVictory = NEW_TIME_VICTORY;
  savegame103279.timeVictory = NEW_TIME_VICTORY;
  expect(savegame10017.timeVictory).toBe(NEW_TIME_VICTORY);
  expect(savegame101135.timeVictory).toBe(NEW_TIME_VICTORY);
  expect(savegame101221.timeVictory).toBe(NEW_TIME_VICTORY);
  expect(savegame10213.timeVictory).toBe(NEW_TIME_VICTORY);
  expect(savegame103279.timeVictory).toBe(NEW_TIME_VICTORY);
});

test('Get science victory', () => {
  expect(savegame10017.scienceVictory).toBe(true);
  expect(savegame101135.scienceVictory).toBe(true);
  expect(savegame101221.scienceVictory).toBe(false);
  expect(savegame10213.scienceVictory).toBe(true);
  expect(savegame103279.scienceVictory).toBe(true);
});

test('Set science victory', () => {
  savegame10017.scienceVictory = NEW_SCIENCE_VICTORY;
  savegame101135.scienceVictory = NEW_SCIENCE_VICTORY;
  savegame101221.scienceVictory = NEW_SCIENCE_VICTORY;
  savegame10213.scienceVictory = NEW_SCIENCE_VICTORY;
  savegame103279.scienceVictory = NEW_SCIENCE_VICTORY;
  expect(savegame101221.scienceVictory).toBe(NEW_SCIENCE_VICTORY);
  expect(savegame10017.scienceVictory).toBe(NEW_SCIENCE_VICTORY);
  expect(savegame101135.scienceVictory).toBe(NEW_SCIENCE_VICTORY);
  expect(savegame10213.scienceVictory).toBe(NEW_SCIENCE_VICTORY);
  expect(savegame103279.scienceVictory).toBe(NEW_SCIENCE_VICTORY);
});

test('Get domination victory', () => {
  expect(savegame10017.dominationVictory).toBe(true);
  expect(savegame101135.dominationVictory).toBe(true);
  expect(savegame101221.dominationVictory).toBe(false);
  expect(savegame10213.dominationVictory).toBe(true);
  expect(savegame103279.dominationVictory).toBe(false);
});

test('Set domination victory', () => {
  savegame10017.dominationVictory = NEW_DOMINATION_VICTORY;
  savegame101135.dominationVictory = NEW_DOMINATION_VICTORY;
  savegame101221.dominationVictory = NEW_DOMINATION_VICTORY;
  savegame10213.dominationVictory = NEW_DOMINATION_VICTORY;
  savegame103279.dominationVictory = NEW_DOMINATION_VICTORY;
  expect(savegame10017.dominationVictory).toBe(NEW_DOMINATION_VICTORY);
  expect(savegame101135.dominationVictory).toBe(NEW_DOMINATION_VICTORY);
  expect(savegame101221.dominationVictory).toBe(NEW_DOMINATION_VICTORY);
  expect(savegame10213.dominationVictory).toBe(NEW_DOMINATION_VICTORY);
  expect(savegame103279.dominationVictory).toBe(NEW_DOMINATION_VICTORY);
});

test('Get cultural victory', () => {
  expect(savegame10017.culturalVictory).toBe(true);
  expect(savegame101135.culturalVictory).toBe(true);
  expect(savegame101221.culturalVictory).toBe(false);
  expect(savegame10213.culturalVictory).toBe(true);
  expect(savegame103279.culturalVictory).toBe(true);
});

test('Set cultural victory', () => {
  savegame10017.culturalVictory = NEW_CULTURAL_VICTORY;
  savegame101135.culturalVictory = NEW_CULTURAL_VICTORY;
  savegame101221.culturalVictory = NEW_CULTURAL_VICTORY;
  savegame10213.culturalVictory = NEW_CULTURAL_VICTORY;
  savegame103279.culturalVictory = NEW_CULTURAL_VICTORY;
  expect(savegame10017.culturalVictory).toBe(NEW_CULTURAL_VICTORY);
  expect(savegame101135.culturalVictory).toBe(NEW_CULTURAL_VICTORY);
  expect(savegame101221.culturalVictory).toBe(NEW_CULTURAL_VICTORY);
  expect(savegame10213.culturalVictory).toBe(NEW_CULTURAL_VICTORY);
  expect(savegame103279.culturalVictory).toBe(NEW_CULTURAL_VICTORY);
});

test('Get diplomatic victory', () => {
  expect(savegame10017.diplomaticVictory).toBe(true);
  expect(savegame101135.diplomaticVictory).toBe(true);
  expect(savegame101221.diplomaticVictory).toBe(false);
  expect(savegame10213.diplomaticVictory).toBe(true);
  expect(savegame103279.diplomaticVictory).toBe(false);
});

test('Set diplomatic victory', () => {
  savegame10017.diplomaticVictory = NEW_DIPLOMATIC_VICTORY;
  savegame101135.diplomaticVictory = NEW_DIPLOMATIC_VICTORY;
  savegame101221.diplomaticVictory = NEW_DIPLOMATIC_VICTORY;
  savegame10213.diplomaticVictory = NEW_DIPLOMATIC_VICTORY;
  savegame103279.diplomaticVictory = NEW_DIPLOMATIC_VICTORY;
  expect(savegame10017.diplomaticVictory).toBe(NEW_DIPLOMATIC_VICTORY);
  expect(savegame101135.diplomaticVictory).toBe(NEW_DIPLOMATIC_VICTORY);
  expect(savegame101221.diplomaticVictory).toBe(NEW_DIPLOMATIC_VICTORY);
  expect(savegame10213.diplomaticVictory).toBe(NEW_DIPLOMATIC_VICTORY);
  expect(savegame103279.diplomaticVictory).toBe(NEW_DIPLOMATIC_VICTORY);
});

test('Save to blob', async () => {
  let newSavegameFile = savegame103279.toBlob();
  let newSavegame = await Civ5Save.fromFile(newSavegameFile);

  expect(newSavegame.alwaysPeace).toBe(NEW_ALWAYS_PEACE);
  expect(newSavegame.alwaysWar).toBe(NEW_ALWAYS_WAR);
  expect(newSavegame.completeKills).toBe(NEW_COMPLETE_KILLS);
  expect(newSavegame.culturalVictory).toBe(NEW_CULTURAL_VICTORY);
  expect(newSavegame.diplomaticVictory).toBe(NEW_DIPLOMATIC_VICTORY);
  expect(newSavegame.dominationVictory).toBe(NEW_DOMINATION_VICTORY);
  expect(newSavegame.lockMods).toBe(NEW_LOCK_MODS);
  expect(newSavegame.maxTurns).toBe(NEW_MAX_TURNS);
  expect(newSavegame.newRandomSeed).toBe(NEW_NEW_RANDOM_SEED);
  expect(newSavegame.noBarbarians).toBe(NEW_NO_BARBARIANS);
  expect(newSavegame.noChangingWarPeace).toBe(NEW_NO_CHANGING_WAR_OR_PEACE);
  expect(newSavegame.noCityRazing).toBe(NEW_NO_CITY_RAZING);
  expect(newSavegame.noCultureOverviewUI).toBe(NEW_NO_CULTURE_OVERVIEW_UI);
  expect(newSavegame.noEspionage).toBe(NEW_NO_ESPIONAGE);
  expect(newSavegame.noHappiness).toBe(NEW_NO_HAPPINESS);
  expect(newSavegame.noPolicies).toBe(NEW_NO_POLICIES);
  expect(newSavegame.noReligion).toBe(NEW_NO_RELIGION);
  expect(newSavegame.noScience).toBe(NEW_NO_SCIENCE);
  expect(newSavegame.noWorldCongress).toBe(NEW_NO_WORLD_CONGRESS);
  expect(newSavegame.oneCityChallenge).toBe(NEW_ONE_CITY_CHALLENGE);
  expect(newSavegame.pitboss).toBe(NEW_PITBOSS);
  expect(newSavegame.policySaving).toBe(NEW_POLICY_SAVING);
  expect(newSavegame.privateGame).toBe(NEW_PRIVATE_GAME);
  expect(newSavegame.promotionSaving).toBe(NEW_PROMOTION_SAVING);
  expect(newSavegame.ragingBarbarians).toBe(NEW_RAGING_BARBARIANS);
  expect(newSavegame.randomPersonalities).toBe(NEW_RANDOM_PERSONALITIES);
  expect(newSavegame.scienceVictory).toBe(NEW_SCIENCE_VICTORY);
  expect(newSavegame.timeVictory).toBe(NEW_TIME_VICTORY);
  expect(newSavegame.turnTimerEnabled).toBe(NEW_TURN_TIMER_ENABLED);
  expect(newSavegame.turnTimerLength).toBe(NEW_TURN_TIMER_VALUE);
  expect(newSavegame.turnMode).toBe(NEW_TURN_MODE);
});

test('Open broken save game', async () => {
  let fileBlob = await getFileBlob(TEST_SAVEGAME_BROKEN);
  await expect(Civ5Save.fromFile(fileBlob)).rejects.toBeDefined();
});

// https://github.com/bmaupin/civ5save-editor/issues/3
test('Test issue 3 (section19SkipSavePath)', async () => {
  let fileBlob = await getFileBlob(path.join(__dirname, 'resources', 'issue3.Civ5Save'));
  let savegame = await Civ5Save.fromFile(fileBlob);
  expect(savegame.maxTurns).toBe(330);
});

// https://github.com/bmaupin/civ5save-editor/issues/4
test('Test issue 4 (gameBuild)', async () => {
  let fileBlob = await getFileBlob(path.join(__dirname, 'resources', 'issue4.Civ5Save'));
  let savegame = await Civ5Save.fromFile(fileBlob);
  expect(savegame.gameBuild).toBe('403694');
  expect(savegame.maxTurns).toBe(500);
});

// https://github.com/bmaupin/civ5save-editor/issues/6
test('Test issue 6', async () => {
  let fileBlob = await getFileBlob(path.join(__dirname, 'resources', 'issue6.Civ5Save'));
  let savegame = await Civ5Save.fromFile(fileBlob);
  expect(savegame.maxTurns).toBe(0);
});

// https://github.com/bmaupin/civ5save-editor/issues/8
test('Test issue 8', async () => {
  let fileBlob = await getFileBlob(path.join(__dirname, 'resources', 'issue8.Civ5Save'));
  let savegame = await Civ5Save.fromFile(fileBlob);
  expect(savegame.enabledMods).toEqual([
    '(1) Community Patch',
    '(2) Community Balance Overhaul',
    '(3) City-State Diplomacy Mod for CBP',
    '(4) C4DF - CBP',
    '(5) More Luxuries - CBO Edition (5-14b)',
  ]);
  expect(savegame.timeVictory).toBe(true);
  expect(savegame.noWorldCongress).toBe(false);
});

// https://github.com/bmaupin/civ5save-editor/issues/15
test('Test issue 15', async () => {
  let fileBlob = await getFileBlob(path.join(__dirname, 'resources', 'issue15.Civ5Save'));
  let savegame = await Civ5Save.fromFile(fileBlob);
  expect(savegame.gameVersion).toBe('1.0.3.279 (180925)');
  expect(savegame.gameBuild).toBe('403694');
  expect(savegame.maxTurns).toBe(330);
});
