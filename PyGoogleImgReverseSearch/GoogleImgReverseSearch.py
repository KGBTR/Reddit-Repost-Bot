import requests
import re


class GoogleImgReverseSearch:
    re_pattern = re.compile(r'href="/imgres\?imgurl=(.+?)&amp;imgrefurl=(.+?)&amp'.encode(), re.IGNORECASE)

    @staticmethod
    def reverse_search(pic_url, filter_site=None, page_start=0, page_end=3, lang='en', region="US", skip_same_img_ref=True):
        hl_param = f"{lang}-{region}"

        pic_url_c = pic_url.split('/')[-1]  # this is for i.redd.it domains
        set_of_results = set()
        for page_indexer in range(page_start * 10, page_end * 10, 10):
            new_page_results = GoogleImgReverseSearch._perform_search(pic_url, hl_param, filter_site, page_indexer)
            for res in new_page_results:
                ref_decoded = res[0].decode('utf-8')
                if skip_same_img_ref and pic_url_c in ref_decoded:
                    continue
                set_of_results |= {(res[1].decode('utf-8'), ref_decoded)}

            new_page_results_l = len(new_page_results)
            if (page_indexer != 0 and new_page_results_l < 9) or new_page_results_l < 4:
                set_of_results.add(("out_of_pages", "out_of_pages"))
                break

        return set_of_results

    @staticmethod
    def _perform_search(pic_url, hl_param, filter_site, start):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/527.36 (KHTML, like Gecko) Chrome/84.0.4183.121 Safari/537.36'
        }
        params = {
            'image_url': pic_url,
            'hl': hl_param,
            'as_sitesearch': filter_site,
            'safe': 'images',
            'cr': '',
            'start': start,

            # 'as_q': '',
            # 'as_epq': '',
            # 'as_oq': '',
            # 'as_eq': '',
            # 'imgsz': '',
            # 'imgar': '',
            # 'imgc': '',
            # 'imgcolor': '',
            # 'imgtype': '',
            # 'as_filetype': '',
        }
        response = requests.get('https://www.google.com/searchbyimage', params=params, allow_redirects=False)
        tbs_response = requests.get(response.headers['location'], headers=headers, params={'hl': hl_param})

        if tbs_response.status_code == 429:
            raise Exception("fuuuuuuuuucking recaptcha")

        # with open(f"{start}.html", "w") as f:
        #     f.write(str(tbs_response.content))

        results_filtered = GoogleImgReverseSearch.re_pattern.findall(tbs_response.content)
        return results_filtered
