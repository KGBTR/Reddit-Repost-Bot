import requests


rBase = "https://www.reddit.com"

# Some stuff.. ------------------
turkish_subs = ["Turkey", "TurkeyJerky", "testyapiyorum", "KGBTR", "svihs", "burdurland"]
# -------------------------------


class rNotif:
    def __init__(self, notif):
        # self.kind = notif['kind']  # kind
        content = notif['data']
        self.author = content.get('author')  # summoner
        self.body = content.get('body', "")  # body
        self.subreddit = content.get('subreddit', "")  # sub
        if self.subreddit in turkish_subs:
            self.lang = 'tr'
        else:
            self.lang = 'en'
        self.parent_id = content.get('parent_id')  # the post or mentioner
        self.id_ = content.get('name')  # answer to this. represents the comment with t1 prefix
        self.rtype = content.get('type')  # comment_reply or user_mention

        try:
            context = content['context']  # /r/SUB/comments/POST_ID/TITLE/COMMENT_ID/
            context_split = str(context).split('/')
            self.post_id = 't3_' + context_split[4]  # post id with t3 prefix added
        except:
            pass
        # self.id_no_prefix = context_split[6]  # comment id without t1 prefix

    def __repr__(self):
        return f"(NotifObject: {self.id_})"


class rPost:
    def __init__(self, post):
        content = post['data']
        self.id_ = content['name']  # answer to this. represents the post with t3 prefix
        self.permalink = content['permalink']
        self.created_utc = content['created_utc']
        self.id_without_prefix = content['id']
        self.is_self = content['is_self']  # text or not
        self.is_video = content['is_video']  # video or not
        self.author = content['author']  # author
        self.title = content['title']

        if content.get('crosspost_parent_list') is not None:
            gallery_content = content['crosspost_parent_list'][0]
        else:
            gallery_content = content

        self.is_gallery = gallery_content.get('is_gallery')
        if bool(self.is_gallery):
            if gallery_content.get('gallery_data') is None:
                self.is_img = False
            else:
                self.gallery_media = []
                for gd in gallery_content['gallery_data']['items']:
                    gallery_id = gd['media_id']
                    try:
                        img_m = gallery_content['media_metadata'][gallery_id]['m'].split('/')[-1]
                    except KeyError:
                        img_m = 'jpg'
                    self.gallery_media.append(f"https://i.redd.it/{gallery_id}.{img_m}")
                self.url = self.gallery_media[0]
                self.is_img = True
        else:
            self.url = content['url']  # url
            self.is_img = self._is_img_post()
        self.subreddit = content['subreddit']
        self.subreddit_name_prefixed = content['subreddit_name_prefixed']
        self.over_18 = content['over_18']
        if self.subreddit in turkish_subs:
            self.lang = 'tr'
        else:
            self.lang = 'en'
        self.is_saved = content['saved']

    def __repr__(self):
        return f"(PostObject: {self.id_})"

    def __eq__(self, other):
        if self.id_ == other.id_:
            return True
        else:
            return False

    def _is_img_post(self):
        if not (self.is_self or self.is_video) and self.url.split(".")[-1].lower() in ["jpg", "jpeg", "png", "tiff", "bmp"]:
            return True
        else:
            return False


class rPostPushShift:
    def __init__(self, post):
        content = post
        self.id_ = 't3_' + content['id']  # answer to this. represents the post with t3 prefix
        self.permalink = content['permalink']
        self.created_utc = content['created_utc']
        self.id_without_prefix = content['id']
        self.is_self = content['is_self']  # text or not
        self.is_video = content['is_video']  # video or not
        self.author = content['author']  # author
        self.title = content['title']

        if content.get('crosspost_parent_list') is not None:
            gallery_content = content['crosspost_parent_list'][0]
        else:
            gallery_content = content

        self.is_gallery = gallery_content.get('is_gallery')
        if bool(self.is_gallery):
            self.gallery_media = []
            if gallery_content.get('gallery_data') is None:
                self.is_img = False
            else:
                for gd in gallery_content['gallery_data']['items']:
                    gallery_id = gd['media_id']
                    try:
                        img_m = gallery_content['media_metadata'][gallery_id]['m'].split('/')[-1]
                    except KeyError:
                        img_m = 'jpg'
                    self.gallery_media.append(f"https://i.redd.it/{gallery_id}.{img_m}")
                self.url = self.gallery_media[0]
                self.is_img = True
        else:
            self.url = content['url']  # url
            self.is_img = self._is_img_post()
        self.subreddit = content['subreddit']
        self.subreddit_name_prefixed = 'r/' + self.subreddit
        self.over_18 = content['over_18']
        if self.subreddit in turkish_subs:
            self.lang = 'tr'
        else:
            self.lang = 'en'

    def __repr__(self):
        return f"(PostObject: {self.id_})"

    def __eq__(self, other):
        if self.id_ == other.id_:
            return True
        else:
            return False

    def _is_img_post(self):
        if not (self.is_self or self.is_video) and self.url.split(".")[-1].lower() in ["jpg", "jpeg", "png", "tiff", "bmp"]:
            return True
        else:
            return False

    def is_img_available(self):
        return requests.head(self.url) == 200
