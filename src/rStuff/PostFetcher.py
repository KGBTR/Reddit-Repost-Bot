from .rUtils import rPost
import requests


class PostFetcher:
    def __init__(self, bot=None, subs=None, limit=50, sort_by='new', pagination=True, stop_if_saved=False, skip_if_nsfw=False,
                 before_or_after='before', pagination_param=None, multiname=None, only_image=False):
        assert any(before_or_after == ba for ba in ['before', 'after'])
        assert (subs is not None) != (multiname is not None)

        self.bot = bot
        if bot is None:
            self.r_session = requests.session()
            self.r_session.headers = {"User-Agent": "#placeholder"}

        self.subs = subs
        self.params = {"limit": limit}
        self.sort_by = sort_by
        self.pagination = pagination
        self.stop_if_saved = stop_if_saved
        self.skip_if_nsfw = skip_if_nsfw
        self.only_image = only_image
        self.before_or_after = before_or_after
        self.pagination_param = pagination_param

        self.last_fetched_ids = []

        if self.pagination_param is not None:
            self.params.update({self.before_or_after: self.pagination_param})
        self._fallback_index = 0
        if self.before_or_after == 'before':
            self._fallback_index_incrementer = 1
            self._pagination_post_indexer = 0
        elif self.before_or_after == 'after':
            self._pagination_post_indexer = self._fallback_index_incrementer = -1

        base_h = "https://www.reddit.com" if bot is None else self.bot.base
        if multiname is not None:
            self._uri = f"{base_h}/user/{self.bot.bot_username}/m/{multiname}/{self.sort_by}.json"
        else:
            self._uri = f"{base_h}/r/{'+'.join(self.subs)}/{self.sort_by}.json"

    def fetch_posts(self):
        if self.bot is not None:
            posts_req = self.bot.handled_req('GET', self._uri, params=self.params).json()
        else:
            posts_req = self.r_session.get(self._uri, params=self.params).json()
        posts = posts_req["data"]["children"]
        posts_len = posts_req["data"]["dist"]
        if self.before_or_after == "before":
            posts_iter = posts
        elif self.before_or_after == "after":
            posts_iter = reversed(posts)
        else:
            raise NotImplementedError

        for post in posts_iter:
            the_post = rPost(post)
            if the_post.id_ in self.last_fetched_ids or (self.stop_if_saved and the_post.is_saved):
                break
            if (self.only_image and not the_post.is_img) or (self.skip_if_nsfw and the_post.over_18):
                continue
            yield the_post

        if posts_len != 0 and self.bot is not None and not the_post.is_saved and self.stop_if_saved:
            self.bot.save_thing_by_id(posts[self._pagination_post_indexer]['data']['name'])

        if self.pagination:
            if posts_len != 0:
                if self.before_or_after == "before":
                    self.last_fetched_ids.extend([post['data']['name'] for post in posts[:15]])
                elif self.before_or_after == "after":
                    self.last_fetched_ids.extend([post['data']['name'] for post in posts[-15:]])
                self.last_fetched_ids = self.last_fetched_ids[-15:]

                self._fallback_index = 0
                self.pagination_param = posts[self._pagination_post_indexer]['data']['name']
            else:
                try:
                    self.pagination_param = self.last_fetched_ids[self._fallback_index % 15]
                except IndexError:
                    pass
                self._fallback_index += self._fallback_index_incrementer
            self.params.update({self.before_or_after: self.pagination_param})
