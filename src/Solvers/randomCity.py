#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Créé le 17 Oct 2018

@author: PierreLeGuen
'''

import sys
import os
sys.path.insert(0, "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-2])+"/")
print(sys.path)
from src.InOutManager.inputmanager import InManager
from src.InOutManager.outputmanager import OutManager
from src.ScoringTools.calculScore import *
from src.projectDisplay import *
from src.projectListBuilder import projectListBuilder
from src.projectListBuilder import getBuildedNums
from src.project import *
from src.grid import Grid
from src.ScoringTools import calculWeight
import random
import time
import copy
from src.constants import Const


def randomSolver(nbErreurs, choixExercice):
    """
    Fonction permettant de remplir la matrice "city plan" de façon aléatoire.

    :param nbErreurs: (int) nombre d'erreurs maximale autorisée
    :param choixExercice: (int) choisir parmi les "inputs" fournis par Google. 0->a_*, 5->f_*
    """
    nbErreursCourant = 0

    print("Random Solver lancé !")
    print("Création de grille lancée à : " + time.strftime('%H:%M:%S'))
    print("chargement des projets du fichier " + Const.FILE_NAMES[choixExercice] + ".in ...")
    inputs = InManager(Const.FILE_NAMES[choixExercice])
    maximumDistance = inputs.walkDist

    # ici on charge dans projectList les projets présents dans le fichier
    projectList, trueNum = projectListBuilder(inputs)

    print("fichiers chargés\n\nconstructions des batiments ...")

    city = Grid(inputs.rows, inputs.columns)
    while nbErreursCourant < nbErreurs: # Condition d'arrêt : après un certains nombre d'érreurs consecutives

        # sélection aléatoire de coordonnées et de type de batiment
        numProjectRand = random.randint(0, len(projectList)-1)
        numColsRand = random.randint(0, inputs.columns)
        numRowsRand = random.randint(0, inputs.rows)

        if city.isBuildable(projectList[numProjectRand], (numRowsRand, numColsRand)):
            # Si le projet peut-être placé alors nous le plaçons aux coordonnées définie aléatoirement.
            city.buildProject(projectList[numProjectRand], (numRowsRand, numColsRand))
        else : 
            nbErreursCourant += 1

    inputs.close()

    print("limite de {} erreurs atteinte".format(nbErreursCourant) + " : grille construite")

    out = OutManager("{} {}".format(Const.FILE_NAMES[choixExercice], time.strftime('%d-%m-%Y %H-%M-%S')))

    # city.showNumProject() # Prend beaucoup de ressources.

    print("nombre de batiments résidentiels : ", len(city.buildedR), " / utilitaires : ", len(city.buildedU), "\n")

    # on calcule le score et on l'écrit dans un fichier et dans le terminal
    score = getGridScore(projectList, maximumDistance, city.buildedR, city.buildedU, True)
    out.writeScore(score)
    out.writeProjects(getBuildedNums(city.buildedR + city.buildedU, trueNum))
    print("score = ", score)
    # printGrid(city, projectList) # Affichage avec TKinter
    Grid.show(city) # Affiche la grille dans la console
