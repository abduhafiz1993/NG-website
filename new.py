from cs50 import SQL

db = SQL("sqlite:///database.db")
Types = db.execute("select * from Types")
for type in Types:
    print(type["type_name"])