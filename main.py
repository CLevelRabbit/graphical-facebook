# Sorts = popularity release_date title
import sys
import os
import pandas as pd
import requests
# This facebook_scraper is a local patched version, also saving the page URL
# diff file is provided
from facebook_scraper import get_posts, enable_logging

FIELDS = [
    #   (field_name, default_value),
    ('post_id', None),
    ('post_text', None),
    ('time', None),
    ('reaction_count', 0),
    ('comments', 0),
    ('shares', 0),
    ('post_url', None),
    ('page_url', None),
]

REACTION_FIELDS = [
    ('like', 0),
    ('love', 0),
    ('haha', 0),
    ('wow', 0),
    ('care', 0),
    ('angry', 0),
    ('sad', 0)
]

IMAGES_POST_PATH = './images/{}'
COOKIE_FILE = 'facebook.com_cookies.txt'
PAGE_NAME = 'hapshuta'
DB_PATH_FMT = '{}_posts.csv'


def download_images(post):
    img_dir = IMAGES_POST_PATH.format(post['post_id'])
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    for i, img_link in enumerate(post['images']):
        if not img_link:
            print('\tERROR! Image link is missing!!!')
            continue
        with open(img_dir + f'/{i}.png', 'wb') as handler:
            img_data = requests.get(img_link).content
            handler.write(img_data)


def main():
    if len(sys.argv) == 2:
        page_name = sys.argv[1]
    else:
        page_name = PAGE_NAME

    db_path = DB_PATH_FMT.format(page_name)

    # Find out if first write or not
    if os.path.exists(db_path):
        write_kwargs = {'mode': 'a', 'index': False, 'header': False}
    else:
        write_kwargs = {'index': False}

    # enable_logging()

    # You can set "start_url=<>" to the page url you wish to start from.
    for i, post in enumerate(
            get_posts(page_name, page_limit=200000000, cookies=COOKIE_FILE, extra_info=True)):
        post_dict = {key: post.get(key, default) for key, default in FIELDS}
        reactions = post.get('reactions', {})
        if not reactions:
            reactions = {}
        post_dict.update({key: reactions.get(key, default) for key, default in REACTION_FIELDS})

        images = post.get('images', [])
        if not images:
            images = []
        images_cnt = len(images)
        post_dict['images_cnt'] = images_cnt
        if images_cnt > 0:
            download_images(post)

        print('Saving post! %d' % i)
        print(post_dict)
        df = pd.json_normalize([post_dict])
        df.to_csv(db_path, **write_kwargs)
        write_kwargs = {'mode': 'a', 'index': False, 'header': False}


if __name__ == '__main__':
    main()
