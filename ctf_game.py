import time
import importlib
from ctf_server import app, Player, Bullet, get_state, db

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


def is_it_a_player(x, y):
    state1 = get_state()
    players1 = state1["players"]
    for pl in players1:
        if (pl["y"] == y) and (pl["x"] == x):
            return pl
    return None


def is_it_an_object(x, y, hype):
    state1 = get_state()
    objects1 = state1["objects"]
    for obj in objects1:
        if (obj["y"] == y) and (obj["x"] == x) and (obj["type"] == hype):
            return obj
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
        db.session.commit()
    else:
        return None


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
            objects = state["objects"]
            bullets = Bullet.query.all()

            for player in active_players:
                choices[player.id] = get_choice(player, state)

            for bullet in bullets:
                while not is_it_an_object(bullet.x, bullet.y, "wall") and not is_it_a_player(bullet.x, bullet.y):
                    if bullet.side == "up":
                        bullet.y -= 1
                    if bullet.side == "down":
                        bullet.y += 1
                    if bullet.side == "right":
                        bullet.x += 1
                    if bullet.side == "left":
                        bullet.y -= 1
                wall = is_it_an_object(bullet.x, bullet.y, "wall")
                if wall:
                    wall["hp"] -= 1
                    if wall["hp"] == 0:
                        db.session.delete(wall)
                    db.session.delete(bullet)

                play = is_it_a_player(bullet.x, bullet.y)
                if play:
                    play["hp"] -= 1
                    db.session.delete(bullet)

            for player in active_players:
                if choices[player.id] == "go_up":
                    if not is_it_an_object(player.x, (player.y - 1), "wall") and (player.y != 0):
                        player.y -= 1
                    player.side = "up"
                if choices[player.id] == "go_down":
                    if not is_it_an_object(player.x, (player.y + 1), "wall") and (player.y < 32):
                        player.y += 1
                    player.side = "down"
                if choices[player.id] == "go_left":
                    if not is_it_an_object((player.x - 1), player.y, "wall") and (player.x != 0):
                        player.x -= 1
                    player.side = "left"
                if choices[player.id] == "go_right":
                    if not is_it_an_object((player.x + 1), player.y, "wall") and (player.x < 32):
                        player.x += 1
                    player.side = "right"

                if is_it_an_object(player.x, player.y, "flag"):
                    player.has_flag = True

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
