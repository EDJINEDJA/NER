from typing import List, Dict, Tuple
import os
import json

def metric(tp:float, fn:float, fp:float)->Tuple[float,float,float]:
    # Calcul de la précision, du rappel et du F1-score
    if tp + fp > 0:
        precision = tp / (tp + fp)
    else:
        precision = 0.0

    if tp + fn > 0:
        recall = tp / (tp + fn)
    else:
        recall = 0.0

    if precision + recall > 0:
        f1 = 2 * (precision * recall) / (precision + recall)
    else:
        f1 = 0.0
    
    return recall, precision, f1

def split_list(input_list: List[str])->List[str]:
    return [item for sublist in [i.split() for i in input_list] for item in sublist]

def evaluate(predictions: Dict[str, List[str]], true_values: Dict[str, List[str]]) -> Dict[str, float]:
    """
    Fonction d'évaluation pour calculer les métriques de classification.
    
    Args:
        predictions (Dict[str, List[str]]): Dictionnaire des entités prédites par le modèle.
        true_values (Dict[str, List[str]]): Dictionnaire des entités réelles.

    Returns:
        Dict[str, float]: Dictionnaire des métriques calculées : précision, rappel, f1, et exactitude.
    """
    metrics = {}
    
    
    # Combinaison des noms et prénoms (PER = NAME + SURNAME)
    true_per = split_list(true_values.get('NAME', []) + true_values.get('SURNAME', []))
    true_LOC = split_list(true_values.get('LOC', []))
    true_ORG = split_list(true_values.get('ORG', []))
    true_MISC = split_list(true_values.get('MISC', []) + true_values.get('MISC1', [])) 

    predicted_per = split_list(predictions.get('PER', []))
    predicted_LOC = split_list(predictions.get('LOC', []))
    predicted_ORG = split_list(predictions.get('ORG', []))
    predicted_MISC = split_list(predictions.get('MISC', []))
    

    #PER

    # Calcul des Vrai Positifs, Faux Négatifs, Faux Positifs pour chaque entité
    # Comparaison exacte des entités
    tp = len(set(predicted_per).intersection(set(true_per)))  # Vrai Positifs
    fp = len(set(true_LOC+true_ORG+true_MISC).intersection(set(predicted_per)))  # Faux Positifs
    fn = len(set(predicted_LOC+predicted_ORG+predicted_MISC).intersection(set(true_per)))  # Faux Négatifs
 
  
    recall, precision, f1 = metric(tp, fn, fp)

    # Ajouter les résultats dans le dictionnaire des métriques
    metrics['PER']= {'precision':precision, 'recall': recall, 'f1_score': f1}
   

    #LOC

    # Calcul des Vrai Positifs, Faux Négatifs, Faux Positifs pour chaque entité
    # Comparaison exacte des entités
    tp = len(set(predicted_LOC).intersection(set(true_LOC)))  # Vrai Positifs
    fp = len(set(true_per+true_ORG+true_MISC).intersection(set(predicted_LOC)))  # Faux Positifs
    fn = len(set(predicted_per+predicted_ORG+predicted_MISC).intersection(set(true_LOC)))  # Faux Négatifs
 
  
    recall, precision, f1 = metric(tp, fn, fp)

    # Ajouter les résultats dans le dictionnaire des métriques
    metrics['LOC']= {'precision':precision, 'recall': recall, 'f1_score': f1}

    #ORG

    # Calcul des Vrai Positifs, Faux Négatifs, Faux Positifs pour chaque entité
    # Comparaison exacte des entités
    tp = len(set(predicted_ORG).intersection(set(true_ORG)))  # Vrai Positifs
    fp = len(set(true_per+true_LOC+true_MISC).intersection(set(predicted_ORG)))  # Faux Positifs
    fn = len(set(predicted_per+predicted_ORG+predicted_MISC).intersection(set(true_ORG)))  # Faux Négatifs
 
  
    recall, precision, f1 = metric(tp, fn, fp)

    # Ajouter les résultats dans le dictionnaire des métriques
    metrics['ORG']= {'precision':precision, 'recall': recall, 'f1_score': f1}


    #MISC

    # Calcul des Vrai Positifs, Faux Négatifs, Faux Positifs pour chaque entité
    # Comparaison exacte des entités
    tp = len(set(predicted_MISC).intersection(set(true_MISC)))  # Vrai Positifs
    fp = len(set(true_per+true_LOC+true_ORG).intersection(set(predicted_MISC)))  # Faux Positifs
    fn = len(set(predicted_per+predicted_ORG+predicted_ORG).intersection(set(true_MISC)))  # Faux Négatifs
 
  
    recall, precision, f1 = metric(tp, fn, fp)

    # Ajouter les résultats dans le dictionnaire des métriques
    metrics['MISC']= {'precision':precision, 'recall': recall, 'f1_score': f1}
   

    return metrics


