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

IMAGES_POST_PATH = '{}_images'
IMAGE_PATH = '{}/{}'
COOKIE_FILE = 'facebook.com_cookies.txt'
PAGE_NAME = 'hapshuta'
DB_PATH_FMT = '{}_posts.csv'


def download_images(post, images_path):
    img_dir = os.path.join(images_path, post['post_id'])
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
    is_group = True
    if len(sys.argv) == 2:
        page_name = sys.argv[1]
    else:
        page_name = PAGE_NAME

    db_path = DB_PATH_FMT.format(page_name)
    images_path = IMAGES_POST_PATH.format(page_name)
    if is_group:
        db_path = 'group_' + db_path
        images_path = 'group_' + images_path

    # Find out if first write or not
    if os.path.exists(db_path):
        write_kwargs = {'mode': 'a', 'index': False, 'header': False}
    else:
        write_kwargs = {'index': False}

    # enable_logging()

    if not os.path.exists(images_path):
        os.mkdir(images_path)
    # You can set "start_url=<>" to the page url you wish to start from.
    print(f'Writing to file {db_path}')
    get_kwargs = {'page_limit': 200000000, 'extra_info': True}#, 'cookies': COOKIE_FILE}
    get_kwargs['start_url'] = 'https://m.facebook.com/groups/823580191927059?bac=MTY2MDMzOTA5OToxMTU1MTcwNjMyMTAxMzQ1OjExNTUxNzA2MzIxMDEzNDUsMCwyODoyMDpLdz09&multi_permalinks'
    if is_group:
        get_kwargs['group'] = page_name
    else:
        get_kwargs['account'] = page_name
    for i, post in enumerate(
            get_posts(**get_kwargs)):
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
            download_images(post, images_path)

        print('Saving post! %d' % i)
        print(post_dict)
        df = pd.json_normalize([post_dict])
        df.to_csv(db_path, **write_kwargs)
        write_kwargs = {'mode': 'a', 'index': False, 'header': False}


if __name__ == '__main__':
    main()
