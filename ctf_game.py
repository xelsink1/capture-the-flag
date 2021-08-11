import time
import importlib
from ctf_server import app, Player, get_state, db

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


def is_it_an_object(objects, x, y, type):
    for obj in objects:
        if (obj["y"] == y) and (obj["x"] == x) and (obj["type"] == type):
            return True
    return False


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

            for player in active_players:
                choices[player.id] = get_choice(player, state)

            for player in active_players:
                if choices[player.id] == "go_up":
                    if not is_it_an_object(objects, player.x, (player.y - 1), "wall") and (player.y != 0):
                        player.y -= 1
                    player.side = "up"
                if choices[player.id] == "go_down":
                    if not is_it_an_object(objects, player.x, (player.y + 1), "wall") and (player.y < 32):
                        player.y += 1
                    player.side = "down"
                if choices[player.id] == "go_left":
                    if not is_it_an_object(objects, (player.x - 1), player.y, "wall") and (player.x != 0):
                        player.x -= 1
                    player.side = "left"
                if choices[player.id] == "go_right":
                    if not is_it_an_object(objects, (player.x + 1), player.y, "wall") and (player.x < 32):
                        player.x += 1
                    player.side = "right"
                if is_it_an_object(objects, player.x, player.y, "flag"):
                    player.has_flag = True

                print("Player {} is on ({}, {})".format(player.id, player.x, player.y))

            db.session.commit()
            time.sleep(1)
            print(" - - " * 10)
