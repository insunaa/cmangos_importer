# TBC-Classic to CMaNGOS Character converter
Python script to convert exported character-data to an importable pdump format

Uses the data gathered by a forked variant of the Questionably Epic Gear Exporter to recreate a character from Vanilla/TBC Classic servers on CMaNGOS Servers.

Usage: `python3 main.py exported_character.txt expansion`  
The `expansion` parameter is optional and can either be `0` for 1.13.x -> 1.12.x or `1`(default) for 2.5.x -> 2.4.3

To import the characters into said cmangos server direct access to the server's filesystem is required. So the final integration either needs to be done by the administrator of said cmangos server, or in some automated way.

The data of the forked QE Addon has to be saved into a file. This file can then be parsed and converted by this python script into a new file that is compatible with CMaNGOS' pdump functionality

To load the data into the server it is imperative that the resulting file *NOT* be applied directly to the database, as that will lead to errors and possibly a corrupted database.

Data *must* be imported with the server `.pdump load` command. To use that one would drop the file created by this script into the working directory of the cmangos mangosd binary and then execute `.pdump load char_dump.sql accountname` whereby "accountname" can be replaced either by the name of the account that the character will be assigned to, or the guid of the account the character will be assigned to.

The Addon+Importer combo import the following things:

Character Name, Character Race, Character Class, Character Gender, Equipped Gear, All items in bags\*, All learned spells, All learned Talents, All learned Professions+recipes, Actionbar Buttons\*\*, the character's pet\*\*\*

\* Items in the Bank are *not* imported. If you need items from your bank, put them into your inventory before you export.

\*\* Macros are not imported, because the server currently does not support importing them. They are however exported to the `macros-cache.txt` file, which you can copy to the WTF folder in your 2.4.3 client, specifically:
`World of Warcraft/WTF/Account/<ACCOUNTNAME>/<ServerName>/<CHARACTERNAME>/macros-cache.txt` they will then appear as regular macros in your `/macros` menu and can be placed into the actionbar.
Right now this only works for character-specific macros, not account-wide macros. That may be added later.

\*\*\* Pet appearance can't be ported, only the general class of pet. Health values and creature values remain, however no learned abilities are ported at this time.

If you have ideas for improvements or find bugs, please open an issue, as I'm sure there are some bugs.

Big thanks to https://github.com/slavanorm/ for his major refactor of this script.
