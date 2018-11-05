import sqlite3

conn = sqlite3.connect('example.db')
c = conn.cursor()

# Create table
c.execute('''
          CREATE TABLE users
          (
              username varchar[255],
              password varchar[255]
          )
          ''')

# Insert a fake user
c.execute('INSERT INTO users VALUES ("root", "password")')

for row in c.execute('SELECT * FROM users'):
    print(row)
