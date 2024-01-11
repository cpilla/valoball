import json
with open("leaderboard.json", "r") as f:
    data = json.load(f)

for entry in data:
    entry["elo"] = 850
    entry["wins"] = 0
    entry["losses"] = 0

with open("leaderboard.json", "w") as f:
    json.dump(data, f)