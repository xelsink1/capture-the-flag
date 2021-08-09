from datetime import datetime
import random
import string

from flask import Flask, jsonify, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from config import *
from flask_migrate import Migrate
from colorama import init

app = Flask(__name__, instance_path="/home/dmitry/PycharmProjects/capture-the-flag/instance")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username
        }

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)


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


def map_generator(height, width):
    def printMaze(maze):
        maze[height // 2][width // 2] = 'F'
        maze[0][width - 1] = maze[0][0] = maze[height - 1][0] = maze[height - 1][width - 1] = 'B'

    def surroundingCells(rand_wall):
        s_cells = 0
        if (maze[rand_wall[0] - 1][rand_wall[1]] == '.'):
            s_cells += 1
        if (maze[rand_wall[0] + 1][rand_wall[1]] == '.'):
            s_cells += 1
        if (maze[rand_wall[0]][rand_wall[1] - 1] == '.'):
            s_cells += 1
        if (maze[rand_wall[0]][rand_wall[1] + 1] == '.'):
            s_cells += 1

        return s_cells

    cell = '.'
    unvisited = '2'
    maze = []

    init()

    for i in range(0, height):
        line = []
        for j in range(0, width):
            line.append(unvisited)
        maze.append(line)

    starting_height = int(random.random() * height)
    starting_width = int(random.random() * width)
    if (starting_height == 0):
        starting_height += 1
    if (starting_height == height - 1):
        starting_height -= 1
    if (starting_width == 0):
        starting_width += 1
    if (starting_width == width - 1):
        starting_width -= 1

    maze[starting_height][starting_width] = cell
    walls = []
    walls.append([starting_height - 1, starting_width])
    walls.append([starting_height, starting_width - 1])
    walls.append([starting_height, starting_width + 1])
    walls.append([starting_height + 1, starting_width])

    maze[starting_height - 1][starting_width] = '#'
    maze[starting_height][starting_width - 1] = '#'
    maze[starting_height][starting_width + 1] = '#'
    maze[starting_height + 1][starting_width] = '#'

    while (walls):

        rand_wall = walls[int(random.random() * len(walls)) - 1]

        if (rand_wall[1] != 0):
            if (maze[rand_wall[0]][rand_wall[1] - 1] == '2' and maze[rand_wall[0]][rand_wall[1] + 1] == '.'):

                s_cells = surroundingCells(rand_wall)

                if (s_cells < 2):
                    maze[rand_wall[0]][rand_wall[1]] = '.'

                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0] - 1][rand_wall[1]] != '.'):
                            maze[rand_wall[0] - 1][rand_wall[1]] = '#'
                        if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                    if (rand_wall[0] != height - 1):
                        if (maze[rand_wall[0] + 1][rand_wall[1]] != '.'):
                            maze[rand_wall[0] + 1][rand_wall[1]] = '#'
                        if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] + 1, rand_wall[1]])

                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1] - 1] != '.'):
                            maze[rand_wall[0]][rand_wall[1] - 1] = '#'
                        if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] - 1])

                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        if (rand_wall[0] != 0):
            if (maze[rand_wall[0] - 1][rand_wall[1]] == '2' and maze[rand_wall[0] + 1][rand_wall[1]] == '.'):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    maze[rand_wall[0]][rand_wall[1]] = '.'

                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0] - 1][rand_wall[1]] != '.'):
                            maze[rand_wall[0] - 1][rand_wall[1]] = '#'
                        if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1] - 1] != '.'):
                            maze[rand_wall[0]][rand_wall[1] - 1] = '#'
                        if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] - 1])

                    if (rand_wall[1] != width - 1):
                        if (maze[rand_wall[0]][rand_wall[1] + 1] != '.'):
                            maze[rand_wall[0]][rand_wall[1] + 1] = '#'
                        if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] + 1])

                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        if (rand_wall[0] != height - 1):
            if (maze[rand_wall[0] + 1][rand_wall[1]] == '2' and maze[rand_wall[0] - 1][rand_wall[1]] == '.'):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    maze[rand_wall[0]][rand_wall[1]] = '.'

                    if (rand_wall[0] != height - 1):
                        if (maze[rand_wall[0] + 1][rand_wall[1]] != '.'):
                            maze[rand_wall[0] + 1][rand_wall[1]] = '#'
                        if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] + 1, rand_wall[1]])
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1] - 1] != '.'):
                            maze[rand_wall[0]][rand_wall[1] - 1] = '#'
                        if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] - 1])
                    if (rand_wall[1] != width - 1):
                        if (maze[rand_wall[0]][rand_wall[1] + 1] != '.'):
                            maze[rand_wall[0]][rand_wall[1] + 1] = '#'
                        if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] + 1])

                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        if (rand_wall[1] != width - 1):
            if (maze[rand_wall[0]][rand_wall[1] + 1] == '2' and maze[rand_wall[0]][rand_wall[1] - 1] == '.'):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    maze[rand_wall[0]][rand_wall[1]] = '.'

                    if (rand_wall[1] != width - 1):
                        if (maze[rand_wall[0]][rand_wall[1] + 1] != '.'):
                            maze[rand_wall[0]][rand_wall[1] + 1] = '#'
                        if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] + 1])
                    if (rand_wall[0] != height - 1):
                        if (maze[rand_wall[0] + 1][rand_wall[1]] != '.'):
                            maze[rand_wall[0] + 1][rand_wall[1]] = '#'
                        if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] + 1, rand_wall[1]])
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0] - 1][rand_wall[1]] != '.'):
                            maze[rand_wall[0] - 1][rand_wall[1]] = '#'
                        if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        for wall in walls:
            if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                walls.remove(wall)

    for i in range(0, height):
        for j in range(0, width):
            if (maze[i][j] == '2'):
                maze[i][j] = '#'

    for i in range(0, width):
        if (maze[1][i] == '#'):
            maze[0][i] = '.'
            break

    for i in range(width - 1, 0, -1):
        if (maze[height - 2][i] == '.'):
            maze[height - 1][i] = '.'
            break
    printMaze(maze)

    return maze


@app.route('/')
def index():
    return render_template("game.html")


@app.route('/test/init_map')
def init_map():
    Base.query.delete()
    Object.query.delete()
    Player.query.delete()
    Bullet.query.delete()
    m = map_generator(32, 32)
    for i in range(len(m)):
        for j in range(len(m[i])):
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
    users = list(User.query.all())
    players = list(Player.query.all())
    objects = list(Object.query.all())
    bases = list(Base.query.all())
    bullets = list(Bullet.query.all())

    return jsonify({
        "users": [user.as_dict() for user in users],
        "players": [player.as_dict() for player in players],
        "objects": [object1.as_dict() for object1 in objects],
        "bases": [base.as_dict() for base in bases],
        "bullets": [bullet.as_dict() for bullet in bullets],
        "width": 32,
        "height": 32
    })


app.run(HOST, PORT, debug=DEBUG)
