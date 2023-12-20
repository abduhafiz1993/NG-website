from cs50 import SQL

db = SQL("sqlite:///database.db")
abdu ="abdu"
Types = rows = db.execute(
            "SELECT * FROM Users WHERE username = ?", abdu,
        )
for type in Types:
    print(type)