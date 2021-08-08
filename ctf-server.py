from flask import Flask
from config import *

app = Flask(__name__)

@app.route('/')
def index():
    return "Here I am!"

app.run(HOST, PORT, debug=DEBUG)