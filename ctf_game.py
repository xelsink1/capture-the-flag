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
            objects = state(key="objects")

            for player in active_players:
                choices[player.id] = get_choice(player, state)

            for player in active_players:
                if choices[player.id] == "go_up":
                    if player.y != 0:
                        player.y -= 1
                    player.side = "up"
                if choices[player.id] == "go_down":
                    if player.y < 32:
                        player.y += 1
                if choices[player.id] == "go_left":
                    if player.x > 0:
                        player.x -= 1
                if choices[player.id] == "go_right":
                    if player.x < 32:
                        player.x += 1

                print("Player {} is on ({}, {})".format(player.id, player.x, player.y))

            db.session.commit()
            time.sleep(1)
            print(" - - " * 10)
