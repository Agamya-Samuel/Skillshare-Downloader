from bot import ANONFILE_TOKEN

import json
import requests
from slugify import slugify
from anonfile import AnonFile


def upload_anonfiles(fpath):
    anon = AnonFile(token=ANONFILE_TOKEN)
    # upload a file and enable progressbar terminal feedback
    print(f'Uploading to Anonfiles.com ...')
    upload = anon.upload(fpath, progressbar=True)
    print(f'Uploaded to Anonfiles.com successfully.')
    return str(upload.url.geturl())


def upload_pixeldrain(fpath):
    print(f'Uploading to Pixeldrain.com ...')
    with open(fpath, 'rb') as fileb:
        req = requests.post('https://pixeldrain.com/api/file',
        data={'anonymous': 'False'},
        files={"file": fileb}
        )
    print(f'Uploaded to Pixeldrain.com successfully.')
    resp = req.text
    resp = json.loads(resp.replace('\n', ''))['id']
    return resp
    

def upload_gofile():
    pass

def upload_file(fpath):
    print(f'Uploading...')
    anon_url = upload_anonfiles(fpath=fpath)
    pd_url = 'https://pixeldrain.com/u/' + upload_pixeldrain(fpath=fpath)
    print(f'Uploaded successfully.')
    return anon_url, pd_url