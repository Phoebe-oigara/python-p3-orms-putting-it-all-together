import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
       CURSOR.execute("DROP TABLE IF EXISTS dogs")

    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.breed))
        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, breed):
        dog1 = Dog(name, breed)
        dog1.save()
        return dog1
    
    @classmethod
    def new_from_db(cls, row):
        if row is not None and len(row) >= 3:
            dog = cls(row[1], row[2])
            dog.id = row[0]
            return dog
        else:
            return None
        
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """

        rows = CURSOR.execute(sql).fetchall()
        cls.all = [cls.new_from_db(row) for row in rows]
        return cls.all

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        if row is not None:
            return cls.new_from_db(row)
        else:
            return None
        
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM dogs
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        if row is not None:
            return cls.new_from_db(row)
        else:
            return None
