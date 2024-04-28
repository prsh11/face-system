import sqlite3 as sql


class Database:

    def __init__(self, file):
        self.file = file
        self.conn = sql.connect(file)

    def create_table(self):
        with self.conn:

            self.conn.execute(
                "CREATE TABLE TEACHERS (id int, name varchar(50), department varchar(50), joinDate date, PRIMARY KEY (id))"
            )

    def __insert(self, sql_string, *params):
        cur = self.conn.cursor()
        cur.execute(sql_string, params)
        self.conn.commit()

    def insert(self, name, department, joinDate):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM TEACHERS ORDER BY id desc limit 1")
            row = cur.fetchall()
            id = 1 if len(row) == 0 else row[0][0] + 1
            self.__insert(
                "INSERT INTO TEACHERS VALUES (?, ?, ?, ?)",
                id,
                name,
                department,
                joinDate,
            )


test = Database("db.sqlite")
test.create_table()
test.insert("Prashant", "physics", "2007/10/11")
test.insert("John Wick", "physics", "2007/10/11")
