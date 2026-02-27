from pokemon_showdown_replays import Replay, Download
import json
import os
import re
from collections import defaultdict

replay_embed_location="https://play.pokemonreborn-showdown.xyz/js/replay-embed.js"
# Helpful to avoid regenerating replays to speed up script
old_months = ["2023-01", "2023-02", "2023-03", "2023-04",
              "2023-05", "2023-06", "2023-07", "2023-08",
              "2023-09", "2023-10", "2023-11", "2023-12",
              "2024-01", "2024-02", "2024-03", "2024-04",
              "2024-05", "2024-06", "2024-07", "2024-08",
              "2024-09", "2024-10", "2024-11", "2024-12", "2025-01",
              "2025-02", "2025-03", "2025-04", "2025-05"]
# old_months = []
old_months = [f"../../PokemonShowdown-Reborn/logs/{m}" for m in old_months]
subfolders = [f.path for f in os.scandir(
    "../../PokemonShowdown-Reborn/logs/") if f.is_dir() and f.path[-3] == "-"]
subfolders = set(subfolders) - set(old_months)
log_json_dict = defaultdict(list)


for dir in subfolders:
    if "-" in dir:
        format_folders = [f.path for f in os.scandir(dir) if f.is_dir()]
        for format_folder in format_folders:
            format = format_folder.split("/")[-1]
            day_folders = [f.path for f in os.scandir(
                format_folder) if f.is_dir()]
            for day_folder in day_folders:
                log_jsons = [f.path for f in os.scandir(day_folder)]
                for log_json in log_jsons:
                    log_json_dict[format].append(log_json)

for format, log_jsons in log_json_dict.items():
    format_dir = f"../PokemonShowdown-Client/play.pokemonshowdown.com/replays/{format}"
    if not os.path.exists(format_dir):
        os.makedirs(format_dir)
    for log_json in log_jsons:
        if not log_json.endswith(".json"):
            continue
        with open(log_json) as file:
            log = json.load(file)
        if log["turns"] < 2:
            continue
        id = log["roomid"].split("-")[2]
        p1 = re.sub(r'\W+', '', log['p1'])
        p2 = re.sub(r'\W+', '', log['p2'])
        p1 = p1.replace("_", "")
        p2 = p2.replace("_", "")
        name = f"{id}_{p1}_vs_{p2}.html"
        path = f"{format_dir}/{name}"
        logPath = f"{path}.log"
        # Skip if the replay already exists
        if (os.path.exists(path) and os.path.exists(logPath)):
            continue

        replay_object = Replay.create_replay_object(log, show_full_damage=True)
        html = Download.create_replay(replay_object,
                                      replay_embed_location=replay_embed_location)
        with open(path, "w") as f:
            f.write(html)

        with open(logPath, "w") as f:
            for line in log["log"]:
                f.write(line + "\n")

print("Generated Replays")
