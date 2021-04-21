-- FROM PRISMATIC (G:\SteamLibrary\steamapps\workshop\content\289070\1661785509) WITH THESE MODIFICATIONS TO GET IT WORKING WITH PYTHON
CREATE TABLE Colors (
    Type text PRIMARY KEY,
    Color text
);

CREATE TABLE PlayerColors (
    Type text PRIMARY KEY,
    UseType text,
    PrimaryColor text,
    SecondaryColor text,
    Alt1PrimaryColor text,
    Alt1SecondaryColor text,
    Alt2PrimaryColor text,
    Alt2SecondaryColor text,
    Alt3PrimaryColor text,
    Alt3SecondaryColor text
);


------------
-- COLORS
------------

INSERT OR REPLACE INTO Colors
		(Type,								Color)
VALUES	('COLOR_SC_BRICK',   				'76,0,0,255'),
		('COLOR_SC_LIGHT_BRICK',			'158,50,50,255'),
		('COLOR_SC_MEDIUM_BROWN',			'85,44,0,255'),
		('COLOR_SC_DARK_PERSIMMON',			'188,70,0,255'),
		('COLOR_SC_PERSIMMON',				'236,88,0,255'),
		('COLOR_SC_COCOA',					'210,105,30,255'),
		('COLOR_SC_LIGHT_BROWN',			'170,116,57,255'),
		('COLOR_SC_LIGHT_PERSIMMON',		'255,153,92,255'),
		('COLOR_SC_ORANGE',					'248,162,2,255'),
		('COLOR_SC_TAN',					'221,183,106,255'),
		('COLOR_SC_LIGHTEST_BROWN',			'255,214,170,255'),
		('COLOR_SC_BRIGHT_YELLOW',			'254,249,0,255'),
		('COLOR_SC_LIGHT_PASTEL_YELLOW',	'255,255,188,255'),
		('COLOR_SC_DARKEST_DRAB',			'44,65,0,255'),
		('COLOR_SC_DARK_DRAB',				'73,103,9,255'),
		('COLOR_SC_MEDIUM_DRAB',			'108,142,35,255'),
		('COLOR_SC_LIGHT_DRAB',				'190,220,127,255'),
		('COLOR_SC_DARK_GREEN',				'0,82,0,255'),
		('COLOR_SC_GREEN',					'0,170,0,255'),
		('COLOR_SC_LIGHT_GREEN',			'66,207,66,255'),
		('COLOR_SC_DARK_PASTEL_GREEN',		'0,152,46,255'),
		('COLOR_SC_LIGHT_PASTEL_GREEN',		'83,209,121,255'),
		('COLOR_SC_DARKEST_TEAL',			'0,117,88,255'),
		('COLOR_SC_DARK_TEAL',				'2,152,114,255'),
		('COLOR_SC_MEDIUM_TEAL',			'97,216,186,255'),
		('COLOR_SC_LIGHT_TEAL',				'187,245,231,255'),
		('COLOR_SC_DARK_CYAN',				'0,126,162,255'),
		('COLOR_SC_DARK_GREECE_BLUE',		'13,72,124,255'),
		--('COLOR_SC_CYAN',					'0,183,235,255'), -- REPLACED, was too close to standard blue light
		('COLOR_SC_CYAN',					'6,200,255,255'),
		('COLOR_SC_LIGHT_CYAN',				'85,215,252,255'),
		('COLOR_SC_GREECE_BLUE',			'50,109,162,255'),
		('COLOR_SC_TRUE_BLUE',				'16,51,166,255'),
		('COLOR_SC_LIGHT_TRUE_BLUE',		'43,76,186,255'),
		('COLOR_SC_LIGHT_GREECE_BLUE',		'168,202,233,255'),
		('COLOR_SC_LIGHTEST_TRUE_BLUE',		'112,136,213,255'),
		('COLOR_SC_DARK_WISTERIA',			'131,73,159,255'),
		('COLOR_SC_WISTERIA',				'166,114,191,255'),
		('COLOR_SC_LIGHT_WISTERIA',			'201,160,220,255'),
		('COLOR_SC_DARK_PURPLE',			'90,0,70,255'),
		('COLOR_SC_MEDIUM_PURPLE',			'146,36,122,255'),
		('COLOR_SC_DARK_RED_VIOLET',		'166,0,104,255'),
		('COLOR_SC_RED_VIOLET',				'199,21,113,255'),
		('COLOR_SC_LIGHT_RED_VIOLET',		'206,58,151,255'),
		('COLOR_SC_LIGHTEST_RED_VIOLET',	'219,97,174,255'),
		('COLOR_SC_DARK_CRANBERRY',			'165,15,22,255'),
		('COLOR_SC_DARK_PINK',				'254,55,108,255'),
		('COLOR_SC_CRANBERRY',				'206,32,41,255'),
		('COLOR_SC_LIGHT_CRANBERRY',		'224,73,81,255'),
		('COLOR_SC_PINK',					'255,145,175,255'),
		('COLOR_SC_LIGHT_PINK',				'255,199,214,255'),
		('COLOR_SC_MEDIUM_GREY',			'128,128,128,255'),
		('COLOR_SC_LIGHT_GREY',				'211,211,211,255'),
		('COLOR_STANDARD_YELLOW_LT',		'250,236,127,255');

-- REMOVED
-- UPDATE PlayerColors
-- SET SecondaryColor = 'COLOR_SC_LIGHT_CRANBERRY'
-- WHERE Type = 'LEADER_FREE_CITIES';

CREATE TABLE IF NOT EXISTS 
		SC_JERSEY_TABLE (
		Leader								text								default null,
		UseType								text								default null,
		Primary1							text								default null,
		Secondary1							text								default null,
		Primary2							text								default null,
		Secondary2							text								default null,
		Primary3							text								default null,
		Secondary3							text								default null,
		Primary4							text								default null,
		Secondary4							text								default null);


