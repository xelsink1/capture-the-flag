from flask import Flask, jsonify
from config import *

app = Flask(__name__)


@app.route('/')
def index():
    return "Here I am!"


@app.route('/api/map')
def get_map():
    M = [
        [0, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 0],
    ]

    return jsonify(M)


app.run(HOST, PORT, debug=DEBUG)
