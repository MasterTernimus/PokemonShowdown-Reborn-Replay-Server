import json
import os
import re
from collections import defaultdict
from datetime import datetime


def create_replay_object(log: dict, show_full_damage: bool = False):
    if not all(key in log for key in ('p1', 'p2', 'log', 'inputLog', 'roomid', 'format')):
        raise ValueError("Invalid log object")

    if not show_full_damage:
        log['log'] = hide_full_damage(log['log'])

    log_as_string = "\n".join(log['log'])[:-1]

    timestamp = get_unix_timestamp(log['timestamp'])

    private = {
        'private': log['roomid'].count('-') == 3,
        'password': "" if not log['roomid'].count('-') == 3 else log['roomid'].split('-')[3]
    }

    format = log['format']

    if "|tier|" in log_as_string:
        format = log_as_string.split("|tier|")[1].split("\n")[0]

    return {
        'id': log['roomid'],
        'format': format,
        'p1': log['p1'],
        'p2': log['p2'],
        'log': log_as_string,
        'inputLog': log['inputLog'],
        'timestamp': timestamp,
        'private': private
    }


def create_replay(replay: dict,
                  replay_embed_location="https://play.pokemonshowdown.com/js/replay-embed.js"):  # the replay you would get when downloading a replay from Pokemon Showdown
    html = f"""<!DOCTYPE html>
<meta charset="utf-8" />
<!-- version 1 -->
<title>{replay['format']}: {replay['p1']} vs. {replay['p2']}</title>
<style>
html,body {{font-family:Verdana, sans-serif;font-size:10pt;margin:0;padding:0;}}body{{padding:12px 0;}} .battle-log {{font-family:Verdana, sans-serif;font-size:10pt;}} .battle-log-inline {{border:1px solid #AAAAAA;background:#EEF2F5;color:black;max-width:640px;margin:0 auto 80px;padding-bottom:5px;}} .battle-log .inner {{padding:4px 8px 0px 8px;}} .battle-log .inner-preempt {{padding:0 8px 4px 8px;}} .battle-log .inner-after {{margin-top:0.5em;}} .battle-log h2 {{margin:0.5em -8px;padding:4px 8px;border:1px solid #AAAAAA;background:#E0E7EA;border-left:0;border-right:0;font-family:Verdana, sans-serif;font-size:13pt;}} .battle-log .chat {{vertical-align:middle;padding:3px 0 3px 0;font-size:8pt;}} .battle-log .chat strong {{color:#40576A;}} .battle-log .chat em {{padding:1px 4px 1px 3px;color:#000000;font-style:normal;}} .chat.mine {{background:rgba(0,0,0,0.05);margin-left:-8px;margin-right:-8px;padding-left:8px;padding-right:8px;}} .spoiler {{color:#BBBBBB;background:#BBBBBB;padding:0px 3px;}} .spoiler:hover, .spoiler:active, .spoiler-shown {{color:#000000;background:#E2E2E2;padding:0px 3px;}} .spoiler a {{color:#BBBBBB;}} .spoiler:hover a, .spoiler:active a, .spoiler-shown a {{color:#2288CC;}} .chat code, .chat .spoiler:hover code, .chat .spoiler:active code, .chat .spoiler-shown code {{border:1px solid #C0C0C0;background:#EEEEEE;color:black;padding:0 2px;}} .chat .spoiler code {{border:1px solid #CCCCCC;background:#CCCCCC;color:#CCCCCC;}} .battle-log .rated {{padding:3px 4px;}} .battle-log .rated strong {{color:white;background:#89A;padding:1px 4px;border-radius:4px;}} .spacer {{margin-top:0.5em;}} .message-announce {{background:#6688AA;color:white;padding:1px 4px 2px;}} .message-announce a, .broadcast-green a, .broadcast-blue a, .broadcast-red a {{color:#DDEEFF;}} .broadcast-green {{background-color:#559955;color:white;padding:2px 4px;}} .broadcast-blue {{background-color:#6688AA;color:white;padding:2px 4px;}} .infobox {{border:1px solid #6688AA;padding:2px 4px;}} .infobox-limited {{max-height:200px;overflow:auto;overflow-x:hidden;}} .broadcast-red {{background-color:#AA5544;color:white;padding:2px 4px;}} .message-learn-canlearn {{font-weight:bold;color:#228822;text-decoration:underline;}} .message-learn-cannotlearn {{font-weight:bold;color:#CC2222;text-decoration:underline;}} .message-effect-weak {{font-weight:bold;color:#CC2222;}} .message-effect-resist {{font-weight:bold;color:#6688AA;}} .message-effect-immune {{font-weight:bold;color:#666666;}} .message-learn-list {{margin-top:0;margin-bottom:0;}} .message-throttle-notice, .message-error {{color:#992222;}} .message-overflow, .chat small.message-overflow {{font-size:0pt;}} .message-overflow::before {{font-size:9pt;content:'...';}} .subtle {{color:#3A4A66;}}
</style>
<div class="wrapper replay-wrapper" style="max-width:1180px;margin:0 auto">
<input type="hidden" name="replayid" value="{replay['id']}" />
<div class="battle"></div><div class="battle-log"></div><div class="replay-controls"></div><div class="replay-controls-2"></div>
<script type="text/plain" class="battle-log-data">{replay['log']}
</script>
</div>
<script>
let daily = Math.floor(Date.now()/1000/60/60/24);document.write('<script src="{replay_embed_location}?version'+daily+'"></'+'script>');
</script>"""

    return html

