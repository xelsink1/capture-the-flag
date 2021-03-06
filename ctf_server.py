from datetime import datetime
import random
import string

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

from config import *
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager

from generator import map_generator

app = Flask(__name__, instance_path="/home/dmitry/PycharmProjects/capture-the-flag/instance")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(100))
#     username = db.Column(db.String(50), nullable=False, unique=True)
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     password_hash = db.Column(db.String(100), nullable=False)
#     created_on = db.Column(db.DateTime(), default=datetime.utcnow)
#     updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
#     app = Flask(__name__)
#     app.debug = True
#     app.config['SECRET_KEY'] = 'a really really really really long secret key'
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@localhost/flask_app_db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
#     app.config['MAIL_PORT'] = 587
#     app.config['MAIL_USE_TLS'] = True
#     app.config['MAIL_USERNAME'] = 'youmail@gmail.com'
#     app.config['MAIL_DEFAULT_SENDER'] = 'youmail@gmail.com'
#     app.config['MAIL_PASSWORD'] = 'password'
#
#     '''manager = Manager(app)
#     manager.add_command('db', MigrateCommand)
#     db = SQLAlchemy(app)
#     migrate = Migrate(app, db)e
#     mail = Mail(app)
#     login_manager = LoginManager(app)
# '''

    # def __repr__(self):
    #     return "<{}:{}>".format(self.id, self.username)
    #
    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)
    #
    # def as_dict(self):
    #     return {
    #         "id": self.id,
    #         "username": self.username
    #     }


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(32), unique=True, nullable=True)
    code = db.Column(db.Text, nullable=True)
    hp = db.Column(db.Integer, nullable=False, default=3)
    bullets = db.Column(db.Integer, nullable=False, default=9999)
    has_flag = db.Column(db.Boolean, nullable=False, default=False)
    x = db.Column(db.Integer, nullable=True, default=0)
    y = db.Column(db.Integer, nullable=True, default=0)
    side = db.Column(db.String(6), default="up")
    inventory = db.Column(db.JSON, nullable=True)
    base_id = db.Column(db.Integer, db.ForeignKey('base.id'), nullable=True)
    base = db.relationship('Base', backref=db.backref('players', lazy=True))

    def as_dict(self):
        return {
            "id": self.id,
            "code": self.code,
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

    def as_dict(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "side": self.side,
            "speed": self.speed
        }


@app.route('/game')
def index():
    return render_template("game.html")


@app.route('/test/init_map')
def init_map():
    Base.query.delete()
    Object.query.delete()
    Player.query.delete()
    Bullet.query.delete()
    m = map_generator(32, 32)
    print(m)
    for i in range(len(m)):
        print(m[i])
        for j in range(len(m[i])):
            if m[i][j] == ".":
                continue
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
    return render_template("map_generation.html")


# def add_code(player_id):
#     players = Player.querry.all()
#     player = players[player_id]
#     code = player.as_dict(key="code")
#     code = code[0].decode('utf8').replace('exit()', '')
#     output_file = open("./bots/" + player + ".py", 'w')
#     output_file.write(code)
#     output_file.close()
#     try:
#         module = __import__(player, fromlist=["make_choice"])
#         module = imp.reload(module)
#         makeChoice = getattr(module, "make_choice")


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


def add_base(x, y, color):
    new_base = Base()
    new_base.x = x
    new_base.y = y
    new_base.color = color
    db.session.add(new_base)
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        init_map()

        codes = []

        codes.append(request.form.get('code1'))
        codes.append(request.form.get('code2'))
        codes.append(request.form.get('code3'))
        codes.append(request.form.get('code4'))
        bases = Base.query.all()

        for base in bases:
            new_player = Player()
            new_player.base = base
            new_player.key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            new_player.code = codes.pop()
            new_player.bullets = 9999
            new_player.x = base.x
            new_player.y = base.y
            db.session.add(new_player)
        db.session.commit()
        return redirect('/game')
    return render_template("bots.html")

@app.route('/test/add_player')
def web_add_player():
    bases = Base.query.all()
    Player.query.delete()

    for base in bases:
            add_player(base.id, open('examples/example_bot.py').read())

    return "ok"


def add_player(base_id, code):
    bases = Base.query.all()
    new_player = Player()
    new_player.base = bases[base_id]
    new_player.key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    new_player.code = code
    new_player.bullets = 9999
    new_player.x = bases[base_id].x
    new_player.y = bases[base_id].y
    db.session.add(new_player)
    db.session.commit()


def move_player(player_id, x, y):
    players = Player.querry.all()
    player = players[player_id]
    player.x = x
    player.y = y
    db.session.commit()


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def get_state():
    # users = list(User.query.all())
    players = list(Player.query.all())
    objects = list(Object.query.all())
    bases = list(Base.query.all())
    bullets = list(Bullet.query.all())

    return {
        # "users": [user.as_dict() for user in users],
        "players": [player.as_dict() for player in players],
        "objects": [object1.as_dict() for object1 in objects],
        "bases": [base.as_dict() for base in bases],
        "bullets": [bullet.as_dict() for bullet in bullets],
        "width": 32,
        "height": 32,
        "game": "running"
    }


@app.route('/api/state')
def web_get_state():
    return jsonify(get_state())


if __name__ == "__main__":
    app.run(HOST, PORT, debug=DEBUG)
