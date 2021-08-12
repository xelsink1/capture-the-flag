import random


def make_choice(players, state):
    return random.choice(["fire_up", "fire_down", "fire_right", "fire_left", "go_up", "go_down", "go_right", "go_left"])