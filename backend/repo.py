import logging

from flask import jsonify

import analysis
import preprocessing
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
    top_list = read_file('/Users/nehsus/Documents/acrux2.nosync/onions/backend/top_universities.txt')
    top_objects = list(University.objects(title__in=top_list))

    prof_list = worker.insert_professor_worker_pool(top_objects[300:])

    err = Professor.objects.insert(prof_list, load_bulk=False)

    if err is None:
        logging.error(err)
        return jsonify({'status': 1, 'data': None})

    logging.info("done!")

    return jsonify({
        'status': 0,
        'data': err
    })


def analyze_professor(pid: int):
    comments = Professor.comments(pid=str(pid))
    return analysis.analyze_comments(comments)


def get_universities():
    logging.info("__init__get_universities()")
    top_list = read_file('/Users/nehsus/Documents/acrux2.nosync/onions/backend/top_universities.txt')
    top_objects = list(University.objects(title__in=top_list))
    return jsonify({
        'status': 1,
        'data': top_objects
    })


def get_professors(uid: int):
    logging.info("__init__get_professors()")
    obj_id = University.objects(uid=uid).first().pk
    print(obj_id)
    professors = list(Professor.objects(university=obj_id))
    return jsonify({
        'status': 1,
        'data': professors
    })


def get_all_scores(pid: int):
    professor = Professor.objects(pid=pid).first()
    v_score = preprocessing.get_happiness_score_professor(professor)
    b_score = preprocessing.get_happiness_score_professor_distillbert(professor)
    r_score = preprocessing.get_happiness_score_professor_fastrnn(professor)
    rmp_score = Professor.objects(pid=pid).first().overall_rating

    return jsonify({
        'status': 1,
        'data': {
            'vader': v_score,
            'bert': b_score,
            'rnn': r_score,
            'rmp': rmp_score
        }
    })


def get_comments(pid: int):
    logging.info("__init__get_comments()")
    comments = list(Professor.objects(pid=pid).first().comments)
    best_comments = preprocessing.get_best_comments(comments)
    return jsonify({
        'status': 1,
        'data': best_comments
    })


def get_happiness_score_professor(pid: int):
    professor = Professor.objects(pid=pid).first()
    score = preprocessing.get_happiness_score_professor_distillbert(professor)
    return jsonify({
        'status': 1,
        'data': score
    })


def get_happiness_score_university(uid: int):
    logging.info("__init__get_professors()")
    obj_id = University.objects(uid=uid).first().pk
    print(obj_id)
    professors = list(Professor.objects(university=obj_id))
    score = preprocessing.get_happiness_score_university(professors)
    return jsonify({
        'status': 1,
        'data': score
    })
