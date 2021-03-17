from environ import DATABASE_URL
import psycopg2
from CompareImageHashes import CompareImageHashes
import logging


class HashDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        self.cur = self.conn.cursor()

        logging.basicConfig(
            level=logging.INFO,
            datefmt="%H:%M",
            format="%(asctime)s, %(levelname)s: %(message)s",
        )
        self.logger = logging.getLogger("hoarder")
        self.logger.disabled = False
        self.logger.info("hash db initilaized")

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

    def query(self, base_hashes, selected_hash, min_similarity_percentage, skip_post_id):
        comparer_p = CompareImageHashes(base_hashes[0])
        comparer_d = CompareImageHashes(base_hashes[1])
        comparer_a = CompareImageHashes(base_hashes[2])
        sql = f"SELECT postid, ahash, phash, dhash FROM Hashes WHERE postid != '{skip_post_id}';"
        # self.cur.execute("SELECT postid, %d FROM Hashes;", (selected_hash,))
        self.cur.execute(sql)
        similar_posts = []
        for row in self.cur:
            post_id, ahash, phash, dhash = row[0], row[1], row[2], row[3]
            similarity_phash = comparer_p.hamming_distance_percentage(phash)
            similarity_dhash = comparer_d.hamming_distance_percentage(dhash)
            similarity_ahash = comparer_a.hamming_distance_percentage(ahash)
            similarity = (similarity_dhash + similarity_phash + similarity_ahash) / 3
            if similarity >= min_similarity_percentage:
                similar_posts.append({"similarity": similarity, "post_id": post_id})
        if bool(similar_posts):
            return similar_posts
        else:
            return None

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
