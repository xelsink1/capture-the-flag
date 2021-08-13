import time
import importlib
from ctf_server import app, Player, Bullet, get_state, db, Object

available_choices = ["go_up", "go_down", "go_right", "go_left", "fire_up", "fire_down", "fire_right", "fire_left"]


def get_choice(player, state):
    try:
        location_module = importlib.import_module("bots.bot_{}".format(player.id))
        choice = location_module.make_choice(player, state)

        if choice not in available_choices:
            return None
        return choice
    except Exception as e:
        print(e)
        return None

def is_it_a_base(x, y, player):
    state1 = get_state()
    bases = state1["bases"]
    for base in bases:
        if (base["y"] == y) and (base["x"] == x) and (player.base == base):
            return base

    return None


def is_it_a_player(x, y):
    state1 = get_state()
    players1 = state1["players"]
    for pl in players1:
        if (pl["y"] == y) and (pl["x"] == x):
            return pl
    return None


def is_it_an_object(x, y, hype, objects):
    intercept = list(filter(lambda obj: obj.x == x and obj.y == y and obj.type == hype, objects))
    if len(intercept) != 0:
        return intercept[0]
    return None


def bullet_launch(player1, side):
    if player1.bullets != 0:
        bullet = Bullet()
        bullet.side = side
        player1.bullets -= 1
        if bullet.side == "up":
            bullet.x = player1.x
            bullet.y = player1.y - 1
        if bullet.side == "down":
            bullet.x = player1.x
            bullet.y = player1.y + 1
        if bullet.side == "right":
            bullet.x = player1.x + 1
            bullet.y = player1.y
        if bullet.side == "left":
            bullet.x = player1.x - 1
            bullet.y = player1.y
        db.session.add(bullet)
    else:
        return None


def bullet_move(bullets, objects, players):

    for bullet in bullets:
        intercept = list(filter(lambda obj: obj.x == bullet.x and obj.y == bullet.y, objects))
        for obj in intercept:
            if obj.type == "wall":
                obj.hp -= 1
                if obj.hp == 0:
                    db.session.delete(obj)
                db.session.delete(bullet)
        intercept2 = list(filter(lambda play: play.x == bullet.x and play.y == bullet.y, players))
        for play in intercept2:
            play.hp -= 1
            if play.hp == 0:
                db.session.delete(play)
            db.session.delete(bullet)
        if bullet.side == "up":
            bullet.y -= 1
        if bullet.side == "down":
            bullet.y += 1
        if bullet.side == "right":
            bullet.x += 1
        if bullet.side == "left":
            bullet.x -= 1




        # play = is_it_a_player(bullet.x, bullet.y)
        # if play:
        #     play["hp"] -= 1
        #     db.session.delete(bullet)


if __name__ == "__main__":
    with app.app_context():
        players = Player.query.all()

        active_players = list(filter(lambda x: x.code, players))

        for player in active_players:
            with open('bots/bot_{}.py'.format(player.id), 'w') as file:
                file.write(player.code)

        while True:
            state = get_state()
            choices = {}
            objects = Object.query.all()
            bullets = Bullet.query.all()

            for player in active_players:
                choices[player.id] = get_choice(player, state)

            bullet_move(bullets, objects, players)

            for player in active_players:
                if choices[player.id] == "go_up":
                    if not is_it_an_object(player.x, (player.y - 1), "wall", objects) and (player.y > 0):
                        player.y -= 1
                    player.side = "up"
                if choices[player.id] == "go_down":
                    if not is_it_an_object(player.x, (player.y + 1), "wall", objects) and (player.y < 32):
                        player.y += 1
                    player.side = "down"
                if choices[player.id] == "go_left":
                    if not is_it_an_object((player.x - 1), player.y, "wall", objects) and (player.x > 0):
                        player.x -= 1
                    player.side = "left"
                if choices[player.id] == "go_right":
                    if not is_it_an_object((player.x + 1), player.y, "wall", objects) and (player.x < 32):
                        player.x += 1
                    player.side = "right"

                if is_it_an_object(player.x, player.y, "flag", objects):
                    player.has_flag = True
                    db.session.delete(is_it_an_object(player.x, player.y, "flag", objects))
                if is_it_an_object(player.x, player.y, "medkit", objects) and (player.hp < 3):
                    player.hp += 1
                    db.session.delete(is_it_an_object(player.x, player.y, "medkit", objects))
                if is_it_an_object(player.x, player.y, "ammo", objects):
                    player.bullets += 6
                    db.session.delete(is_it_an_object(player.x, player.y, "ammo", objects))
                # if is_it_a_base(player.x, player.y, player):
                #     break

                if choices[player.id] == "fire_up":
                    bullet_launch(player, "up")
                if choices[player.id] == "fire_down":
                    bullet_launch(player, "down")
                if choices[player.id] == "fire_right":
                    bullet_launch(player, "right")
                if choices[player.id] == "fire_left":
                    bullet_launch(player, "left")

                print("Player {} is on ({}, {})".format(player.id, player.x, player.y))

            db.session.commit()
            time.sleep(1)
            print(" - - " * 10)
