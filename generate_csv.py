import os
import csv
import json
import re

server_location = "https://play.pokemonreborn-showdown.xyz"

month_to_index = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}

def fix_species(species):
    if (species.startswith("Alcremie")):
        return "Alcremie"
    if (species.startswith("Magearna")):
        return "Magearna"
    if (species.startswith("Polteageist")):
        return "Polteageist"
    if (species.startswith("Keldeo")):
        return "Keldeo"
    if (species.startswith("Minior")):
        return "Minior"
    if (species.startswith("Pikachu")):
        return "Pikachu"
    if (species.startswith("Sawsbuck")):
        return "Sawsbuck"
    if (species.startswith("Maushold")):
        return "Maushold"
    if (species.startswith("Dudunsparce")):
        return "Dudunsparce"
    if (species.startswith("Vivillon")):
        return "Vivillon"
    return species


def process_logs(folder_path, output_csv):
    # Create or open the CSV file for writing
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['tier', 'p1', 'p2', 'score', 'date',
                      'link', 'team1', 'team2', 'turns', 'winner']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header to the CSV file
        csv_writer.writeheader()

        # Walk through all files in the 'logs' folder and its subdirectories
        for root, _, files in os.walk(folder_path):
            for filename in files:
                if filename.endswith(".json"):
                    file_path = os.path.join(root, filename)

                    # Read the JSON file and extract relevant elements
                    with open(file_path, 'r') as json_file:
                        try:
                            data = json.load(json_file)
                            turns = data.get('turns', 0)
                            if turns <= 2:
                                continue
                            room_id = data.get("roomid", '').split("-")[2]
                            p1 = data.get('p1', '')
                            p2 = data.get('p2', '')
                            winner = data.get('winner', '')
                            score = data.get('score', [0, 0])
                            score = f"{score[0]} - {score[1]}"
                            timestamp = data.get('timestamp', '')

                            team1 = data.get('p1team', [])
                            if team1:
                                team1 = [fix_species(p["species"]) for p in team1]
                            team2 = data.get('p2team', [])
                            if team2:
                                team2 = [fix_species(p["species"]) for p in team2]

                            tier = root.split("/")[-2]
                            p1id = re.sub(r'\W+', '', p1).replace("_", "")
                            p2id = re.sub(r'\W+', '', p2).replace("_", "")
                            link = f"{server_location}/replays/{tier}/{room_id}_{p1id}_vs_{p2id}.html"

                            # Write the values to the CSV file
                            csv_writer.writerow({
                                'tier': tier,
                                'winner': winner,
                                'p1': p1,
                                'score': score,
                                'p2': p2,
                                'date': timestamp,
                                'team1': "/".join(team1),
                                'team2': "/".join(team2),
                                'link': link,
                                'turns': turns,
                            })
                        except json.JSONDecodeError as e:
                            print(f"Error reading file {file_path}: {e}")
                        except Exception as e:
                            print(f"Error processing file {file_path}: {e}")


process_logs('../../PokemonShowdown-Reborn/logs',
             '../PokemonShowdown-Client/play.pokemonshowdown.com/replays/data.csv')
print("Generated CSV")
