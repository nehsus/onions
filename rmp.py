import json
import math

import requests
from constant import *


# Get bucket size for current page
def get_size(uid):
    page = requests.get(RMP_PAGE + str(1) + RMP_QUERY + str(uid))
    json_data = json.loads(page.content)
    size = json_data['remaining'] + 20
    return size


# RateMyProfessor init
class RmP:
    def __init__(self, uid):
        self.uid = uid
        self.list = self.create_list()

    def create_list(self):

        data = []
        size = get_size(self.uid)
        pages = math.ceil(size / 20)

        for i in range(1, pages):
            page = requests.get(RMP_PAGE + str(i) + RMP_QUERY + str(self.uid))
            json_data = json.loads(page.content)
            p_list = json_data['professors']
            for item in p_list:
                data.append(item)

        return data
