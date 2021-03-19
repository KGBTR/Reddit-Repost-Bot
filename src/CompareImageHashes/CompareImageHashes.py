from PIL import Image, UnidentifiedImageError
import imagehash
import requests


class ImgNotAvailable(Exception):
    pass


class HashedImage:
    def __init__(self, pic_url, calculate_on_init=False):
        self.opened_stream = self._get_pilimg(pic_url)
        if calculate_on_init:
            self.ahash = self.get_ahash()
            self.dhash = self.get_dhash()
            self.phash = self.get_phash()
            # self.crophash = self.get_crophash()

    def get_ahash(self):
        return imagehash.average_hash(self.opened_stream)

    def get_dhash(self):
        return imagehash.dhash(self.opened_stream)

    def get_phash(self):
        return imagehash.phash(self.opened_stream)

    # def get_crophash(self):
    #     return imagehash.crop_resistant_hash(self.opened_stream)

    def _get_pilimg(self, url):
        try:
            img = requests.get(url, stream=True)
            img.raise_for_status()
            img.raw.decode_content = True
            pilimg = Image.open(img.raw)
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, UnidentifiedImageError):
            raise ImgNotAvailable
        return pilimg


class CompareImageHashes:
    def __init__(self, base):
        self.base_img_hash = self._get_imagehash_type_from_any(base)
        self.base_img_hash_l = float(len(self.base_img_hash))

    def hamming_distance_percentage(self, hash2):
        hash2_ = self._get_imagehash_type_from_any(hash2)
        hamming_dist = hash2_ - self.base_img_hash
        return 100.0 * (1.0 - hamming_dist / self.base_img_hash_l)

    def _get_imagehash_type_from_any(self, anything):  # only url, ImageHash and hex str is accepted
        if isinstance(anything, str):
            if anything.startswith("http"):
                return HashedImage(
                    anything, calculate_on_init=False
                ).get_phash()  # default to phash
            elif "," in anything:
                str_split = anything.split(",")
                return imagehash.ImageMultiHash(
                    [imagehash.hex_to_hash(segment) for segment in str_split]
                )
            else:
                return imagehash.hex_to_hash(anything)
        elif isinstance(anything, (imagehash.ImageMultiHash, imagehash.ImageHash)):
            return anything
        else:
            raise NotImplementedError
