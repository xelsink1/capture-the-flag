import random


def make_choice(players, state):
    return random.choice(["go_up", "go_down", "go_right", "go_left", "fire_up", "fire_down", "fire_right", "fire_left"])