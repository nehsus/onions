import os
import time

from dotenv import load_dotenv
from flask import Flask
from flask_mongoengine import MongoEngine

import repo

# load environment
load_dotenv()

app = Flask(__name__,
            static_folder=os.getenv('STATIC_FOLDER'),
            template_folder=os.getenv('TEMPLATE_FOLDER'))

app.config['MONGODB_SETTINGS'] = {'host': os.getenv('MONGODB_URI')}

db = MongoEngine()
db.init_app(app)


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@app.route('/api/get/universities/all')
def get_universities():
    return repo.get_universities()


@app.route('/api/get/professors/<uid>')
def get_professors(uid: str):
    return repo.get_professors(int(uid))


@app.route('/api/get/comments/<pid>')
def get_comments(pid: str):
    return repo.get_comments(int(pid))


@app.route('/api/get/scores/<pid>')
def get_scores(pid: int):
    return repo.get_all_scores(pid)

@app.route('/api/add/university/all')
def add_university():
    return repo.add_university()


@app.route('/api/add/professor/all')
def add_professor():
    return repo.add_professor()


@app.route('/api/score/professor/<pid>')
def score_professor(pid: int):
    return repo.get_happiness_score_professor(pid)


@app.route('/api/score/university/<uid>')
def score_university(uid: int):
    return repo.get_happiness_score_university(uid)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(5001), debug=True, use_reloader=True)
