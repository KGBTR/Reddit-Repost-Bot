from environ import DATABASE_URL
import psycopg2
from logger import logger


class HashDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        self.cur = self.conn.cursor()

        self.logger = logger
        self.logger.disabled = False
        self.logger.info("HashDB initilaized")

    def create_table(self, name, values):
        # values = postid TEXT, dhash TEXT
        sql = f"""CREATE TABLE IF NOT EXISTS {name} ({values});"""
        self.cur.execute(sql)
        self.conn.commit()

    def insert_data(self, postid, dhash, ahash, phash):
        try:
            self.cur.execute(
                "INSERT INTO Hashes (postid, dhash, ahash, phash) VALUES (%s, %s, %s, %s);",
                (postid, dhash, ahash, phash),
            )
            self.logger.info(f"saved into the db: {postid}")
        except psycopg2.errors.UniqueViolation:
            self.logger.warning(f"same post skipping: {postid}")
        finally:
            self.conn.commit()

    def query(self, base_post_id):
        self.cur.execute("SELECT postid, ahash, phash, dhash FROM Hashes WHERE postid != %s;", (base_post_id,))
        for row in self.cur:
            yield row

    def fetch_all(self, table_name):
        sql = f"SELECT * FROM {table_name};"
        self.cur.execute(sql)
        return self.cur.fetchall()

    def update_before_and_after(self, before=None, after=None):
        ba_l = []
        if before is not None:
            ba_l.append(f"before = '{before}'")
        if after is not None:
            ba_l.append(f"after = '{after}'")
        sql = f"UPDATE beforeafter SET {','.join(ba_l)}"
        self.cur.execute(sql)
        self.conn.commit()

    def reset_before_and_after(self):
        self.update_before_and_after("None", "None")

    def initialize_before_and_after(self):
        self.cur.execute(
            "INSERT INTO beforeafter (before, after) VALUES ('None', 'None');"
        )
        self.conn.commit()

    def fetch_before_and_after(self):
        self.cur.execute("SELECT * FROM beforeafter;")
        res = self.cur.fetchone()
        return res

    def delete_table(self, table_name):
        sql = f"DROP TABLE {table_name}"
        self.cur.execute(sql)
        self.conn.commit()

    def custom_execute(self, sql):
        self.cur.execute(sql)
        self.conn.commit()
