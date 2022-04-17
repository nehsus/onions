from flask import Flask
import time
import requests
import re
import os
import rmp
import logging

from model import *
from constant import *

from bs4 import BeautifulSoup
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv

# load environment
load_dotenv()

app = Flask(__name__,
            static_folder=os.getenv('STATIC_FOLDER'),
            template_folder=os.getenv('TEMPLATE_FOLDER'))

app.config['MONGODB_SETTINGS'] = {'host': os.getenv('MONGODB_URI')}

db = MongoEngine()
db.init_app(app)


@app.route('/')
def home():
    logging.info("/---" + str(time.time()))
    # headers = {"Accept": "*/*",
    #            "User-Agent": "PostmanRuntime/7.29.0",
    #            "Accept-Encoding": "gzip, deflate, br",
    #           "Connection": "keep-alive"}

    uni_list = []

    soup = ''
    # Start time
    start = time.time()

    # Number of batches of universities
    batch = 1

    # Batch size
    batch_size = 2000

    while batch <= 5:

        i = 1 if batch == 1 else ((batch * batch_size) + 1)

        while i < batch_size:

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
                        time.sleep(0.33)

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
            logging.warning("U--\r{0}".format((float(i) / (batch * batch_size) * 100)))
            # logging.warning("Success: " + str(i))
            uni_list.append(university)

            i += 1

        batch -= 1

    # Insert universities' list
    University.objects.insert(uni_list)

    # Log time taken to insert
    finish = time.time()
    logging.warning("Universities' inserted--time taken--" + str(start - finish))

    prof_list = []

    i = 1
    start = time.time()
    for uni in uni_list:

        uni_rmp = rmp.RmP(uni.uid)

        temp_list = uni_rmp.list

        # Log Status
        logging.warning("P--\r{0}".format((float(i) / 6050) * 100))

        for j in temp_list:
            professor = Professor(
                name=j['tFname'] + " " + j['tLname'],
                pid=j['tid'],
                dept=j['tDept'],
                no_ratings=j['tNumRatings'] or 0,
                rating_class=j['rating_class'],
                overall_rating=str(j['overall_rating']),
                # TODO: Scrape Comments Concurrently
                comments=None,
                university=uni,
            )

            prof_list.append(professor)
            # professor.save()

        i += 1

    Professor.objects.insert(prof_list)
    finish = time.time()
    logging.warning("Professors' inserted--time taken--" + str(start - finish))

    size = len(prof_list)
    i = 1
    for p in prof_list:

        logging.warning("C--\r{0}".format((float(i) / size) * 100))
        url = RMP_PROF + str(p.pid)
        # TODO: Handle ConnectionReset Error
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find_all('div', attrs={'class': 'Rating__RatingBody-sc-1rhvpxz-0 dGrvXb'})

        comments = []

        for k in table:
            comments.append(k.select(
                'div[class="Comments__StyledComments-dzzyvm-0 gRjWel"]')[0].get_text(strip=True))

        Professor.objects(pid=p.pid).update(comments=comments)
        i += 1

    print("Updated!")

    return {
        'status': 'success!'
    }


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(5001), debug=True)
