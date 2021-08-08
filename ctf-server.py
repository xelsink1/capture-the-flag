import random
import string

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import *
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
'''
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)

    def __repr__(self):
	    return "<{}:{}>".format(self.id, self.username)
'''
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
    return "Here I am!"


@app.route('/test/add_base')
def add_base():
    new_base = Base()
    new_base.x = 0
    new_base.y = 5
    new_base.color = "#FFFFFF"

    db.session.add(new_base)
    db.session.commit()

    return "created base"


@app.route('/test/add_player')
def add_player():
    bases = Base.query.all()

    new_player = Player()
    new_player.base = bases[0]
    new_player.key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    new_player.x = bases[0].x
    new_player.y = bases[0].y

    db.session.add(new_player)
    db.session.commit()

    return "added_player"


@app.route('/api/state')
def get_state():
    players = list(Player.query.all())
    objects = list(Object.query.all())
    bases = list(Base.query.all())
    bullets = list(Bullet.query.all())

    return jsonify({
        "players": [player.as_dict() for player in players],
        "objects": [object1.as_dict() for object1 in objects],
        "bases": [base.as_dict() for base in bases],
        "bullets": [bullet.as_dict() for bullet in bullets],
        "width": 32,
        "heigth": 32
    })


app.run(HOST, PORT, debug=DEBUG)