INSERT INTO SC_JERSEY_TABLE
		(Leader,			UseType,	Primary1, 	Secondary1, Primary2, 	Secondary2, Primary3, 	Secondary3, Primary4, 	Secondary4)
VALUES	('LEADER_ALEXANDER', 'Unique', 'COLOR_STANDARD_WHITE_MD2', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_DARK_GREECE_BLUE', 'COLOR_STANDARD_YELLOW_LT', 'COLOR_STANDARD_ORANGE_DK', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_SC_DARK_CYAN', 'COLOR_SC_LIGHT_CYAN'),
		('LEADER_AMANITORE', 'Unique', 'COLOR_SC_TAN', 'COLOR_STANDARD_ORANGE_DK', 'COLOR_SC_COCOA', 'COLOR_SC_LIGHTEST_BROWN', 'COLOR_STANDARD_YELLOW_LT', 'COLOR_SC_PERSIMMON', 'COLOR_SC_MEDIUM_PURPLE', 'COLOR_SC_LIGHTEST_BROWN'),
		('LEADER_BARBAROSSA', 'Unique', 'COLOR_SC_LIGHT_GREY', 'COLOR_STANDARD_WHITE_DK', 'COLOR_SC_DARK_GREECE_BLUE', 'COLOR_SC_LIGHT_GREY', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_STANDARD_WHITE_DK', 'COLOR_STANDARD_WHITE_MD', 'COLOR_SC_LIGHT_GREY'),
		('LEADER_CATHERINE_DE_MEDICI', 'Unique', 'COLOR_STANDARD_BLUE_MD', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_STANDARD_WHITE_LT', 'COLOR_STANDARD_YELLOW_DK', 'COLOR_SC_LIGHT_TRUE_BLUE', 'COLOR_STANDARD_WHITE_LT', 'COLOR_SC_GREECE_BLUE', 'COLOR_SC_BRIGHT_YELLOW'),
		('LEADER_CHANDRAGUPTA', 'Unique', 'COLOR_STANDARD_AQUA_LT', 'COLOR_STANDARD_PURPLE_DK', 'COLOR_SC_DARK_TEAL', 'COLOR_SC_LIGHT_TEAL', 'COLOR_SC_MEDIUM_PURPLE', 'COLOR_SC_MEDIUM_TEAL', 'COLOR_SC_DARK_DRAB', 'COLOR_SC_LIGHT_PINK'),
		('LEADER_CLEOPATRA', 'Unique', 'COLOR_STANDARD_AQUA_DK', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_DARKEST_TEAL', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_RED_VIOLET', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_STANDARD_PURPLE_MD'),
		('LEADER_JOHN_CURTIN', 'Unique', 'COLOR_STANDARD_GREEN_DK', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_SC_DARK_GREEN', 'COLOR_STANDARD_BLUE_DK', 'COLOR_STANDARD_WHITE_LT', 'COLOR_STANDARD_GREEN_LT', 'COLOR_STANDARD_GREEN_DK'),
		('LEADER_CYRUS', 'Unique', 'COLOR_SC_LIGHT_GREECE_BLUE', 'COLOR_STANDARD_RED_DK', 'COLOR_SC_LIGHT_PERSIMMON', 'COLOR_STANDARD_BLUE_DK', 'COLOR_STANDARD_AQUA_MD', 'COLOR_STANDARD_RED_DK', 'COLOR_SC_LIGHT_CYAN', 'COLOR_SC_DARK_PURPLE'),
		('LEADER_DIDO', 'Unique', 'COLOR_SC_MEDIUM_PURPLE', 'COLOR_SC_LIGHT_WISTERIA', 'COLOR_SC_DARK_WISTERIA', 'COLOR_SC_LIGHT_GREY', 'COLOR_SC_DARK_PURPLE', 'COLOR_SC_LIGHT_WISTERIA', 'COLOR_SC_LIGHT_GREY', 'COLOR_STANDARD_PURPLE_MD'),
		('LEADER_ELEANOR_ENGLAND', 'Unique', 'COLOR_SC_PINK', 'COLOR_SC_LIGHT_PASTEL_YELLOW', 'COLOR_SC_DARK_PINK', 'COLOR_SC_LIGHT_PASTEL_YELLOW', 'COLOR_STANDARD_RED_LT', 'COLOR_SC_LIGHT_PASTEL_YELLOW', 'COLOR_SC_LIGHT_RED_VIOLET', 'COLOR_SC_LIGHT_PASTEL_YELLOW'),
		('LEADER_ELEANOR_FRANCE', 'Unique', 'COLOR_SC_LIGHT_WISTERIA', 'COLOR_SC_LIGHT_PASTEL_YELLOW', 'COLOR_SC_WISTERIA', 'COLOR_SC_LIGHT_PASTEL_YELLOW', 'COLOR_STANDARD_PURPLE_LT', 'COLOR_SC_LIGHT_PASTEL_YELLOW', 'COLOR_SC_DARK_RED_VIOLET', 'COLOR_SC_LIGHT_PASTEL_YELLOW'),
		('LEADER_GANDHI', 'Unique', 'COLOR_SC_DARK_PURPLE', 'COLOR_STANDARD_AQUA_LT', 'COLOR_SC_LIGHT_RED_VIOLET', 'COLOR_SC_LIGHT_PASTEL_YELLOW', 'COLOR_SC_ORANGE', 'COLOR_SC_TRUE_BLUE', 'COLOR_SC_GREEN', 'COLOR_STANDARD_ORANGE_LT'),
		('LEADER_GENGHIS_KHAN', 'Unique', 'COLOR_SC_BRICK', 'COLOR_SC_COCOA', 'COLOR_STANDARD_ORANGE_MD', 'COLOR_STANDARD_RED_DK', 'COLOR_SC_TAN', 'COLOR_STANDARD_RED_DK', 'COLOR_SC_DARK_CRANBERRY', 'COLOR_STANDARD_ORANGE_MD'),
		('LEADER_GILGAMESH', 'Unique', 'COLOR_STANDARD_BLUE_DK', 'COLOR_STANDARD_ORANGE_LT', 'COLOR_STANDARD_ORANGE_MD', 'COLOR_STANDARD_BLUE_DK', 'COLOR_SC_LIGHT_PASTEL_YELLOW', 'COLOR_STANDARD_BLUE_DK', 'COLOR_SC_TAN', 'COLOR_STANDARD_BLUE_DK'),
		('LEADER_GITARJA', 'Unique', 'COLOR_SC_CRANBERRY', 'COLOR_STANDARD_AQUA_LT', 'COLOR_SC_LIGHT_TEAL', 'COLOR_SC_DARK_RED_VIOLET', 'COLOR_STANDARD_PURPLE_LT', 'COLOR_STANDARD_RED_DK', 'COLOR_STANDARD_AQUA_LT', 'COLOR_STANDARD_AQUA_LT'),
		('LEADER_GORGO', 'Unique', 'COLOR_SC_LIGHT_BRICK', 'COLOR_SC_LIGHT_GREECE_BLUE', 'COLOR_SC_BRICK', 'COLOR_SC_TAN', 'COLOR_SC_PERSIMMON', 'COLOR_STANDARD_WHITE_DK', 'COLOR_STANDARD_YELLOW_DK', 'COLOR_STANDARD_RED_DK'),
		('LEADER_HARDRADA', 'Unique', 'COLOR_SC_TRUE_BLUE', 'COLOR_STANDARD_RED_LT', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_SC_DARK_CRANBERRY', 'COLOR_STANDARD_BLUE_LT', 'COLOR_SC_BRICK', 'COLOR_SC_LIGHT_CRANBERRY', 'COLOR_STANDARD_BLUE_DK'),
		('LEADER_HOJO', 'Unique', 'COLOR_STANDARD_WHITE_LT', 'COLOR_STANDARD_RED_DK', 'COLOR_SC_WISTERIA', 'COLOR_STANDARD_BLUE_DK', 'COLOR_STANDARD_RED_DK', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_SC_TRUE_BLUE', 'COLOR_STANDARD_WHITE_LT'),
		('LEADER_JADWIGA', 'Unique', 'COLOR_STANDARD_RED_LT', 'COLOR_SC_LIGHT_PASTEL_YELLOW', 'COLOR_SC_LIGHTEST_RED_VIOLET', 'COLOR_STANDARD_RED_DK', 'COLOR_SC_RED_VIOLET', 'COLOR_SC_LIGHT_PINK', 'COLOR_SC_LIGHT_PINK', 'COLOR_SC_CRANBERRY'),
		('LEADER_JAYAVARMAN', 'Unique', 'COLOR_STANDARD_MAGENTA_DK', 'COLOR_STANDARD_ORANGE_LT', 'COLOR_STANDARD_YELLOW_DK', 'COLOR_STANDARD_BLUE_DK', 'COLOR_STANDARD_BLUE_DK', 'COLOR_STANDARD_YELLOW_LT', 'COLOR_SC_LIGHT_PERSIMMON', 'COLOR_STANDARD_BLUE_DK'),
		('LEADER_KRISTINA', 'Unique', 'COLOR_STANDARD_BLUE_LT', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_STANDARD_BLUE_MD', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_DARK_GREECE_BLUE', 'COLOR_SC_CYAN', 'COLOR_STANDARD_BLUE_DK'),
		('LEADER_KUPE', 'Unique', 'COLOR_SC_LIGHT_CRANBERRY', 'COLOR_SC_LIGHT_GREECE_BLUE', 'COLOR_STANDARD_RED_MD', 'COLOR_SC_LIGHT_GREY', 'COLOR_STANDARD_WHITE_MD', 'COLOR_STANDARD_WHITE_LT', 'COLOR_SC_MEDIUM_DRAB', 'COLOR_SC_LIGHT_CYAN'),
		('LEADER_LAURIER', 'Unique', 'COLOR_STANDARD_WHITE_LT', 'COLOR_STANDARD_RED_MD', 'COLOR_SC_LIGHT_PINK', 'COLOR_STANDARD_RED_MD', 'COLOR_SC_TRUE_BLUE', 'COLOR_STANDARD_WHITE_LT', 'COLOR_SC_DARK_PASTEL_GREEN', 'COLOR_SC_PINK'),
		('LEADER_LAUTARO', 'Unique', 'COLOR_SC_DARK_GREECE_BLUE', 'COLOR_SC_LIGHT_GREECE_BLUE', 'COLOR_STANDARD_ORANGE_DK', 'COLOR_SC_LIGHTEST_BROWN', 'COLOR_SC_DARKEST_DRAB', 'COLOR_SC_LIGHT_TEAL', 'COLOR_SC_LIGHTEST_BROWN', 'COLOR_STANDARD_BLUE_DK'),
		('LEADER_MATTHIAS_CORVINUS', 'Unique', 'COLOR_SC_DARK_GREEN', 'COLOR_SC_LIGHT_CRANBERRY', 'COLOR_SC_CRANBERRY', 'COLOR_STANDARD_WHITE_LT', 'COLOR_STANDARD_BLUE_MD', 'COLOR_STANDARD_WHITE_DK', 'COLOR_SC_LIGHT_GREEN', 'COLOR_STANDARD_RED_MD'),
		('LEADER_MONTEZUMA', 'Unique', 'COLOR_SC_MEDIUM_TEAL', 'COLOR_STANDARD_RED_MD', 'COLOR_STANDARD_RED_DK', 'COLOR_SC_MEDIUM_TEAL', 'COLOR_SC_LIGHT_TEAL', 'COLOR_SC_DARKEST_DRAB', 'COLOR_SC_LIGHT_DRAB', 'COLOR_SC_DARK_CRANBERRY'),
		('LEADER_MANSA_MUSA', 'Unique', 'COLOR_SC_DARK_PERSIMMON', 'COLOR_SC_LIGHT_PASTEL_YELLOW', 'COLOR_STANDARD_RED_DK', 'COLOR_STANDARD_YELLOW_LT', 'COLOR_SC_MEDIUM_BROWN', 'COLOR_SC_LIGHT_PERSIMMON', 'COLOR_SC_LIGHT_BROWN', 'COLOR_STANDARD_RED_DK'),
		('LEADER_MVEMBA', 'Unique', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_STANDARD_RED_MD', 'COLOR_SC_CRANBERRY', 'COLOR_SC_LIGHT_GREY', 'COLOR_SC_DARK_DRAB', 'COLOR_SC_LIGHT_GREY', 'COLOR_STANDARD_GREEN_MD', 'COLOR_STANDARD_BLUE_DK'),
		('LEADER_PACHACUTI', 'Unique', 'COLOR_SC_PERSIMMON', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_STANDARD_ORANGE_DK', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_SC_DARK_GREEN', 'COLOR_SC_PERSIMMON', 'COLOR_STANDARD_PURPLE_MD', 'COLOR_STANDARD_WHITE_LT'),
		('LEADER_PEDRO', 'Unique', 'COLOR_SC_GREEN', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_TRUE_BLUE', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_STANDARD_GREEN_MD', 'COLOR_STANDARD_BLUE_DK', 'COLOR_SC_LIGHT_GREEN', 'COLOR_SC_BRIGHT_YELLOW'),
		('LEADER_PERICLES', 'Unique', 'COLOR_SC_GREECE_BLUE', 'COLOR_STANDARD_WHITE_LT', 'COLOR_SC_DARK_TEAL', 'COLOR_STANDARD_WHITE_LT', 'COLOR_SC_LIGHT_GREECE_BLUE', 'COLOR_SC_DARK_GREECE_BLUE', 'COLOR_SC_PERSIMMON', 'COLOR_STANDARD_WHITE_DK'),
		('LEADER_PETER_GREAT', 'Unique', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_STANDARD_WHITE_DK', 'COLOR_SC_DARK_DRAB', 'COLOR_STANDARD_YELLOW_LT', 'COLOR_STANDARD_WHITE_LT', 'COLOR_STANDARD_BLUE_MD', 'COLOR_SC_LIGHTEST_TRUE_BLUE', 'COLOR_STANDARD_WHITE_LT'),
		('LEADER_PHILIP_II', 'Unique', 'COLOR_STANDARD_RED_MD', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_DARK_WISTERIA', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_SC_MEDIUM_PURPLE', 'COLOR_SC_BRICK', 'COLOR_STANDARD_RED_LT'),
		('LEADER_POUNDMAKER', 'Unique', 'COLOR_SC_LIGHTEST_BROWN', 'COLOR_STANDARD_ORANGE_DK', 'COLOR_STANDARD_BLUE_DK', 'COLOR_STANDARD_GREEN_MD', 'COLOR_STANDARD_AQUA_DK', 'COLOR_SC_LIGHT_CYAN', 'COLOR_SC_LIGHT_PASTEL_GREEN', 'COLOR_SC_DARK_GREEN'),
		('LEADER_QIN', 'Unique', 'COLOR_SC_MEDIUM_DRAB', 'COLOR_STANDARD_WHITE_LT', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_DARK_GREECE_BLUE', 'COLOR_STANDARD_AQUA_DK', 'COLOR_SC_LIGHT_PASTEL_GREEN', 'COLOR_SC_DARK_CRANBERRY', 'COLOR_STANDARD_PURPLE_LT'),
		('LEADER_ROBERT_THE_BRUCE', 'Unique', 'COLOR_SC_LIGHTEST_TRUE_BLUE', 'COLOR_STANDARD_WHITE_LT', 'COLOR_STANDARD_BLUE_LT', 'COLOR_STANDARD_WHITE_LT', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_STANDARD_RED_MD', 'COLOR_SC_LIGHT_GREECE_BLUE', 'COLOR_SC_DARK_GREECE_BLUE'),
		('LEADER_SALADIN', 'Unique', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_STANDARD_GREEN_DK', 'COLOR_SC_DARK_PASTEL_GREEN', 'COLOR_SC_LIGHT_PASTEL_YELLOW', 'COLOR_SC_MEDIUM_GREY', 'COLOR_STANDARD_YELLOW_LT', 'COLOR_STANDARD_GREEN_DK', 'COLOR_STANDARD_GREEN_LT'),
		('LEADER_SEONDEOK', 'Unique', 'COLOR_SC_DARK_CRANBERRY', 'COLOR_STANDARD_BLUE_LT', 'COLOR_STANDARD_MAGENTA_LT', 'COLOR_STANDARD_MAGENTA_DK', 'COLOR_STANDARD_PURPLE_MD', 'COLOR_SC_PINK', 'COLOR_SC_LIGHTEST_RED_VIOLET', 'COLOR_STANDARD_BLUE_DK'),
		('LEADER_SHAKA', 'Unique', 'COLOR_SC_DARKEST_DRAB', 'COLOR_SC_LIGHT_PASTEL_YELLOW', 'COLOR_STANDARD_ORANGE_DK', 'COLOR_SC_LIGHTEST_BROWN', 'COLOR_SC_LIGHT_PASTEL_GREEN', 'COLOR_STANDARD_RED_MD', 'COLOR_SC_LIGHT_DRAB', 'COLOR_SC_DARK_GREEN'),
		('LEADER_SULEIMAN', 'Unique', 'COLOR_SC_LIGHT_PASTEL_YELLOW', 'COLOR_SC_DARK_GREEN', 'COLOR_SC_DARK_GREEN', 'COLOR_STANDARD_YELLOW_LT', 'COLOR_STANDARD_YELLOW_LT', 'COLOR_STANDARD_RED_MD', 'COLOR_STANDARD_RED_MD', 'COLOR_STANDARD_YELLOW_LT'),
		('LEADER_TAMAR', 'Unique', 'COLOR_STANDARD_WHITE_LT', 'COLOR_STANDARD_ORANGE_MD', 'COLOR_SC_DARK_RED_VIOLET', 'COLOR_SC_LIGHT_PINK', 'COLOR_SC_GREECE_BLUE', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_SC_LIGHT_GREY', 'COLOR_STANDARD_RED_MD'),
		('LEADER_T_ROOSEVELT', 'Unique', 'COLOR_SC_LIGHT_TRUE_BLUE', 'COLOR_STANDARD_WHITE_LT', 'COLOR_STANDARD_BLUE_DK', 'COLOR_SC_LIGHT_GREY', 'COLOR_SC_DARK_CYAN', 'COLOR_SC_LIGHT_GREY', 'COLOR_STANDARD_WHITE_MD2', 'COLOR_STANDARD_BLUE_DK'),
		('LEADER_TOMYRIS', 'Unique', 'COLOR_STANDARD_YELLOW_LT', 'COLOR_STANDARD_RED_MD', 'COLOR_SC_MEDIUM_BROWN', 'COLOR_SC_LIGHT_GREECE_BLUE', 'COLOR_SC_CYAN', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_COCOA', 'COLOR_STANDARD_BLUE_DK'),
		('LEADER_TRAJAN', 'Unique', 'COLOR_STANDARD_PURPLE_DK', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_DARK_PURPLE', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_DARK_WISTERIA', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_DARK_RED_VIOLET', 'COLOR_SC_BRIGHT_YELLOW'),
		('LEADER_VICTORIA', 'Unique', 'COLOR_STANDARD_RED_DK', 'COLOR_STANDARD_WHITE_LT', 'COLOR_SC_PINK', 'COLOR_SC_LIGHT_PASTEL_YELLOW', 'COLOR_SC_LIGHT_PINK', 'COLOR_STANDARD_RED_MD', 'COLOR_SC_LIGHT_WISTERIA', 'COLOR_STANDARD_RED_DK'),
		('LEADER_WILHELMINA', 'Unique', 'COLOR_SC_ORANGE', 'COLOR_STANDARD_WHITE_LT', 'COLOR_SC_LIGHT_TRUE_BLUE', 'COLOR_STANDARD_ORANGE_LT', 'COLOR_STANDARD_ORANGE_MD', 'COLOR_STANDARD_WHITE_LT', 'COLOR_STANDARD_ORANGE_LT', 'COLOR_STANDARD_BLUE_DK'),

		('LEADER_KUBLAI_KHAN_MONGOLIA', 'Unique', 'COLOR_SC_COCOA', 'COLOR_SC_BRICK', 'COLOR_SC_MEDIUM_BROWN', 'COLOR_SC_COCOA', 'COLOR_STANDARD_RED_DK', 'COLOR_STANDARD_YELLOW_LT', 'COLOR_SC_DARK_GREECE_BLUE', 'COLOR_STANDARD_RED_LT'),
		('LEADER_KUBLAI_KHAN_CHINA', 'Unique', 'COLOR_SC_MEDIUM_BROWN', 'COLOR_STANDARD_YELLOW_LT', 'COLOR_SC_COCOA', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_STANDARD_YELLOW_LT', 'COLOR_STANDARD_RED_DK', 'COLOR_SC_DARK_GREECE_BLUE', 'COLOR_STANDARD_RED_LT'),
		('LEADER_LADY_TRIEU', 'Unique', 'COLOR_SC_DARK_TEAL', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_STANDARD_MAGENTA_DK', 'COLOR_STANDARD_RED_MD', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_LIGHT_TEAL', 'COLOR_STANDARD_AQUA_DK'),
		
		('LEADER_SIMON_BOLIVAR', 'Unique', 'COLOR_STANDARD_BLUE_DK', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_CYAN', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_STANDARD_BLUE_DK', 'COLOR_STANDARD_RED_MD', 'COLOR_SC_LIGHT_CYAN'),
		('LEADER_LADY_SIX_SKY', 'Unique', 'COLOR_SC_LIGHT_CYAN', 'COLOR_STANDARD_AQUA_DK', 'COLOR_STANDARD_AQUA_DK', 'COLOR_STANDARD_BLUE_LT', 'COLOR_SC_DARK_CYAN', 'COLOR_SC_TAN', 'COLOR_SC_DARK_DRAB', 'COLOR_STANDARD_YELLOW_LT'),
		('LEADER_MENELIK', 'Unique', 'COLOR_SC_DARK_CYAN', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_DARK_PASTEL_GREEN', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_DARK_GREEN', 'COLOR_SC_LIGHT_CRANBERRY', 'COLOR_SC_CYAN', 'COLOR_SC_BRIGHT_YELLOW'),
		('LEADER_CATHERINE_DE_MEDICI_ALT', 'Unique',  'COLOR_STANDARD_WHITE_LT', 'COLOR_STANDARD_YELLOW_DK', 'COLOR_SC_LIGHT_PERSIMMON', 'COLOR_STANDARD_WHITE_LT', 'COLOR_STANDARD_BLUE_MD', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_GREECE_BLUE', 'COLOR_SC_BRIGHT_YELLOW'),
		('LEADER_T_ROOSEVELT_ROUGHRIDER', 'Unique', 'COLOR_STANDARD_ORANGE_LT', 'COLOR_STANDARD_BLUE_DK', 'COLOR_SC_LIGHT_TRUE_BLUE', 'COLOR_STANDARD_WHITE_LT', 'COLOR_SC_DARK_CYAN', 'COLOR_SC_LIGHT_GREY', 'COLOR_STANDARD_WHITE_MD2', 'COLOR_STANDARD_BLUE_DK'),
		('LEADER_AMBIORIX', 'Unique', 'COLOR_SC_DARKEST_TEAL', 'COLOR_SC_LIGHT_TEAL', 'COLOR_SC_DARK_CYAN', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_STANDARD_GREEN_DK', 'COLOR_SC_LIGHT_GREECE_BLUE', 'COLOR_STANDARD_YELLOW_LT', 'COLOR_STANDARD_GREEN_DK'),
		('LEADER_BASIL', 'Unique', 'COLOR_SC_DARK_WISTERIA', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_STANDARD_WHITE_MD', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_STANDARD_BLUE_LT', 'COLOR_STANDARD_MAGENTA_DK', 'COLOR_STANDARD_RED_MD', 'COLOR_SC_BRIGHT_YELLOW'),
		('LEADER_HAMMURABI', 'Unique', 'COLOR_SC_DARK_GREECE_BLUE', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_SC_LIGHT_BROWN', 'COLOR_STANDARD_YELLOW_LT', 'COLOR_STANDARD_BLUE_LT', 'COLOR_STANDARD_BLUE_DK', 'COLOR_STANDARD_AQUA_DK', 'COLOR_STANDARD_AQUA_LT'),
		('LEADER_JOAO_III', 'Unique', 'COLOR_STANDARD_WHITE_LT', 'COLOR_SC_DARK_GREECE_BLUE', 'COLOR_SC_LIGHT_TEAL', 'COLOR_SC_DARK_GREECE_BLUE', 'COLOR_SC_DARK_GREEN', 'COLOR_SC_LIGHT_CRANBERRY', 'COLOR_SC_DARK_GREECE_BLUE', 'COLOR_STANDARD_WHITE_LT');

--DELETE FROM PlayerColors
--WHERE	Type IN ('LEADER_ALEXANDER', 'LEADER_AMANITORE', 'LEADER_BARBAROSSA', 'LEADER_CATHERINE_DE_MEDICI', 'LEADER_CHANDRAGUPTA', 'LEADER_CLEOPATRA', 'LEADER_JOHN_CURTIN', 'LEADER_CYRUS', 'LEADER_DIDO',
--'LEADER_ELEANOR_ENGLAND', 'LEADER_ELEANOR_FRANCE', 'LEADER_GANDHI', 'LEADER_GENGHIS_KHAN', 'LEADER_GILGAMESH', 'LEADER_GITARJA', 'LEADER_GORGO', 'LEADER_HARDRADA', 'LEADER_HOJO', 'LEADER_JADWIGA', 'LEADER_JAYAVARMAN',
--'LEADER_KRISTINA', 'LEADER_KUPE', 'LEADER_LAURIER', 'LEADER_LAUTARO', 'LEADER_MATTHIAS_CORVINUS', 'LEADER_MONTEZUMA', 'LEADER_MANSA_MUSA', 'LEADER_MVEMBA', 'LEADER_PACHACUTI', 'LEADER_PEDRO', 'LEADER_PERICLES', 'LEADER_PETER_GREAT',
--'LEADER_PHILIP_II', 'LEADER_POUNDMAKER', 'LEADER_QIN', 'LEADER_ROBERT_THE_BRUCE', 'LEADER_SALADIN', 'LEADER_SEONDEOK', 'LEADER_SHAKA', 'LEADER_SULEIMAN', 'LEADER_TAMAR', 'LEADER_T_ROOSEVELT', 'LEADER_TOMYRIS', 'LEADER_TRAJAN',
--'LEADER_VICTORIA', 'LEADER_WILHELMINA', 'LEADER_SIMON_BOLIVAR', 'LEADER_LADY_SIX_SKY', 'LEADER_MENELIK', 'LEADER_T_ROOSEVELT_ROUGHRIDER', 'LEADER_CATHERINE_DE_MEDICI_ALT', 'LEADER_AMBIORIX', 'LEADER_BASIL', 'LEADER_HAMMURABI', 'LEADER_KUBLAI_KHAN_MONGOLIA',
--'LEADER_KUBLAI_KHAN_CHINA', 'LEADER_LADY_TRIEU');

-- Changed Usage -> UseType
INSERT INTO PlayerColors
		(Type,	UseType,	PrimaryColor,	SecondaryColor,	Alt1PrimaryColor,	Alt1SecondaryColor,	Alt2PrimaryColor,	Alt2SecondaryColor,	Alt3PrimaryColor,	Alt3SecondaryColor)
SELECT	Leader,	UseType,	Primary1, 		Secondary1, 	Primary2, 			Secondary2, 		Primary3, 			Secondary3, 		Primary4, 			Secondary4
FROM 	SC_JERSEY_TABLE;


INSERT INTO 	PlayerColors
				(Type,		UseType,		PrimaryColor,				SecondaryColor)
VALUES			('OVERFLOW1', 'Major', 'COLOR_SC_BRICK', 'COLOR_STANDARD_MAGENTA_LT'),
				('OVERFLOW2', 'Major', 'COLOR_SC_DARKEST_DRAB', 'COLOR_SC_PINK'),
				('OVERFLOW3', 'Major', 'COLOR_SC_DARK_GREECE_BLUE', 'COLOR_SC_MEDIUM_TEAL'),
				('OVERFLOW4', 'Major', 'COLOR_STANDARD_MAGENTA_MD', 'COLOR_SC_DARK_PURPLE'),
				('OVERFLOW5', 'Major', 'COLOR_SC_LIGHT_BRICK', 'COLOR_SC_LIGHTEST_BROWN'),
				('OVERFLOW6', 'Major', 'COLOR_SC_DARK_DRAB', 'COLOR_SC_LIGHTEST_RED_VIOLET'),
				('OVERFLOW7', 'Major', 'COLOR_SC_CYAN', 'COLOR_SC_DARK_PURPLE'),
				('OVERFLOW8', 'Major', 'COLOR_SC_DARK_RED_VIOLET', 'COLOR_SC_LIGHT_GREECE_BLUE'),
				('OVERFLOW9', 'Major', 'COLOR_STANDARD_RED_LT', 'COLOR_SC_LIGHT_PINK'),
				('OVERFLOW10', 'Major', 'COLOR_SC_MEDIUM_DRAB', 'COLOR_STANDARD_RED_DK'),
				('OVERFLOW11', 'Major', 'COLOR_STANDARD_BLUE_DK', 'COLOR_SC_LIGHT_CYAN'),
				('OVERFLOW12', 'Major', 'COLOR_STANDARD_MAGENTA_LT', 'COLOR_SC_DARK_RED_VIOLET'),
				('OVERFLOW13', 'Major', 'COLOR_SC_MEDIUM_BROWN', 'COLOR_STANDARD_PURPLE_LT'),
				('OVERFLOW14', 'Major', 'COLOR_STANDARD_GREEN_MD', 'COLOR_SC_DARK_RED_VIOLET'),
				('OVERFLOW15', 'Major', 'COLOR_SC_LIGHT_CYAN', 'COLOR_SC_DARK_PERSIMMON'),
				('OVERFLOW16', 'Major', 'COLOR_SC_RED_VIOLET', 'COLOR_STANDARD_BLUE_DK'),
				('OVERFLOW17', 'Major', 'COLOR_SC_DARK_PERSIMMON', 'COLOR_STANDARD_BLUE_LT'),
				('OVERFLOW18', 'Major', 'COLOR_SC_LIGHT_DRAB', 'COLOR_SC_DARK_PERSIMMON'),
				('OVERFLOW19', 'Major', 'COLOR_STANDARD_BLUE_MD', 'COLOR_STANDARD_PURPLE_LT'),
				('OVERFLOW20', 'Major', 'COLOR_SC_LIGHT_RED_VIOLET', 'COLOR_STANDARD_AQUA_LT'),
				('OVERFLOW21', 'Major', 'COLOR_STANDARD_ORANGE_DK', 'COLOR_SC_LIGHT_DRAB'),
				('OVERFLOW22', 'Major', 'COLOR_SC_DARK_GREEN', 'COLOR_STANDARD_GREEN_LT'),
				('OVERFLOW23', 'Major', 'COLOR_SC_GREECE_BLUE', 'COLOR_STANDARD_BLUE_DK'),
				('OVERFLOW24', 'Major', 'COLOR_SC_LIGHTEST_RED_VIOLET', 'COLOR_SC_LIGHTEST_BROWN'),
				('OVERFLOW25', 'Major', 'COLOR_SC_PERSIMMON', 'COLOR_SC_DARK_PURPLE'),
				('OVERFLOW26', 'Major', 'COLOR_SC_GREEN', 'COLOR_SC_LIGHT_TEAL'),
				('OVERFLOW27', 'Major', 'COLOR_SC_TRUE_BLUE', 'COLOR_SC_DARK_TEAL'),
				('OVERFLOW28', 'Major', 'COLOR_STANDARD_RED_DK', 'COLOR_SC_LIGHT_WISTERIA'),
				('OVERFLOW29', 'Major', 'COLOR_SC_COCOA', 'COLOR_STANDARD_AQUA_LT'),
				('OVERFLOW30', 'Major', 'COLOR_STANDARD_GREEN_LT', 'COLOR_SC_CRANBERRY'),
				('OVERFLOW31', 'Major', 'COLOR_SC_LIGHT_TRUE_BLUE', 'COLOR_STANDARD_ORANGE_MD'),
				('OVERFLOW32', 'Major', 'COLOR_SC_DARK_CRANBERRY', 'COLOR_STANDARD_GREEN_LT'),
				('OVERFLOW33', 'Major', 'COLOR_SC_LIGHT_BROWN', 'COLOR_SC_DARK_GREEN'),
				('OVERFLOW34', 'Major', 'COLOR_SC_LIGHT_GREEN', 'COLOR_SC_DARK_RED_VIOLET'),
				('OVERFLOW35', 'Major', 'COLOR_SC_LIGHT_GREECE_BLUE', 'COLOR_SC_DARKEST_DRAB'),
				('OVERFLOW36', 'Major', 'COLOR_STANDARD_RED_MD', 'COLOR_SC_TAN'),
				('OVERFLOW37', 'Major', 'COLOR_STANDARD_ORANGE_MD', 'COLOR_STANDARD_YELLOW_LT'),
				('OVERFLOW38', 'Major', 'COLOR_STANDARD_GREEN_DK', 'COLOR_SC_LIGHT_PASTEL_GREEN'),
				('OVERFLOW39', 'Major', 'COLOR_STANDARD_BLUE_LT', 'COLOR_STANDARD_BLUE_DK'),
				('OVERFLOW40', 'Major', 'COLOR_SC_DARK_PINK', 'COLOR_SC_DARK_PURPLE'),
				('OVERFLOW41', 'Major', 'COLOR_SC_LIGHT_PERSIMMON', 'COLOR_SC_MEDIUM_PURPLE'),
				('OVERFLOW42', 'Major', 'COLOR_SC_DARK_PASTEL_GREEN', 'COLOR_STANDARD_AQUA_DK'),
				('OVERFLOW43', 'Major', 'COLOR_SC_LIGHTEST_TRUE_BLUE', 'COLOR_STANDARD_PURPLE_DK'),
				('OVERFLOW44', 'Major', 'COLOR_SC_CRANBERRY', 'COLOR_SC_LIGHT_DRAB'),
				('OVERFLOW45', 'Major', 'COLOR_STANDARD_YELLOW_DK', 'COLOR_STANDARD_MAGENTA_LT'),
				('OVERFLOW46', 'Major', 'COLOR_SC_LIGHT_PASTEL_GREEN', 'COLOR_STANDARD_PURPLE_DK'),
				('OVERFLOW47', 'Major', 'COLOR_STANDARD_PURPLE_DK', 'COLOR_SC_WISTERIA'),
				('OVERFLOW48', 'Major', 'COLOR_SC_LIGHT_CRANBERRY', 'COLOR_SC_LIGHT_CYAN'),
				('OVERFLOW49', 'Major', 'COLOR_SC_ORANGE', 'COLOR_SC_DARKEST_TEAL'),
				('OVERFLOW50', 'Major', 'COLOR_SC_DARKEST_TEAL', 'COLOR_STANDARD_BLUE_LT'),
				('OVERFLOW51', 'Major', 'COLOR_STANDARD_PURPLE_MD', 'COLOR_SC_LIGHTEST_BROWN'),
				('OVERFLOW52', 'Major', 'COLOR_SC_PINK', 'COLOR_STANDARD_BLUE_DK'),
				('OVERFLOW53', 'Major', 'COLOR_STANDARD_ORANGE_LT', 'COLOR_SC_DARK_WISTERIA'),
				('OVERFLOW54', 'Major', 'COLOR_SC_DARK_TEAL', 'COLOR_STANDARD_AQUA_LT'),
				('OVERFLOW55', 'Major', 'COLOR_SC_DARK_WISTERIA', 'COLOR_SC_LIGHT_PINK'),
				('OVERFLOW56', 'Major', 'COLOR_SC_LIGHT_PINK', 'COLOR_STANDARD_GREEN_DK'),
				('OVERFLOW57', 'Major', 'COLOR_SC_TAN', 'COLOR_STANDARD_BLUE_DK'),
				('OVERFLOW58', 'Major', 'COLOR_STANDARD_AQUA_MD', 'COLOR_STANDARD_MAGENTA_DK'),
				('OVERFLOW59', 'Major', 'COLOR_STANDARD_PURPLE_LT', 'COLOR_STANDARD_MAGENTA_DK'),
				('OVERFLOW60', 'Major', 'COLOR_STANDARD_WHITE_MD', 'COLOR_SC_TAN'),
				('OVERFLOW61', 'Major', 'COLOR_SC_LIGHTEST_BROWN', 'COLOR_SC_DARK_CYAN'),
				('OVERFLOW62', 'Major', 'COLOR_SC_MEDIUM_TEAL', 'COLOR_SC_DARK_GREEN'),
				('OVERFLOW63', 'Major', 'COLOR_SC_WISTERIA', 'COLOR_STANDARD_RED_DK'),
				('OVERFLOW64', 'Major', 'COLOR_SC_MEDIUM_GREY', 'COLOR_SC_LIGHT_TEAL'),
				('OVERFLOW65', 'Major', 'COLOR_STANDARD_YELLOW_MD', 'COLOR_STANDARD_WHITE_LT'),
				('OVERFLOW66', 'Major', 'COLOR_SC_LIGHT_TEAL', 'COLOR_SC_PERSIMMON'),
				('OVERFLOW67', 'Major', 'COLOR_SC_LIGHT_WISTERIA', 'COLOR_SC_DARK_GREECE_BLUE'),
				('OVERFLOW68', 'Major', 'COLOR_STANDARD_WHITE_MD2', 'COLOR_STANDARD_RED_DK'),
				('OVERFLOW69', 'Major', 'COLOR_SC_BRIGHT_YELLOW', 'COLOR_SC_DARK_PURPLE'),
				('OVERFLOW70', 'Major', 'COLOR_STANDARD_AQUA_LT', 'COLOR_SC_DARK_RED_VIOLET'),
				('OVERFLOW71', 'Major', 'COLOR_STANDARD_MAGENTA_DK', 'COLOR_STANDARD_AQUA_MD'),
				('OVERFLOW72', 'Major', 'COLOR_SC_LIGHT_GREY', 'COLOR_SC_DARK_GREEN'),
				('OVERFLOW73', 'Major', 'COLOR_STANDARD_YELLOW_LT', 'COLOR_STANDARD_WHITE_MD'),
				('OVERFLOW74', 'Major', 'COLOR_STANDARD_AQUA_DK', 'COLOR_SC_DARK_PINK'),
				('OVERFLOW75', 'Major', 'COLOR_SC_DARK_PURPLE', 'COLOR_SC_PINK'),
				('OVERFLOW76', 'Major', 'COLOR_STANDARD_WHITE_LT', 'COLOR_SC_DARK_PURPLE'),
				('OVERFLOW77', 'Major', 'COLOR_SC_LIGHT_PASTEL_YELLOW', 'COLOR_STANDARD_RED_MD'),
				('OVERFLOW78', 'Major', 'COLOR_SC_DARK_CYAN', 'COLOR_SC_LIGHT_DRAB'),
				('OVERFLOW79', 'Major', 'COLOR_SC_MEDIUM_PURPLE', 'COLOR_STANDARD_MAGENTA_LT');