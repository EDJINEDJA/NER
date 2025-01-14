import os
import json

def save_dict_to_folder(dicts: dict, folder: str, filename:str):
    """
    Sauvegarde plusieurs dictionnaires dans des fichiers JSON dans un dossier donné.
    
    Args:
        dicts (dict): Dictionnaire où les clés sont les noms de fichiers et les valeurs sont les dictionnaires à enregistrer.
        folder (str): Le chemin du dossier où enregistrer les fichiers JSON.
    """
    # Créer le dossier si nécessaire
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Le dossier '{folder}' a été créé.")

  
    # Créer un chemin de fichier pour le dictionnaire
    file_path = os.path.join(folder, f"{filename}.json")
    
    # Enregistrer le dictionnaire dans le fichier JSON
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(dicts, f, indent=4, ensure_ascii=False)
        print(f"Dictionnaire enregistré sous : {file_path}")