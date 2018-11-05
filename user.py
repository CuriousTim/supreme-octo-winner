import sqlite3
from pypika import Query, Table, Field
from ast import literal_eval as make_tuple

class UserManager:
    def __init__(self, dbpath):
        # connect to sqlite database
        self.conn = sqlite3.connect(dbpath)
        self.c = self.conn.cursor()

        # create user table if not already existing
        self.c.execute('''CREATE TABLE IF NOT EXISTS
                          users
                          (
                              username varchar[255],
                              password varchar[255]
                          )''')

    def createUser(self, username, password):
        """
        Insert a new user with given information into the database if there
        currently exists no other same username in the database
        """
        if len(self.findByUsername(username)) == 0:
            users = Table('users')
            q = Query.into(users).insert(username, password)
            self.c.execute(q.get_sql())

    def findByUsername(self, username):
        """
        Returns tuple of user data if found otherwise return empty tuple
        """
        users = Table('users')
        q = Query.from_(users).select('*').where(users.username == username)
        self.c.execute(q.get_sql())
        res = self.c.fetchone()
        return () if res == None else res

    def verifyPassword(self, username, password):
        """
        Return true if a given username is in the database and given password
        matches password in database for username
        """
        # Check that username is in the database
        if len(self.findByUsername(username)) == 0:
            return False

        users = Table('users')
        q = Query.from_(users).select('password').where(users.username == username)
        self.c.execute(q.get_sql())
        return make_tuple(str(self.c.fetchone()))[0] == password
