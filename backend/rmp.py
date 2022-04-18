import math

from constant import *
from util import appeal


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
            url = RMP_PAGE + str(i) + RMP_QUERY + str(self.uid)
            page = appeal(url, 1)
            p_list = page['professors']

            for item in p_list:
                data.append(item)

        return data


def get_size(uid):
    url = RMP_PAGE + str(1) + RMP_QUERY + str(uid)
    page = appeal(url, 1)
    size = page['remaining'] + 20
    return size