def upload_replay_start(replay: dict, client_location: str = "https://play.pokemonshowdown.com"):
    html = f"""<!DOCTYPE html>
<html><head>

	<meta charset="utf-8" />

	<title>{replay['format']} replay: {replay['p1']} vs. {replay['p2']} - Pok&eacute;mon Showdown</title>

	<meta name="description" content="Watch a replay of a Pokémon battle between {replay['p1']} and {replay['p2']} ({replay['format']})" />

	<meta http-equiv="X-UA-Compatible" content="IE=Edge,chrome=IE8" />
	<link rel="stylesheet" href="https://{client_location}/style/font-awesome.css?932f42c7" />
	<link rel="stylesheet" href="https://pokemonshowdown.com/theme/panels.css?0.8626627733285226" />
	<link rel="stylesheet" href="https://pokemonshowdown.com/theme/main.css?0.9739025453096699" />
	<link rel="stylesheet" href="https://{client_location}/style/battle.css?8e37a9fd" />
	<link rel="stylesheet" href="https://{client_location}/style/replay.css?cfa51183" />
	<link rel="stylesheet" href="https://{client_location}/style/utilichart.css?e39c48cf" />
	<!-- Workarounds for IE bugs to display trees correctly. -->
	<!--[if lte IE 6]><style> li.tree {{ height: 1px; }} </style><![endif]-->
	<!--[if IE 7]><style> li.tree {{ zoom: 1; }} </style><![endif]-->

</head><body>

	<div class="pfx-topbar">
		<div class="header">
			<ul class="nav">
				<li><a class="button nav-first" href="https://pokemonshowdown.com/?0.03188637145193396"><img src="https://pokemonshowdown.com/images/pokemonshowdownbeta.png?0.02847646698151296" alt="Pok&eacute;mon Showdown! (beta)" /> Home</a></li>
				<li><a class="button" href="https://dex.pokemonshowdown.com/?0.5521979938481671">Pok&eacute;dex</a></li>
				<li><a class="button cur" href="/?0.5977172940377489">Replays</a></li>
				<li><a class="button" href="https://pokemonshowdown.com/ladder/?0.5868977915492632">Ladder</a></li>
				<li><a class="button nav-last" href="https://pokemonshowdown.com/forums/?0.0327954326633102">Forum</a></li>
			</ul>
			<ul class="nav nav-play">
				<li><a class="button greenbutton nav-first nav-last" href="http://play.pokemonshowdown.com/">Play</a></li>
			</ul>
			<div style="clear:both"></div>
		</div>
	</div>
	<div class="pfx-panel"><div class="pfx-body" style="max-width:1180px">
		<div class="wrapper replay-wrapper">

			<div class="battle"><div class="playbutton"><button disabled>Loading...</button></div></div>
			<div class="battle-log"></div>
			<div class="replay-controls">
				<button data-action="start"><i class="fa fa-play"></i> Play</button>
			</div>
			<div class="replay-controls-2">
				<div class="chooser leftchooser speedchooser">
					<em>Speed:</em>
					<div><button value="hyperfast">Hyperfast</button> <button value="fast">Fast</button><button value="normal" class="sel">Normal</button><button value="slow">Slow</button><button value="reallyslow">Really Slow</button></div>
				</div>
				<div class="chooser colorchooser">
					<em>Color&nbsp;scheme:</em>
					<div><button class="sel" value="light">Light</button><button value="dark">Dark</button></div>
				</div>
				<div class="chooser soundchooser" style="display:none">
					<em>Music:</em>
					<div><button class="sel" value="on">On</button><button value="off">Off</button></div>
				</div>
			</div>
			<!--[if lte IE 8]>
				<div class="error"><p>&#3232;_&#3232; <strong>You're using an old version of Internet Explorer.</strong></p>
				<p>We use some transparent backgrounds, rounded corners, and other effects that your old version of IE doesn't support.</p>
				<p>Please install <em>one</em> of these: <a href="http://www.google.com/chrome">Chrome</a> | <a href="http://www.mozilla.org/en-US/firefox/">Firefox</a> | <a href="http://windows.microsoft.com/en-US/internet-explorer/products/ie/home">Internet Explorer 9</a></p></div>
			<![endif]-->


			<pre class="urlbox" style="word-wrap: break-word;">https://replay.pokemonshowdown.com/{replay['id'].split("battle-")[1]}</pre>

			<h1 style="font-weight:normal;text-align:left"><strong>{replay['format']}</strong>: <a href="https://pokemonshowdown.com/users/{replay['p1']}" class="subtle">{replay['p1']}</a> vs. <a href="https://pokemonshowdown.com/users/{replay['p2']}" class="subtle">{replay['p2']}</a></h1>
			<p style="padding:0 1em;margin-top:0">
				<small class="uploaddate" data-timestamp="{replay['timestamp']}"><em>Uploaded:</em> {datetime.fromtimestamp(replay['timestamp']).strftime("%m/%d/%Y %H:%M:%S")}</small>
			</p>

			<div id="loopcount"></div>
		</div>

		<input type="hidden" name="replayid" value="{replay['id'].split("battle-")[1]}" />

		<script type="text/plain" class="log">"""

    return html


