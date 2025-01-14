from evaluator import calculer_moyenne_scores
import os

WORKDIR = os.getcwd()
if __name__=="__main__":
    dossier_input = os.path.abspath(os.path.join(WORKDIR,"data/Results/mixtral-8x7b-32768"))
    fichier_output = os.path.abspath(os.path.join(WORKDIR,"data/finalscores/mixtral-8x7b-32768/mixtral-8x7b-32768.json"))
    calculer_moyenne_scores(dossier_input, fichier_output)
