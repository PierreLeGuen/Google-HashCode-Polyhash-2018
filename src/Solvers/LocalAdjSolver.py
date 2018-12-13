#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Créé le 14 Nov 2018

@author: Pierre Le Guen
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

from src.ScoringTools.calculScore import getGridScore
from src.constants import Const

def BestCitySolver(nbErreurs, choixExercice, nbSimus):
    """
    Fonction permettant de remplir la matrice "city plan" en divisant la grille originelle puis en maximisant le score dans cette grille plus petite. Puis multiplication pour retrouver la grille par défaut.

    :param nbErreurs: (int) nombre d'erreurs maximale autorisée
    :param choixExercice: (int) choisir parmi les "inputs" fournis par Google. 0->a_*, 5->f_*
    :param nbSimu: (int) nombre de simulation à effectuer pour obtenir la meilleur grille
    """

    simulation_not_stop = True
    score_max = 0
    i = 0
    print("Algo d'adjacence locale lancé !")
    print("Création de grille lancée à : " + time.strftime('%H:%M:%S'))
    print("chargement des projets du fichier " + Const.FILE_NAMES[choixExercice] + ".in ...")
    inputs = InManager(Const.FILE_NAMES[choixExercice])
    maximumDistance = inputs.walkDist

    # ici on charge dans projectList les projets présents dans le fichier
    projectList, trueNum = projectListBuilder(inputs)

    print("fichiers chargés\n\nconstructions des batiments ...")

    rows = inputs.rows
    columns = inputs.columns
    if inputs.rows == 1000:
        rows = inputs.rows//10
        columns = inputs.columns//10
    best_city = Grid(rows,columns)
    nbErreursCourant = 0
    initialization = True

    # ici on charge dans projectList les projets présents dans le fichier
    i = 0
    n = 0
    while projectList[i].isResid():
        i += 1
    # i est le dernier indice des résidentiels
    residList = projectList[:i]
    utilList = projectList[i:]

    listWeightsR = calculWeight.weight(residList)


    while simulation_not_stop:
        initialization = True
        city = Grid(rows, columns)
        # Création des listes de projets résidentiels et utilitaires:
        # ici on charge dans projectList les projets présents dans le fichier
        while initialization:
            firstProjectResid = calculWeight.selectRandResid(residList, listWeightsR)
            firstProjectUtil = calculWeight.selectRandUtil(utilList, projectList, maximumDistance, city.buildedU, city.buildedR)

            residBuildable = city.isBuildable(firstProjectResid, (rows//2 - firstProjectResid.rows//2, columns//2 ))
            utilBuildable = city.isBuildable(firstProjectUtil, (rows//2 - firstProjectUtil.rows//2, columns//2 - firstProjectUtil.columns))

            # Si on arrive à placer les 2 bâtiments, on les place et on passe au placement unitaire
            if residBuildable and utilBuildable:
                city.buildProject(firstProjectResid, (rows//2 - firstProjectResid.rows//2, columns//2 ))
                city.buildProject(firstProjectUtil, (rows//2 - firstProjectUtil.rows//2, columns//2 - firstProjectUtil.columns))

                initialization = False
        while nbErreursCourant < nbErreurs: # Condition d'arrêt : après un certains nombre d'érreurs consecutives
            # sélection aléatoire de coordonnées et de type de batiment
            numProjectRand = random.randint(0, len(projectList) - 1)
            numColsRand = random.randint(0, columns)
            numRowsRand = random.randint(0, rows)

            if city.isBuildable(projectList[numProjectRand], (numRowsRand, numColsRand)):
                # Si le projet peut-être placé alors nous le plaçons aux coordonnées définie aléatoirement.
                city.buildProject(projectList[numProjectRand], (numRowsRand, numColsRand))
            else : 
                nbErreursCourant += 1
        score_simu = getGridScore(projectList, maximumDistance, city.buildedR, city.buildedU, False)

        nbErreursCourant = 0
        if score_max < score_simu:
            score_max = score_simu
            best_city = copy.deepcopy(city)
        sys.stdout.write('Simulations en cours ... %3d%%\r' % int((n/nbSimus)*100))
        n += 1
        if n == nbSimus:
            simulation_not_stop = False

    if inputs.rows == 1000:
        print("duplication de la grille par 100")
        finalCity = duplicate(best_city, 10, 10, projectList)
    else:
        finalCity = best_city

    print("nombre de batiments résidentiels : ", len(finalCity.buildedR), " / utilitaires : ", len(finalCity.buildedU), "\n")
    print("Calcul du score ...")
    score_max = getGridScore(projectList, maximumDistance, finalCity.buildedR, finalCity.buildedU, False)
    inputs.close()
    print("Score final : {}".format(score_max))
    print("THE END !")
    out = OutManager("{} {}".format(Const.FILE_NAMES[choixExercice], time.strftime('%d-%m-%Y %H-%M-%S')))

    out.writeScore(score_max)
    out.writeProjects(getBuildedNums(finalCity.buildedR + finalCity.buildedU, trueNum))
    # printGrid(finalCity, projectList) # Affichage avec TKinter
    Grid.show(finalCity) # Affiche la grille dans la console


def duplicate(city, nbDupliX, nbDupliY, projectList):
    """
    Fonction permettant de dupliquer une grille le nombre de fois demandé

    :param city: (Grid) grille à dupliquer
    :param nbDupliX: (int) nombre de duplications en X
    :param nbDupliY: (int) nombre de duplications en Y
    :param projectList: (list[Project]) list des projets de l'input
    :return grid: (Grid) grille finale dupliquée
    """
    grid = Grid(city.grows*nbDupliX, city.gcolumns*nbDupliY)

    for i in range(nbDupliX):
        for j in range(nbDupliY):
            for k in range(len(city.buildedR)):
                proj = projectList[city.buildedR[k][Const.NUM_PROJ]]
                newBuildedR = copy.deepcopy(city.buildedR[k])
                newBuildedR[Const.COORD_PROJ] = (newBuildedR[Const.COORD_PROJ][0] + city.grows*i, newBuildedR[Const.COORD_PROJ][1] + city.gcolumns*j)
                grid.buildProject(proj, newBuildedR[Const.COORD_PROJ])

            for k in range(len(city.buildedU)):
                proj = projectList[city.buildedU[k][Const.NUM_PROJ]]
                newBuildedU = copy.deepcopy(city.buildedU[k])
                newBuildedU[Const.COORD_PROJ] = (newBuildedU[Const.COORD_PROJ][0] + city.grows*i, newBuildedU[Const.COORD_PROJ][1] + city.gcolumns*j)
                grid.buildProject(proj, newBuildedU[Const.COORD_PROJ])

    return grid
