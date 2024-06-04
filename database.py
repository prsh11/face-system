import sqlite3 as sql


class Database:

    def __init__(self, file):
        self.file = file
        self.conn = sql.connect(file)

    def create_tables(self):
        with self.conn:

            try:
                self.conn.execute(
                    "CREATE TABLE TEACHERS (id int, name varchar(50), department varchar(50), joinDate date, PRIMARY KEY (id))"
                )
            except sql.OperationalError:
                pass
            try:
                self.conn.execute(
                    "CREATE TABLE ATTENDANCE (id int, present int, date date, FOREIGN KEY (id) REFERENCES TEACHERS(id))"
                )
            except sql.OperationalError:
                pass

    def __insert(self, sql_string, *params):
        cur = self.conn.cursor()
        cur.execute(sql_string, params)
        self.conn.commit()

    def __query(self, sql_string, *params):
        cur = self.conn.cursor()
        cur.execute(sql_string, params)
        return cur.fetchall()

    def insert(self, name, department, joinDate):
        with self.conn:
            row = self.__query("SELECT * FROM TEACHERS ORDER BY id desc limit 1")
            id = 1 if len(row) == 0 else row[0][0] + 1
            self.__insert(
                "INSERT INTO TEACHERS VALUES (?, ?, ?, ?)",
                id,
                name,
                department,
                joinDate,
            )

    def insert_record(self, id, date):
        with self.conn:
            query = self.__query(
                "SELECT * FROM ATTENDANCE WHERE id=? AND date=?", id, date
            )
            if len(query) == 0:
                self.__insert("INSERT INTO ATTENDANCE VALUES (?, ?, ?)", id, 1, date)

    def get_data(self, id):
        with self.conn:
            return self.__query("SELECT * FROM TEACHERS WHERE id=?", id)[0]
