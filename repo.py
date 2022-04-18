import logging

from flask import jsonify

import worker
from model import University, Professor
from util import read_file


def add_university():
    logging.info("__init__add_university()")
    uni_list = worker.insert_university_worker()

    err = University.objects.insert(uni_list)
    if err is None:
        logging.error(err)
        return jsonify({'status': 1, 'data': None})

    return jsonify({
        'status': 0,
        'data': err
    })


def add_professor():
    logging.info("__init__add_professor()")
    top_list = read_file('./top_universities.txt')
    top_objects = list(University.objects(title__in=top_list))

    prof_list = worker.insert_professor_worker_pool(top_objects[100:300])

    err = Professor.objects.insert(prof_list, load_bulk=False)

    if err is None:
        logging.error(err)
        return jsonify({'status': 1, 'data': None})

    logging.info("done!")

    return jsonify({
        'status': 0,
        'data': err
    })

