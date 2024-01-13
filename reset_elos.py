import json
from random import randint

with open("leaderboard.json", "r") as f:
    data = json.load(f)
names = ["cam", "tommy", "eddy", "isabelle", "kev", "kyaw", "nathan", "manny", "sam", "beebus"]

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

for name in names:
    id = random_with_N_digits(18)
    elo = random_with_N_digits(3)
    data[id] = {"name": name, "wins": 0, "losses": 0, "elo": elo, "id": id}

with open("leaderboard.json", "w") as f:
    json.dump(data, f)