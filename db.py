import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
a1 = int(input())
if a1 == 1:
    lat = int(input())
    long = int(input())
    name = input()
    photo_url = input()
    cursor.execute('INSERT INTO Mashup (lat, long, name, photo_url) VALUES (?, ?, ?, ?)',
                   [lat, long, name, photo_url])
elif a1 == 2:
    name = input()
    cursor.execute('SELECT * FROM Mapohui WHERE name LIKE ?', ['%' + name + '%'])
elif a1 == 3:
    id = int(input())
    cursor.execute('DELETE FROM Mapohui WHERE id=?', [id])

result = cursor.fetchall()
print(result)

connection.commit()