def upload_replay_end(client_location: str = "https://play.pokemonshowdown.com"):
    return f"""</script>



		<a href="/index.php" class="pfx-backbutton" data-target="back"><i class="fa fa-chevron-left"></i> Other replays</a>

	</div></div>
	<script src="{client_location}/js/lib/jquery-1.11.0.min.js"></script>
	<script src="{client_location}/js/lib/lodash.core.js"></script>
	<script src="{client_location}/js/lib/backbone.js"></script>
	<script src="https://dex.pokemonshowdown.com/js/panels.js"></script>

	<script src="{client_location}/js/lib/jquery-cookie.js"></script>
	<script src="{client_location}/js/lib/html-sanitizer-minified.js"></script>
	<script src="{client_location}/js/battle-sound.js"></script>
	<script src="{client_location}/config/config.js"></script>
	<script src="{client_location}/js/battledata.js"></script>
	<script src="{client_location}/data/pokedex-mini.js"></script>
	<script src="{client_location}/data/pokedex-mini-bw.js"></script>
	<script src="{client_location}/data/graphics.js"></script>
	<script src="{client_location}/data/pokedex.js"></script>
	<script src="{client_location}/data/items.js"></script>
	<script src="{client_location}/data/moves.js"></script>
	<script src="{client_location}/data/abilities.js"></script>
	<script src="{client_location}/data/teambuilder-tables.js"></script>
	<script src="{client_location}/js/battle-tooltips.js"></script>
	<script src="{client_location}/js/battle.js"></script>
	<script src="{client_location}/replays/js/replay.js"></script>

</body></html>
"""


def create_replay(replay: dict,
                  client_location="https://play.pokemonshowdown.com"):  # the type of replay at https://replay.pokemonshowdown.com/
    start = upload_replay_start(replay, client_location=client_location)
    log = replay['log']
    end = upload_replay_end(client_location=client_location)

    return start + log + end


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
old_months = [f"../../lib/PokemonShowdown-Reborn/logs/{m}" for m in old_months]
subfolders = [f.path for f in os.scandir(
    "../../lib/PokemonShowdown-Reborn/logs/") if f.is_dir() and f.path[-3] == "-"]
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

        replay_object = create_replay_object(log, show_full_damage=True)
        html = create_replay(replay_object,
                                      replay_embed_location=replay_embed_location)
        with open(path, "w") as f:
            f.write(html)

        with open(logPath, "w") as f:
            for line in log["log"]:
                f.write(line + "\n")

print("Generated Replays")
