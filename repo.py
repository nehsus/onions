import logging

import worker
from model import University, Professor


def add_university():
    uni_list = worker.insert_university_worker()

    _, err = University.objects.insert(uni_list)
    if err is not None:
        logging.error(err)

    return {"status": err}


def add_professor():
    prof_list = worker.insert_professor_worker(list(University.objects))

    _, err = Professor.objects.insert(prof_list)
    if err is not None:
        logging.error(err)

    return {"status": err}


def update_comments():
    comments = worker.insert_professor_worker(list(Professor.objects))

    _, err = Professor.objects.insert()
    if err is not None:
        logging.error(err)

    return {"status": err}
