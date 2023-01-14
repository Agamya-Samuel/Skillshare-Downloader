from bot import SKILLSHARE_COOKIE

import requests, sys, re, os
import cloudscraper
from slugify import slugify

cookie = SKILLSHARE_COOKIE
download_path = os.environ.get('FILE_PATH', './Skillshare')
pk = 'BCpkADawqM2OOcM6njnM7hf9EaK6lIFlqiXB0iWjqGWUQjU7R8965xUvIQNqdQbnDTLz0IAO7E6Ir2rIbXJtFdzrGtitoee0n1XXRliD-RH9A-svuvNW9qgo3Bh34HEZjXjG4Nml4iyz3KqF'
brightcove_account_id = 3695997568001


url = None
course_id = None
title = None
file_name = None
size = None
anonfile_url = None
pixeldrain_url = None
# gofile_url = None
# gofile_folder_url = None

def beautify_str(string) -> str:
    new_list = []
    list = slugify(string).split('-')
    for l in list:
        l.capitalize()
        new_list.append(l)
    return " ".join(new_list)

def is_unicode_string(string):
    if isinstance(string, str):
        return True

    else:
        return False

def download_video(fpath, video_id):
    meta_url = 'https://edge.api.brightcove.com/playback/v1/accounts/{account_id}/videos/{video_id}'.format(
        account_id=brightcove_account_id,
        video_id=video_id,
    )

    scraper = cloudscraper.create_scraper(
        browser={
            'custom': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3',
        },
        delay=10
    )

    meta_res = scraper.get(
        meta_url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'Accept': 'application/json;pk={}'.format(pk),
            'Origin': 'https://www.skillshare.com'
        }
    )

    if meta_res.status_code != 200:
        raise Exception('Failed to fetch video meta')

    if meta_res.json()['sources'][6]['container'] == 'MP4' and 'src' in meta_res.json()['sources'][6]:
        dl_url = meta_res.json()['sources'][6]['src']
        # break
    else:
        dl_url = meta_res.json()['sources'][1]['src']

    print('Downloading {}...'.format(fpath))

    if os.path.exists(fpath):
        print('Video already downloaded, skipping...')
        return

    with open(fpath, 'wb') as f:
        response = requests.get(dl_url, allow_redirects=True, stream=True)
        total_length = response.headers.get('content-length')

        if not total_length:
            f.write(response.content)

        else:
            dl = 0
            total_length = int(total_length)

            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                sys.stdout.flush()

        print('')
    
        # sleep_time = 120
        # print("Sleeping for - {sleep_time} seconds".format(sleep_time=sleep_time))
        # sleep(sleep_time)

def fetch_course_data_by_class_id(course_id):
    url = 'https://api.skillshare.com/classes/{}'.format(course_id)
    scraper = cloudscraper.create_scraper(
        browser={
            'custom': 'Skillshare/4.1.1; Android 5.1.1',
        },
        delay=10
    )

    res = scraper.get(
        url,
        headers={
        'Accept': 'application/vnd.skillshare.class+json;,version=0.8',
        'User-Agent': 'Skillshare/5.3.0; Android 9.0.1',
        'Host': 'api.skillshare.com',
        'Referer': 'https://www.skillshare.com/',
        'cookie': cookie
        }
    )

    if not res.status_code == 200:
        raise Exception('Fetch error, code == {}'.format(res.status_code))

    return res.json()

def download_course_by_class_id(course_id):
    data = fetch_course_data_by_class_id(course_id=course_id)
    teacher_name = None

    if 'vanity_username' in data['_embedded']['teacher']:
        teacher_name = data['_embedded']['teacher']['vanity_username']

    if not teacher_name:
        teacher_name = data['_embedded']['teacher']['full_name']

    if not teacher_name:
        raise Exception('Failed to read teacher name from data')

    if is_unicode_string(teacher_name):
        teacher_name = teacher_name.encode('ascii', 'replace')

    title = slugify(data['title'])

    if is_unicode_string(title):
        title = title.encode('ascii', 'replace')  # ignore any weird char

    base_path = os.path.abspath(
        os.path.join(
            download_path,
            slugify(teacher_name),
            slugify(title),
        )
    ).rstrip('/')

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    for s in data['_embedded']['sessions']['_embedded']['sessions']:
        video_id = None
        if 'video_hashed_id' in s and s['video_hashed_id']:
            video_id = s['video_hashed_id'].split(':')[1]

        if not video_id:
            raise Exception('Failed to read video ID from data')

        s_title = s['title']

        if is_unicode_string(s_title):
            s_title = s_title.encode('ascii', 'replace')

        file_name = '{} - {}'.format(
            str(s['index'] + 1).zfill(2),
            slugify(s_title),
        )

        download_video(
            fpath='{base_path}/{session}.mp4'.format(
                base_path=base_path,
                session=file_name,
            ),
            video_id=video_id,
        )

        print('')
    base_path = os.path.abspath(
        os.path.join(
            download_path
        )
    ).rstrip('/')
    
    return base_path, slugify(title), slugify(teacher_name)

def get_course_id(url):
    m = re.match(r'https://www.skillshare.com/classes/.*?/(\d+)', url)
    if m is None:
        m = re.match(r'https://www.skillshare.com/[a-zA-Z]+/classes/.*?/(\d+)', url)

    if m is None:
        raise Exception('Failed to parse class ID from URL')

    course_id = m.group(1)
    return int(course_id)