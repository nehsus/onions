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


@app.route('/api/add/university/all')
def add_university():
    return repo.add_university()


@app.route('/api/add/professor/all')
def add_professor():
    return repo.add_professor()


@app.route('/api/update/comments/all')
def update_comments():
    return repo.update_comments()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(5001), debug=True, use_reloader=False)
