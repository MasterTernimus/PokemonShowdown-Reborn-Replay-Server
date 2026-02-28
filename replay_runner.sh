trap "echo 'Exited!'; exit" SIGINT SIGTERM

while true; do
    inotifywait -r -e modify,create,delete ../../lib/PokemonShowdown-Reborn/logs/
    
    echo "Change detected. Regenerating..."
    
    python generate_replays.py
    python generate_csv.py
done