def calculate_average_metrics(results: Dict[int, Dict[str, Dict[str, float]]]) -> Dict[str, Dict[str, float]]:
    """
    Calculer la moyenne des métriques (precision, recall, f1_score) pour chaque entité
    à travers toutes les simulations.
    
    Args:
        results (Dict[int, Dict[str, Dict[str, float]]]): Résultats des simulations.
    
    Returns:
        Dict[str, Dict[str, float]]: Moyennes des métriques pour chaque entité.
    """
    # Initialiser un dictionnaire pour accumuler les sommes des métriques
    averages = {}
    
    # Initialiser le nombre de simulations
    num_simulations = len(results)
    
    # Initialiser les clés pour chaque entité
    entities = ['PER', 'LOC', 'ORG', 'MISC']
    
    for entity in entities:
        # Initialiser un sous-dictionnaire pour chaque entité
        averages[entity] = {'precision': 0.0, 'recall': 0.0, 'f1_score': 0.0}
        
        # Additionner les valeurs pour chaque simulation
        for simulation_id in results:
            for metric in ['precision', 'recall', 'f1_score']:
                averages[entity][metric] += results[simulation_id].get(entity, {}).get(metric, 0.0)
        
        # Calculer la moyenne pour chaque métrique de l'entité
        for metric in ['precision', 'recall', 'f1_score']:
            averages[entity][metric] /= num_simulations
    
    return averages


def calculer_moyenne_scores(dossier_input, fichier_output):
    # Créer un dictionnaire pour stocker les sommes des scores pour chaque entité
    total_scores = {
        "PER": {"precision": 0, "recall": 0, "f1_score": 0},
        "LOC": {"precision": 0, "recall": 0, "f1_score": 0},
        "ORG": {"precision": 0, "recall": 0, "f1_score": 0},
        "MISC": {"precision": 0, "recall": 0, "f1_score": 0}
    }
    
    # Compteur pour le nombre de fichiers traités
    count = 0
    
    # Parcourir les fichiers JSON dans le dossier
    for fichier in os.listdir(dossier_input):
        if fichier.endswith('.json'):
            # Charger chaque fichier JSON
            with open(os.path.join(dossier_input, fichier), 'r') as f:
                data = json.load(f)
                
                # Ajouter les scores du fichier au total
                for entite in total_scores:
                    total_scores[entite]["precision"] += data["score"][entite]["precision"]
                    total_scores[entite]["recall"] += data["score"][entite]["recall"]
                    total_scores[entite]["f1_score"] += data["score"][entite]["f1_score"]
                
                count += 1
    
    # Calculer la moyenne pour chaque entité et arrondir à 2 chiffres
    for entite in total_scores:
        if count > 0:
            total_scores[entite]["precision"] = round(total_scores[entite]["precision"] / count, 2)
            total_scores[entite]["recall"] = round(total_scores[entite]["recall"] / count, 2)
            total_scores[entite]["f1_score"] = round(total_scores[entite]["f1_score"] / count, 2)
    
    # Préparer les données pour l'écriture dans le fichier de sortie
    resultats = {
        "score": total_scores
    }
    
    # Sauvegarder les résultats dans un fichier JSON
    with open(fichier_output, 'w') as f:
        json.dump(resultats, f, indent=4)
