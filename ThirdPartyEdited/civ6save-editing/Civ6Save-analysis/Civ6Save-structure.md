# .Civ6Save Structure Rundown (WIP)

### Section 1: Header

ByteLength | Type | Purpose | DefaultValue
--- | --- | --- | ---
4 | String | File Header | "CIV6"
4 | Int32 | ? | 0x01?
4 | Int32 | ? | 0x20?
4 | Int32 | ? | 0x05d9b099?
4 | Int32 | ? | 0x05?
8 | ? | GAME_SPEED String Length | N/A
Variable | String | GAME_SPEED | N/A
4 | Int32 | ? | 0x0b835c40?
4 | Int32 | ? | 0x05
8 | ? | MAPSIZE String Length | N/A
Variable | String | MAPSIZE | N/A
4 | Int32 | ? | 0x0efe6c64?
4 | Int32 | ? | 0x14?
4 | Int32 | ? | 0x80000000?
4 | Int32 | ? | 0x00?
4 | UInt32 | Unix Epoch | N/A
4 | Int32 | Possibly overflow for Unix Epoch | 0x00?
4 | Int32 | ? | 0x0f32e71d?
4 | Int32 | ? | 0x05

### Section 2: JSON's

ByteLength | Type | Purpose | DefaultValue
--- | --- | --- | ---
8 | ? | Length of JSON Group 1 | N/A
Variable | JSON | ? | N/A
4 | Int32 | ? | 0x12f52ff3?
4 | Int32 | ? | 0x05?
8 | ? | Length of JSON Group 2 | N/A
Variable | JSON | ? | N/A
4 | Int32 | ? | 0x1ab13eef?
4 | Int32 | ? | 0x18?
8 | ? | Combined Length of Next 4 Row Items | N/A
4 | Int32 | ? | 0x01?
4 | Int32 | ? | 0x14c0?
4 | Int32 | Length of Proceeding Buffer | N/A
Variable | Zlib Buffer | ? | N/A

// TODO: Continue this

4 | Int32 | ? | B0 13 4C 1E?
4 | Int32 | ? | 06 00 00 00?
8 | UInt16+UInt16+UInt16+UInt16 | Length of savename+0x00+0x21+multiplier | N/A
Variable | savename
4 | Int32 | ? | F9 37 6F 30?
4 | Int32 | ? | 05 00 00 00?
8 | UInt16+UInt16+UInt16+UInt16 | Length of Platform+0x00+0x21+multiplier | N/A
Variable | PC? 
4 | Int32 | ? | DA 45 05 3A?
4 | Int32 | ? | 05 00 00 00?
8 | UInt16+UInt16+UInt16+UInt16 | Length of Version+0x00+0x21+multiplier | N/A
Variable | Version?
4 | Int32 | ? | DC 0C 4C 41?
4 | Int32 | ? | 03 00 00 00?
2x 00 00 00 00
01 00 00 00
4 | Int32 | ? | 27 60 4C 58?
4 | Int32 | ? | 05 00 00 00?
8 | ? | Length of JSON Group 3 | N/A
Variable | JSON | ? | N/A

4 | Int32 | ? | EB 1B A6 61?
4 | Int32 | ? | 03 00 00 00?
3x 00 00 00 00

4 | Int32 | ? | A1 B2 B7 6B?
4 | Int32 | ? | 05 00 00 00?
8 | UInt16+UInt16+UInt16+UInt16 | Length of leader+0x00+0x21+multiplier | N/A
Variable | leader?
4 | Int32 | ? | 2A 63 0A 76?
4 | Int32 | ? | 05 00 00 00?
8 | ? | Length of JSON Group leader | N/A
Variable | JSON | ? | N/A
4 | Int32 | ? | 81 6F 54 7C?
4 | Int32 | ? | 03 00 00 00?

2x 00 00 00 00
4 | Int32 | ? | E7 5E 68 E9?
4 | Int32 | ? | A8 16 B4 7F?
4 | Int32 | ? | 05 00 00 00?
8 | UInt16+UInt16+UInt16+UInt16 | Length of difficulty+0x00+0x21+multiplier | N/A
Variable | difficulty?
4 | Int32 | ? | EF 8C F1 83?
4 | Int32 | ? | 03 00 00 00?
3x 00 00 00 00

