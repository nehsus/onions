import json
import logging
import time

import requests
from bs4 import BeautifulSoup

from constant import INVALID_URL


# an appeal for soup
def appeal(url: str, k=0):
    x = 0
    retry_count = 3  # maximum tries
    soup = ''

    while retry_count > 0:

        try:
            time.sleep(0.01)
            r = requests.get(url, verify=True)
            if r.url == INVALID_URL:
                logging.error("ERR 404" + url)
                break
            soup = BeautifulSoup(r.content, "html.parser")
            if k != 0:
                soup = json.loads(r.content)
            x += 1
            retry_count = 0  # yay!

        except ConnectionResetError as ex:
            if retry_count <= 0:
                print("Failed::: " + url + "\t" + str(ex))
            else:
                retry_count -= 1
            time.sleep(0.5)

    return soup


def read_file(name: str):
    f = open(name, "r")
    words = f.read().splitlines()
    f.close()
    return words
