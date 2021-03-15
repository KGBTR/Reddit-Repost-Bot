from .rUtils import rPostPushShift
import requests
from time import sleep


class PostFetcherPushShift:
    def __init__(self, subs=None, limit=50, sort='desc', pagination=True, skip_if_nsfw=False,
                 pagination_param=None, only_image=False, before_or_after='before'):

        self.s = requests.session()
        self.s.headers = {}
        self.sub = subs[0]
        self.s.params = {"limit": limit}
        self.pagination = pagination
        self.skip_if_nsfw = skip_if_nsfw
        self.only_image = only_image
        self.before_or_after = before_or_after

        if self.before_or_after == 'before':
            self._pagination_post_indexer = -1
        elif self.before_or_after == 'after':
            self._pagination_post_indexer = 0

        self.pagination_param = pagination_param
        if pagination_param is not None:
            self.s.params.update({self.before_or_after: pagination_param})

        self._uri = f"https://api.pushshift.io/reddit/search/submission/?subreddit={self.sub}&sort={sort}&sort_type=created_utc&size={limit}"

    def fetch_posts(self):
        posts_req = self.s.get(self._uri)
        if posts_req.status_code != 200:
            sleep(30)
            return
        posts = posts_req.json()["data"]
        for post in posts:
            the_post = rPostPushShift(post)
            if (self.only_image and not the_post.is_img) or (self.skip_if_nsfw and the_post.over_18):
                continue
            yield the_post

        if bool(posts) and self.pagination:
            self.pagination_param = posts[self._pagination_post_indexer]['created_utc']
            self.s.params.update({self.before_or_after: self.pagination_param})
