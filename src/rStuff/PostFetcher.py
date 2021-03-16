from .rUtils import rPost


class PostFetcher:
    def __init__(self, bot, subs=None, limit=50, sort_by='new', pagination=True, stop_if_saved=False, skip_if_nsfw=False,
                 before_or_after='before', pagination_param=None, multiname=None, only_image=False):
        assert any(before_or_after == ba for ba in ['before', 'after'])
        assert (subs is not None) != (multiname is not None)

        self.bot = bot

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

        if multiname is not None:
            self._uri = f"{self.bot.base}/user/{self.bot.bot_username}/m/{multiname}/{self.sort_by}"
        else:
            self._uri = f"{self.bot.base}/r/{'+'.join(self.subs)}/{self.sort_by}"

    def fetch_posts(self):
        posts_req = self.bot.handled_req('GET', self._uri, params=self.params).json()
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
                self.pagination_param = the_post.id_
                self.params.update({self.before_or_after: self.pagination_param})
                break
            if (self.only_image and not the_post.is_img) or (self.skip_if_nsfw and the_post.over_18):
                continue
            yield the_post

        if posts_len != 0 and not the_post.is_saved and self.stop_if_saved:
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
