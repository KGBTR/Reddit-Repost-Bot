from CompareImageHashes import HashedImage, ImgNotAvailable
from rStuff import PostFetcherPushShift
from time import sleep


class HashCollector:
    def __init__(self, rBot, hashdb):
        self.rBot = rBot
        self.hash_database = hashdb
        self.hash_database.create_table(
            "Hashes", "postid TEXT, dhash TEXT, ahash TEXT, phash TEXT, UNIQUE(postid)"
        )
        self.hash_database.create_table("beforeafter", "before TEXT, after TEXT")

        before_after = self.hash_database.fetch_before_and_after()
        if not bool(before_after):
            self.hash_database.initialize_before_and_after()
            before_after = self.hash_database.fetch_before_and_after()
        before, after = before_after[0], before_after[1]

        if before == "None":
            newest_post_fetched = PostFetcherPushShift(
                subs=["KGBTR"], before_or_after="after", limit=1
            ).fetch_posts()
            newest_post = list(newest_post_fetched)[0]
            before = after = newest_post.created_utc
            print(f"newest post timestamp fetched: {before}")

        # self.fetcher_before = PostFetcherPushShift(
        #     subs=["KGBTR"],
        #     before_or_after="before",
        #     pagination_param=before,
        #     limit=100,
        #     only_image=True,
        # )
        self.fetcher_after = PostFetcherPushShift(
            subs=["KGBTR"],
            before_or_after="after",
            pagination_param=after,
            limit=100,
            only_image=True,
        )

    def start_collectin(self):
        # # RESETS EVERYTHING INCLUDING ALL THE HASHES!!:
        # self.hash_database.delete_table("hashes")
        # self.hash_database.reset_before_and_after()
        # exit()

        # # INSERT FAKE DATA FOR TESTING
        # pic_url = ""
        # hashedimg = HashedImage(pic_url, calculate_on_init=True)
        # self.hash_database.insert_data("t3_aaaaaa", str(hashedimg.dhash), str(hashedimg.ahash), str(hashedimg.phash))
        # exit()

        # b_a_dec = 0
        while True:
            # if b_a_dec % 4 == 0:
            print("fetched from after")
            for post in self.fetcher_after.fetch_posts():
                try:
                    hashedimg = HashedImage(post.url, calculate_on_init=True)
                except ImgNotAvailable:
                    print(
                        f"skipping a submission with deleted image: {post.id_} {post.url}"
                    )
                    continue
                self.hash_database.insert_data(
                    post.id_,
                    str(hashedimg.dhash),
                    str(hashedimg.ahash),
                    str(hashedimg.phash),
                )
            sleep(30)
            # else:
            #     print("fetched from before")
            #     for post in self.fetcher_before.fetch_posts():
            #         try:
            #             hashedimg = HashedImage(post.url, calculate_on_init=True)
            #         except ImgNotAvailable:
            #             print(
            #                 f"skipping a submission with deleted image: {post.id_} {post.url}"
            #             )
            #             continue
            #         self.hash_database.insert_data(
            #             post.id_,
            #             str(hashedimg.dhash),
            #             str(hashedimg.ahash),
            #             str(hashedimg.phash),
            #         )

            # b_a_dec += 1
            self.hash_database.update_before_and_after(
                before=None,  # self.fetcher_before.pagination_param,
                after=self.fetcher_after.pagination_param,
            )
