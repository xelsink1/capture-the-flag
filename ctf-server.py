import datetime
import random
import string

from flask import Flask, jsonify, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from config import *
from flask_migrate import Migrate

app = Flask(__name__, instance_path="/home/dmitry/PycharmProjects/capture-the-flag/instance")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


'''class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)'''


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(32), unique=True, nullable=True)
    code = db.Column(db.Text, nullable=True)
    hp = db.Column(db.Integer, nullable=False, default=3)
    bullets = db.Column(db.Integer, nullable=False, default=0)
    has_flag = db.Column(db.Boolean, nullable=False, default=False)
    x = db.Column(db.Integer, nullable=True, default=0)
    y = db.Column(db.Integer, nullable=True, default=0)
    side = db.Column(db.String(6), default="up")
    inventory = db.Column(db.JSON, nullable=True)
    base_id = db.Column(db.Integer, db.ForeignKey('base.id'),
                        nullable=True)
    base = db.relationship('Base', backref=db.backref('players', lazy=True))

    def as_dict(self):
        return {
            "id": self.id,
            "hp": self.hp,
            "bullets": self.bullets,
            "has_flag": self.has_flag,
            "x": self.x,
            "y": self.y,
            "side": self.side,
            "base": self.base.as_dict()
        }


class Base(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=True, default=0)
    y = db.Column(db.Integer, nullable=True, default=0)
    color = db.Column(db.String(8), default="#FF0000")

    def as_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "color": self.color,
            "id": self.id
        }


class Object(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), default="ground")
    hp = db.Column(db.Integer, nullable=False, default=0)
    x = db.Column(db.Integer, nullable=True, default=0)
    y = db.Column(db.Integer, nullable=True, default=0)

    def as_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "hp": self.hp,
            "x": self.x,
            "y": self.y
        }


class Bullet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=True, default=0)
    y = db.Column(db.Integer, nullable=True, default=0)
    side = db.Column(db.String(6), default="up")
    speed = db.Column(db.Integer, nullable=False, default=2)
    type = db.Column(db.String(10), default="ground")

    def as_dict(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "side": self.side,
            "speed": self.side,
            "type": self.type,
        }


@app.route('/')
def index():
    return render_template("game.html")


@app.route('/test/init_map')
def init_map():
    Base.query.delete()
    Object.query.delete()
    Player.query.delete()
    Bullet.query.delete()

    with open('maps/map1.txt') as map_file:
        m = map_file.read().split('\n')
    for i in range(len(m)):
        for j in range(len(m[i].split(' '))):
            if m[i][j] == ".":
                add_object("ground", i, j)
            elif m[i][j] == "#":
                add_object("wall", i, j)
            elif m[i][j] == "F":
                add_object("flag", i, j)
            elif m[i][j] == "H":
                add_object("medkit", i, j)
            elif m[i][j] == "A":
                add_object("ammo", i, j)
            elif m[i][j] == "B":
                add_base(i, j, random.choice(["#00FF00", "#FF0000", "#0000FF", "#FFFF00"]))
            else:
                abort(400)
        return "heh"
    # str -> db


def add_object(hype, x, y):
    new_object = Object()
    new_object.type = hype
    if hype == "wall":
        new_object.hp = 3
    else:
        new_object.hp = 0
    new_object.x = x
    new_object.y = y
    db.session.add(new_object)
    db.session.commit()


# @app.route('/test/add_base')
def add_base(x, y, color):
    new_base = Base()
    new_base.x = x
    new_base.y = y
    new_base.color = color
    db.session.add(new_base)
    db.session.commit()


# @app.route('/test/add_player')
def add_player(base_id):
    bases = Base.query.all()
    new_player = Player()
    new_player.base = bases[base_id]
    new_player.key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    new_player.x = bases[base_id].x
    new_player.y = bases[base_id].y
    db.session.add(new_player)
    db.session.commit()


# def move_player(player_id, x, y):
#
@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/api/state')
def get_state():
    # users = list(User.query.all())
    players = list(Player.query.all())
    objects = list(Object.query.all())
    bases = list(Base.query.all())
    bullets = list(Bullet.query.all())

    return jsonify({
        # "users": [user.as_dict() for user in users],
        "players": [player.as_dict() for player in players],
        "objects": [object1.as_dict() for object1 in objects],
        "bases": [base.as_dict() for base in bases],
        "bullets": [bullet.as_dict() for bullet in bullets],
        "width": 32,
        "heigth": 32
    })


app.run(HOST, PORT, debug=DEBUG)
