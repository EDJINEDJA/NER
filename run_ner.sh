#!/bin/bash

# Chemin du script Python
SCRIPT="src/ner.py"

# Boucle infinie pour exécuter le script toutes les 2 minutes
while true; do
    echo "Exécution de $SCRIPT à $(date)"
    python3 $SCRIPT
    echo "Attente de 1 minutes..."
    sleep 15
done
