import sqlite3

connection = sqlite3.connect(":memory:")

cursor = connection.cursor()

sql_file = open("Colors.sql")
sql_as_string = sql_file.read()
cursor.executescript(sql_as_string)

leader_colors = {}
for row in cursor.execute("SELECT * FROM SC_JERSEY_TABLE"):
    leader = row[0][7:]
    colors = [x for x in row[2:]]
    leader_colors[leader] = colors
    print("\'" + leader + "\': [\'" + "\', \'".join(colors) + "\'],")




