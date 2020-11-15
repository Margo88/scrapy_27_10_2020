import scrapy
from scrapy.http import HtmlResponse
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from instaparser.items import InstaparserItem

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    # логин, пароль
    insta_login = ''
    insta_passwd = ''
    #мои кумиры
    parse_user = ['buzova86', '_larisa_guzeeva_', 'stas_mihailoff']
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    relations = {'subscriptions': {'hash': 'd04b0a864b4b54837c0d870b0e77e076',
                                   'json_key': 'edge_follow'},
                 'subscribers': {'hash': 'c76146de99bb02f6415203be841dd25a',
                                 'json_key': 'edge_followed_by'}}

    def parse(self, response:HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.insta_login_link,
            method = 'POST',
            callback = self.auth,
            formdata = {'username' : self.insta_login,
                        'enc_password' : self.insta_passwd},
            headers = {'X-CSRFToken':csrf}
        )

    def auth(self, response:HtmlResponse):
        jdata = response.json()
        if jdata.get('authenticated'):
            for user in self.parse_user:
                yield response.follow(
                    f'/{user}/',
                    callback=self.user_data_parse,
                    cb_kwargs={'username':user}
                )

    def user_data_parse(self, response:HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {
            'id' : user_id,
            'include_reel' : 'true',
            'fetch_mutual' : 'false',
            'first' : 50
        }

        for relation_type in self.relations.keys():
            related_users = f'{self.graphql_url}query_hash={self.relations[relation_type]["hash"]}&{urlencode(variables)}'
            yield response.follow(
                related_users,
                callback=self.related_users_parse,
                cb_kwargs={
                    'username' : username,
                    'user_id' : user_id,
                    'variables' : deepcopy(variables),
                    'relation_type' : relation_type
                }
            )

    def related_users_parse(self, response:HtmlResponse, username, user_id, variables, relation_type):
        jdata = response.json()
        page_info = jdata.get('data').get('user').get(self.relations[relation_type]['json_key']).get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            related_users = f'{self.graphql_url}query_hash={self.relations[relation_type]["hash"]}&{urlencode(variables)}'
            yield response.follow(
                related_users,
                callback=self.related_users_parse,
                cb_kwargs={
                    'username': username,
                    'user_id': user_id,
                    'variables': deepcopy(variables),
                    'relation_type': relation_type
                }
            )
        related_users_list = jdata.get('data').get('user').get(self.relations[relation_type]['json_key']).get('edges')
        for user in related_users_list:
            item = InstaparserItem(
                parsed_user = username, #исходный юзер, чьи подписки/подписчиков парсим
                relation_type = relation_type,
                user_id = user['node']['id'],
                username = user['node']['username'],
                full_name = user['node']['full_name'],
                photo = user['node']['profile_pic_url']
            )
            yield item

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

