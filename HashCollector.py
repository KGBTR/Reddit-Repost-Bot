from CompareImageHashes import HashedImage
from time import sleep


class HashCollector:
    def __init__(self, rBot, hashdb):
        self.rBot = rBot
        self.hash_database = hashdb
        self.hash_database.create_table("Hashes", "postid TEXT, dhash TEXT, ahash TEXT, phash TEXT, UNIQUE(postid)")
        self.hash_database.create_table("beforeafter", "before TEXT, after TEXT")

        before_after = self.hash_database.fetch_before_and_after()
        if not bool(before_after):
            self.hash_database.initialize_before_and_after()
            before_after = self.hash_database.fetch_before_and_after()
        before, after = before_after
        before = None if before == 'None' else before
        after = None if after == 'None' else after

        self.fetcher_before = self.rBot.init_new_fetcher(stop_if_saved=False, subs=['KGBTR'], before_or_after='before', pagination_param=before, limit=100)
        self.fetcher_after = self.rBot.init_new_fetcher(stop_if_saved=False, subs=['KGBTR'], before_or_after='after', pagination_param=after, limit=100)

    def start_collectin(self):
        # self.hash_database.delete_table("hashes")
        # self.hash_database.reset_before_and_after()
        while True:
            for post in self.fetcher_before.fetch_posts():
                print(f"{post} from before")
                if post.is_img:
                    pic_url = post.gallery_media[0] if post.is_gallery else post.url
                    hashedimg = HashedImage(pic_url, calculate_on_init=True)
                    self.hash_database.insert_data(post.id_, str(hashedimg.dhash), str(hashedimg.ahash), str(hashedimg.phash))

            print()

            for post in self.fetcher_after.fetch_posts():
                print(f"{post} from after")
                if post.is_img:
                    pic_url = post.gallery_media[0] if post.is_gallery else post.url
                    hashedimg = HashedImage(pic_url, calculate_on_init=True)
                    self.hash_database.insert_data(post.id_, str(hashedimg.dhash), str(hashedimg.ahash), str(hashedimg.phash))

            self.hash_database.update_before_and_after(self.fetcher_before.pagination_param, self.fetcher_after.pagination_param)
            sleep(5)
            print('---------------------')
