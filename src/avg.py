from evaluator import calculer_moyenne_scores

if __name__=="__main__":
    dossier_input = "/home/laris/laris/NER/data/Results/mixtral-8x7b-32768"
    fichier_output = "/home/laris/laris/NER/data/finalscores/mixtral-8x7b-32768/mixtral-8x7b-32768.json"
    calculer_moyenne_scores(dossier_input, fichier_output)
