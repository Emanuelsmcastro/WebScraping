import os
import time
import sys
import requests

POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split())
BASE_URL = 'https://www.fluentpython.com/data/flags/'
DES_DIR = 'Downloads/'


def save_flag(img, filename):
    path = os.path.join(DES_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def get_flag(cc):
    url = f'{BASE_URL}/{cc.lower()}/{cc.lower()}.gif'
    resp = requests.get(url)
    return resp.content


def show(text):
    print(text, end=' ')
    sys.stdout.flush()


def download_many(cc_list):
    for cc in sorted(cc_list):
        image = get_flag(cc)
        show(cc)
        save_flag(image, cc.lower() + '.gif')
    return len(cc_list)


def main(down_many):
    t0 = time.time()
    count = down_many(POP20_CC)
    elapsed = time.time() - t0
    msg = f'\n{count} flags downloaded in {elapsed}'
    print(msg)


if __name__ == '__main__':
    main(download_many)
