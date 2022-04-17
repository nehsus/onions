import re
import time

import logging

import requests
from bs4 import BeautifulSoup

import rmp
from constant import RMP_UNI, INVALID_URL, RMP_PROF
from model import University, Professor


def insert_university_worker():
    uni_list = []

    soup = ''
    # Start time
    start = time.time()

    # Number of batches of universities
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

            try:
                url = RMP_UNI + str(i)
                title = ''
                x = 0
                retry_count = 2  # maximum tries
                while retry_count > 0:
                    try:
                        r = requests.get(url)
                        if r.url == INVALID_URL:
                            logging.error("ERR not found: " + RMP_UNI + str(i))
                            break
                        soup = BeautifulSoup(r.content, 'html.parser')
                        x += 1
                        retry_count = 0

                    # Too many ConnectionReset Errors, retry with t.sleep(0.33)
                    except ConnectionResetError as ex:
                        if retry_count <= 0:
                            print("Failed::: " + url + "\t" + str(ex))
                        else:
                            retry_count -= 1
                        time.sleep(0.5)

                    title = soup.find_all('div', {'class': 'result-text'})[0].getText()
                    if not title:
                        raise IndexError

            except IndexError:
                logging.warning("ERR No Name found: " + str(i))
                continue

            title = re.sub('\r+\n+\t+', '', title)

            # Write University document to DB
            university = University(title=title, uid=i)
            # university.save()

            # Log Status
            logging.warning("*Bch*-" + str(batch)
                            + "--" + "\t{0}".format((float(i % (1000 * batch)) / 2000 * 100)))
            # logging.warning("Success: " + str(i))
            uni_list.append(university)

            i += 1

        batch += 1

    # Log time taken to insert
    finish = time.time()
    logging.warning("Universities' inserted--time taken--" + str(start - finish))

    return uni_list


def insert_professor_worker(uni_list: list[University]):
    prof_list = []

    # process start time
    start = time.time()

    # size = len(uni_list)

    size = 50

    for i in range(size):

        uni_id = uni_list[i].uid
        uni_rmp = rmp.RmP(uni_id)

        temp_list = uni_rmp.list

        # Log Status
        logging.warning("added--" + str(uni_id) + "--" + "--"
                        + "\t{0}".format((float(i) / size) * 100))

        s2 = len(temp_list)
        for j in temp_list:

            idx = temp_list.index(j)
            professor = Professor(
                name=j['tFname'] + " " + j['tLname'],
                pid=j['tid'],
                dept=j['tDept'],
                no_ratings=j['tNumRatings'] or 0,
                rating_class=j['rating_class'],
                overall_rating=str(j['overall_rating']),
                # TODO: Scrape Comments Concurrently
                comments=None,
                university=uni_list[i],
            )

            logging.warning("\tprof---" + str(uni_id) + "--" + professor.name + "--"
                            + "\t{0}".format((float(idx) / s2) * 100))

            prof_list.append(professor)

    # process end time
    finish = time.time()
    logging.warning("Professors' process--time taken--" + str(start - finish))

    return prof_list


def insert_comments_worker(pid: int):
    url = RMP_PROF + str(pid)
    # TODO: Handle ConnectionReset Error
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find_all('div', attrs={'class': 'Rating__RatingBody-sc-1rhvpxz-0 dGrvXb'})

    comments = []

    size = len(table)
    for k in range(size):
        logging.warning("*PID*-" + str(pid) + "--\t{0}".format((float(k) / size) * 100))
        comments.append(table[k].select(
            'div[class="Comments__StyledComments-dzzyvm-0 gRjWel"]')[0].get_text(strip=True))

    return comments
    # Professor.objects(pid=p.pid).update(comments=comments)
    # i += 1