4 | Int32 | ? | 5C AE 27 84?
4 | Int32 | ? | 0B 00 00 00? # player count?
4 | Int32 | ? | 00 00 00 11?
00 00 00 00
01 00 00 00
0A 00 00 00
00 00 00 04
00 00 00 00
04 00 00 00
54 5F C4 04
05 00 00 00
8 | UInt16+UInt16+UInt16+UInt16 | Length of some uuid+0x00+0x21+multiplier | N/A
Variable | uuid?
72 E1 34 30
05 00 00 00
8 | UInt16+UInt16+UInt16+UInt16 | Length of json mods+0x00+0x21+multiplier | N/A
Variable | JSON | ? | N/A
92 F5 B0 6D
05 00 00 00
00 00 00 20
01 00 00 00
00 00 00 00
10 07 58 F4
05 00 00 00
8 | UInt16+UInt16+UInt16+UInt16 | Length of some number str+0x00+0x21+multiplier | N/A
Variable | number | ? | N/A
15 87 98 85
03 00 00 00
2x 00 00 00 00
37 00 65 FF
B3 07 42 91
18 00 00 00

8 | UInt24+UInt16+UInt16 | Length of some zlib and following+0x01+0x21+multiplier | N/A, D9 18 01 21
01 00 00 00
80 30 02 00
00 00 01 00
Variable | zlib

95 DA BC 9D
05 00 00 00
8 | UInt16+UInt16+UInt16+UInt16 | Length of leader name json +0x00+0x21+multiplier | N/A
Variable | JSON | ? | N/A

CD 93 9B A6
05 00 00 00
8 | UInt16+UInt16+UInt16+UInt16 | Length of mapsize json +0x00+0x21+multiplier | N/A
Variable | JSON | ? | N/A

BB E4 9A AF
05 00 00 00
8 | UInt16+UInt16+UInt16+UInt16 | Length of civilization name +0x00+0x21+multiplier | N/A
Variable | civilization name | ? | N/A

9D 2C E6 BD
02 00 00 00
2x 00 00 00 00
02 00 00 00
DE 25 59 C4
05 00 00 00
8 | UInt16+UInt16+UInt16+UInt16 | Length of ruleset name +0x00+0x21+multiplier | N/A
Variable | ruleset name | ? | N/A

15 C3 52 C6
01 00 00 00
2x 00 00 00 00
01 00 00 00
31 A4 28 D0
05 00 00 00
8 | UInt16+UInt16+UInt16+UInt16 | Length of ruleset name json +0x00+0x21+multiplier | N/A
Variable | JSON | ? | N/A

20 08 76 D2
18 00 00 00
8 | UInt16+UInt16+UInt16+UInt16 | Length of some zlib and following+0x00+0x21+multiplier | N/A, D9 18 01 21
01 00 00 00
24 20 00 00
72 12 00 00
zlib

B5 68 DD DF
03 00 00 00
2x 00 00 00 00
00 C0 9B FF
55 0E 17 E7
05 00 00 00
8 | UInt16+UInt16+UInt16+UInt16 | Length of era name +0x00+0x21+multiplier | N/A
Variable | era name | ? | N/A

4E 22 CA EF
02 00 00 00
2x 00 00 00 00
01 00 00 00
D8 40 E5 F4
05 00 00 00
8 | UInt16+UInt16+UInt16+UInt16 | Length of some uuid+0x00+0x21+multiplier | N/A
Variable | uuid?

C3 D4 D3 FA
05 00 00 00
8 | UInt16+UInt16+UInt16+UInt16 | Length of gamespeed json +0x00+0x21+multiplier | N/A
Variable | JSON | ? | N/A

06 00 00 00
01 00 00 00
03 00 00 00
99 55 59 28
01 00 00 00
2x 00 00 00 00
01 00 00 00
A7 68 38 7F
01 00 00 00
2x 00 00 00 00
01 00 00 00
56 72 CE EC
01 00 00 00
2x 00 00 00 00
2x 01 00 00 00

... something about civs and states


24 95 06 35 05 00 00 00
8 | UInt16+UInt16+UInt16+UInt16 | Length of map type json +0x00+0x21+multiplier | N/A
Variable | JSON | ? | N/A

...

8B 30 00 2C 05 00 00 00
8 | UInt16+UInt16+UInt16+UInt16 | Length of gamespeed json +0x00+0x21+multiplier | N/A
Variable | JSON | ? | N/A


...
ruleset name
LOC_ERA_ANCIENT_NAME json
...

game name
LOC_RULESET_NAME json

...

uuid
dlc
next civ 

...

LOC_MAP_SMALL_CONTINENTS

...

...

zlib main



5F 5E CD E8