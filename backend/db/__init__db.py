import sqlite3
import subprocess

connection = sqlite3.connect('images.db')

subprocess.run(["ls", "-l"]) 

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO images (filename, filepath) VALUES (?, ?)",
            ('profile', './asdfasdf')
        )

connection.commit()
connection.close()