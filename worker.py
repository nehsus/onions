import logging
import re
import time

import rmp
from constant import RMP_UNI, RMP_PROF
from model import University, Professor
from util import appeal


def insert_university_worker():
    uni_list = []

    # Start time
    start = time.time()

    # university batches
    batch = 1

    # Batch size
    batch_inc = 2000

    batch_size = 2000

    while batch <= 5:

        if batch == 1:
            i = 1
        else:
            i = (batch_size + 1)
            batch_size += batch_inc

        while i <= batch_size:

            url = RMP_UNI + str(i)
            soup = appeal(url)
            title = ''

            if soup is not '':
                try:
                    title = soup.find_all('div', {'class': 'result-text'})[0].getText()
                    if not title:
                        raise IndexError

                except IndexError:
                    logging.warning("ERR name not found. " + str(i))
                    continue

            title = re.sub('\r+\n+\t+', '', title)

            # Write University document to DB
            university = University(title=title, uid=i)

            # Log Status
            logging.warning("*B*-" + str(batch)
                            + "--" + "\t{0}".format((float(i % (1000 * batch)) / 2000 * 100)))
            uni_list.append(university)

            i += 1

        batch += 1

    # Log time taken to process
    finish = time.time()
    logging.warning("Universities' process--time taken--" + str(start - finish))

    return uni_list


def insert_professor_worker_pool(uni_list: list[University]):
    # process start time
    start = time.time()

    prof_list = []
    size = len(uni_list)

    for item in uni_list:
        idx = uni_list.index(item)

        uid = item.uid
        uni_rmp = rmp.RmP(uid)

        temp_list = uni_rmp.list

        s2 = len(temp_list)
        for i in range(s2):
            j = temp_list[i]

            if j['tDept'] != 'Computer Science':
                continue

            professor = Professor(
                name=j['tFname'] + " " + j['tLname'],
                pid=j['tid'],
                dept=j['tDept'],
                no_ratings=j['tNumRatings'] or 0,
                rating_class=j['rating_class'],
                overall_rating=str(j['overall_rating']),
                # TODO: Scrape Comments Concurrently
                comments=insert_comments_worker(j['tid'], item.title),
                university=item,
            )

            logging.warning("\tAdded---" + str(professor.university.title) + "--" + professor.name + "--"
                            + "\t{0}".format((float(idx) / size) * 100))

            prof_list.append(professor)

    # process end time
    finish = time.time()
    logging.warning("\tdone! size:" + str(len(prof_list)) + ", time: " + str(finish - start))

    return prof_list


def insert_comments_worker(pid: int, title: str):
    logging.warning("\tUpdating--" + title + "--Professor--" + str(pid))

    # process start time
    start = time.time()

    comments = []
    url = RMP_PROF + str(pid)

    soup = appeal(url)
    if soup is not '':

        table = soup.find_all('div', attrs={'class': 'Rating__RatingBody-sc-1rhvpxz-0 dGrvXb'})
        for item in table:
            comments.append(
                item.select('div[class="Comments__StyledComments-dzzyvm-0 gRjWel"]')[0].get_text(strip=True)
            )

    # process end time
    finish = time.time()
    logging.warning("\tdone! " + str(pid) + ", time: " + str(finish - start))

    return comments
