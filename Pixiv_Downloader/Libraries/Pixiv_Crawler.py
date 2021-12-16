import os
import shutil
import hashlib
import cloudscraper
import imageio
from zipfile import ZipFile
from datetime import datetime

class Pixiv():
    client_id = 'MOBrBDS8blbauoSck0ZfDbtuzpyT'
    client_secret = 'lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj'
    hash_secret = '28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c'
    
    access_token = None
    login_user_id = 0
    refresh_token = None

    def __init__(self, **requests_kwargs):
        self.s = cloudscraper.create_scraper()
        self.requests_kwargs = requests_kwargs
        self.app_host = 'https://app-api.pixiv.net'
        self.web_host = 'https://pixiv.net'
        
        self.headers = {
            #'User-Agent': 'PixivIOSApp/7.9.4',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'referer': 'www.pixiv.net'
        }
        
        self.pages = {
            'daily': {None: 10, 'illust': 10, 'ugoira': 2, 'manga': 10},
            'daily_r18': {None: 2, 'illust': 2, 'ugoira': 2, 'manga': 2},
            'weekly': {None: 10, 'illust': 10, 'ugoira': 2, 'manga': 10},
            'weekly_r18': {None: 2, 'illust': 2, 'ugoira': 1, 'manga': 2},
            'monthly': {None: 10, 'illust': 5, 'manga': 2},
            'rookie': {None: 6, 'illust': 6, 'manga': 2},
            'original': {None: 6},
            'male': {None: 10},
            'male_r18': {None: 6},
            'female': {None: 10},
            'female_r18': {None: 6},
            'r18g': {None: 1, 'illust': 1}
        }
        
        self.illust_type = {
            '0': 'illust',
            '1': 'manga',
            '2': 'ugoira'
        }

    def parse_url(self, url, mode='get', headers=None, data=None, params=None, stream=False):
        if not headers:
            headers = self.headers
        if mode == 'get':
            return self.s.get(url, headers=headers, data=data, params=params, stream=stream, **self.requests_kwargs)
        if mode == 'post':
            return self.s.post(url, headers=headers, data=data, params=params, stream=stream, **self.requests_kwargs)
        if mode == 'delete':
            return self.s.delete(url, headers=headers, data=data, params=params, stream=stream, **self.requests_kwargs)
            
    def login(self, pixiv_id=None, password=None, refresh_token=None):
        local_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00:00')
        headers = {
            'User-Agent': 'PixivIOSApp/7.9.4',
            'X-Client-Time': local_time,
            'X-Client-Hash': hashlib.md5(f'{local_time}{self.hash_secret}'.encode('utf-8')).hexdigest()
        }
        url = 'https://oauth.secure.pixiv.net/auth/token'
        data = {
            'get_secure_url': 1,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        if pixiv_id and password:
            data['grant_type'] = 'password'
            data['username'] = pixiv_id
            data['password'] = password
        elif refresh_token:
            data['grant_type'] = 'refresh_token'
            data['refresh_token'] = refresh_token or self.refresh_token
            
        res = self.parse_url(url, 'post', headers=headers, data=data)
        
        token = None
        if res.status_code == 200:
            token = res.json()
            self.access_token = token['access_token']
            self.user_id = token['user']['id']
            self.refresh_token = token['refresh_token']
            self.headers['Authorization'] = 'Bearer {access_token}'.format(access_token=token['response']['access_token'])
            self.headers['host'] = 'app-api.pixiv.net'
        return token
  
    def user_detail(self, user_id, filter=None, is_pc=False):
        if is_pc:
          url = f'{self.web_host}/ajax/user/{user_id}'
          return self.parse_url(url).json()
        url = f'{self.app_host}/v1/user/detail'
        params = {
            'user_id': user_id,
            'filter': filter
        }
        return self.parse_url(url, params=params).json()

    def user_illust(self, user_id, type=None, tags=None, restrict=None, filter=None, offset=None, is_pc=False):
        if is_pc:
            url = f'{self.web_host}/ajax/user/{user_id}/profile/all'
            return self.parse_url(url).json()
        url = f'{self.app_host}/v1/user/illusts'
        params = {
            'user_id': user_id,
            'type': type,
            'tags': tags,
            'restrict': restrict,
            'filter': filter,
            'offset': offset
        }
        return self.parse_url(url, params=params).json()
        
    def user_bookmark_illust(self, user_id, restrict=None, filter=None, offset=None):
        url = f'{self.app_host}/v1/user/bookmarks/illust'
        params = {
            'user_id': user_id,
            'restrict': restrict,
            'filter': filter,
            'offset': offset
        }
        return self.parse_url(url, params=params).json()

    def user_following(self, user_id, restrict=None, filter=None, offset=None):
        url = f'{self.app_host}/v1/user/following'
        params = {
            'user_id': user_id,
            'restrict': restrict,
            'filter': filter,
            'offset': offset
        }
        return self.parse_url(url, params=params).json()
   
    def user_mypixiv(self, user_id, restrict=None, filter=None, offset=None):
        url = f'{self.app_host}/v1/user/mypixiv'
        params = {
            'user_id': user_id,
            'restrict': restrict,
            'filter': filter,
            'offset': offset
        }
        return self.parse_url(url, params=params).json()

    def illust_detail(self, illust_id, is_pc=False):
        if is_pc:
            url = f'{self.web_host}/touch/ajax/illust/details'
        else:
            url = f'{self.app_host}/v1/illust/detail'
        params = {
            'illust_id': illust_id
        }
        return self.parse_url(url, params=params).json()
        
    def illust_pages(self, illust_id):
        url = f'https://www.pixiv.net/ajax/illust/{illust_id}/pages'
        return self.parse_url(url).json()

    def illust_comments(self, illust_id, include_total_comments=None, offset=None):
        url = f'{self.app_host}/v1/illust/comments'
        params = {
            'illust_id': illust_id,
            'include_total_comments': include_total_comments,
            'offset': offset
        }
        return self.parse_url(url, params=params).json()

    def illust_recommended(self, illust_id, filter=None, min_bookmark_id_for_recent_illust=None, max_bookmark_id_for_recommend=None, offset=None, include_ranking_illusts=None, include_privacy_policy=None):
        url = f'{self.app_hosts}/v1/illust/recommended'
        params = {
            'illust_id': illust_id,
            'filter': filter,
            'min_bookmark_id_for_recent_illust': min_bookmark_id_for_recent_illust,
            'max_bookmark_id_for_recommend': max_bookmark_id_for_recommend,
            'offset': offset,
            'include_ranking_illusts': include_ranking_illusts,
            'include_privacy_policy': include_privacy_policy
        }
        return self.parse_url(url, params=params).json()

    def illust_ranking(self, mode=None, content=None, index='1', filter=None, date=None, offset=None, is_pc=False):
        params = {
            'mode': mode,
            'filter': filter,
            'date': date,
            'offset': offset
        }
        if is_pc:
            url = f'{self.web_host}/ranking.php'
            params['content'] = content
            params['p'] = min(index, self.pages[mode][content])
            params['format'] = 'json'
        else:
            url = f'{self.app_host}/v1/illust/ranking'
        return self.parse_url(url, params=params).json()

    def trending_tags_illust(self, filter=None):
        url = f'{self.app_host}/v1/trending-tags/illust/'
        params = {
            'filter': filter
        }
        return self.parse_url(url, params=params).json()

    def search_illust(self, word, include_translated_tag_results='true', merge_plain_keyword_results='true', filter=None, search_target=None, sort=None, duration=None, start_date=None, end_date=None, offset=None):
        url = f'{self.app_host}/v1/search/illust'
        params = {
            'word': word,
            'include_translated_tag_results': include_translated_tag_results,
            'merge_plain_keyword_results': merge_plain_keyword_results,
            'filter': filter,
            'search_target': search_target,
            'sort': sort,
            'duration': duration,
            'start_date': start_date,
            'end_date': end_date,
            'offset': offset
        }
        return self.parse_url(url, params=params).json()

    def search_user(self, word, filter=None, sort=None, duration=None, offset=None):
        url = f'{self.app_host}/v1/search/user'
        params = {
            'word': word,
            'filter': filter,
            'sort': sort,
            'duration': duration,
            'offset': offset
        }
        return self.parse_url(url, params=params).json()
        
    def ugoira_metadata(self, illust_id, is_pc=False):
        if is_pc:
            url = f'{self.web_host}/ajax/illust/{illust_id}/ugoira_meta'
            return self.parse_url(url).json()
        url = f'{self.app_host}/v1/ugoira/metadata'
        params = {
            'illust_id': illust_id
        }
        return self.parse_url(url, params=params).json()

    def illust_follow(self, restrict='public', filter=None):
        url = f'{self.app_host}/v2/illust/follow'
        params = {
            'restrict': restrict,
            'filter': filter
        }
        return self.parse_url(url, params=params).json()
        
    def illust_related(self, illust_id, filter=None, seed_illust_ids=None, offset=None):
        url = f'{self.app_host}/v2/illust/related'
        params = {
            'illust_id': illust_id,
            'filter': filter,
            'seed_illust_ids': seed_illust_ids,
            'offset': offset
        }
        return self.parse_url(url, params=params).json()

    def illust_bookmark_detail(self, illust_id, filter=None):
        url = f'{self.app_host}/v2/illust/bookmark/detail'
        params = {
            'illust_id': illust_id,
            'filter': filter
        }
        return self.parse_url(url, params=params).json()
        
    def illust_bookmark_add(self, illust_id, restrict='public', tags=None):
        url = f'{self.app_host}/v2/illust/bookmark/add'
        data = {
            'illust_id': illust_id,
            'restrict': restrict,
            'tags': tags
        }
        return self.parse_url(url, mode='post', data=data).json()

    def illust_bookmark_delete(self, illust_id):
        url = f'{self.app_host}/v1/illust/bookmark/delete'
        data = {
            'illust_id': illust_id
        }
        return self.parse_url(url, mode='post', data=data).json()
        
    def illust_bookmark_detail(self, illust_id):
        url = f'{self.app_host}/v2/illust/bookmark/detail'
        params = {
            'illust_id': illust_id
        }
        return self.parse_url(url, params=params).json()

    def illust_bookmark_users(self, illust_id):
        url = f'{self.app_host}/v1/illust/bookmark/users'
        params = {
            'illust_id': illust_id
        }
        return self.parse_url(url, params=params).json()

    def user_follow(self, user_id, restrict='public'):
        url = f'{self.app_host}/v1/user/follow/add'
        data = {
            'user_id': user_id,
            'restrict': restrict
        }
        return self.parse_url(url, mode='post', data=data).json()
        
    def user_unfollow(self, user_id, restrict='public'):
        url = f'{self.app_host}/v1/user/follow/delete'
        data = {
            'user_id': user_id,
            'restrict': restrict
        }
        return self.parse_url(url, mode='post', data=data).json()

    def user_follow_detail(self, user_id):
        url = f'{self.app_host}/v1/user/follow/detail'
        params = {
            'user_id': user_id
        }
        return self.parse_url(url, params=params).json()

    def spotlight_articles(self, offset=None):
        url = f'{self.app_host}/v1/spotlight/articles'
        params = {
            'offset': offset
        }
        return self.parse_url(url, params=params).json()
        
    def emoji(self):
        url = f'{self.app_host}/v1/emoji'
        return self.parse_url(url).json()

    def user_list(self, user_id, filter=None, offset=None):
        url = f'{self.app_host}/v2/user/list'
        params = {
            'user_id': user_id,
            'filter': filter,
            'offset': offset
        }
        return self.parse_url(url, params=params).json()
        
    def illust_new(self, max_illust_id=None):
        url = f'{self.app_host}/v1/illust/new'
        params = {
            'max_illust_id': max_illust_id
        }
        return self.parse_url(url, params=params).json()
        
    def illust_series(self, illust_series_id):
        url = f'{self.app_host}/v1/illust/series'
        params = {
            'illust_series_id': illust_series_id
        }
        return self.parse_url(url, params=params).json()
        
    def img_data(self, url):
      headers = {
        'referer': 'https://app-api.pixiv.net/'
      }
      return self.parse_url(url, headers=headers, stream=True).raw.read()

    def download(self, url, delay=None):
        headers = {
            'referer': 'https://app-api.pixiv.net/'
        }
        res = self.parse_url(url, headers=headers, stream=True)
        file_name = os.path.basename(url)
        with open(file_name, 'wb') as handle:
            shutil.copyfileobj(res.raw, handle)
        del res
        if delay:
            with ZipFile(file_name, 'r') as zip:
                new_path = file_name.split('.')[0]
                zip.extractall(new_path)
                list = zip.namelist()
                shutil.move(file_name, new_path)
            with imageio.get_writer(f'{new_path}.gif', mode='I', format='GIF-PIL', duration=delay) as writer:
                for file in list:
                    img = imageio.imread(os.path.join(new_path, file))
                    writer.append_data(img)
            shutil.rmtree(new_path)
