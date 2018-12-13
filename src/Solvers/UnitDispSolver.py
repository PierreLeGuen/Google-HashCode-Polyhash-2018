#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Créé le 14 Nov 2018

@author: SachaWanono
'''
import sys
import os
sys.path.insert(0, "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-2])+"/")
from src.InOutManager.inputmanager import InManager
from src.InOutManager.outputmanager import OutManager
from src.ScoringTools.calculScore import *
from src.projectDisplay import *
from src.projectListBuilder import projectListBuilder
from src.projectListBuilder import getBuildedNums
from src.project import *
from src.grid import Grid
from src.ScoringTools.calculWeight import *
import random
import time
from src.constants import Const


def placementUnitOpti(nbErreurs, choixExercice, nbSimu):
    """
    Fonction permettant de remplir la matrice "city plan" bâtiment par bâtiment en
    optimisant le score.

    :param nbErreurs: (int) nombre d'erreurs maximale autorisée
    :param choixExercice: (int) choisir parmi les "inputs" fournis par Google. 0->a_*, 5->f_*
    :param nbSimu: (int) nombre de simulation à effectuer pour obtenir la meilleur grille
    """

    print("Placement Unitaire Optimisé lancé !")
    print("Création de grille lancée à : " + time.strftime('%H:%M:%S'))
    print("chargement des projets du fichier " + Const.FILE_NAMES[choixExercice] + ".in ...")
    inputs = InManager(Const.FILE_NAMES[choixExercice])
    maximumDistance = inputs.walkDist

    # ici on charge dans projectList les projets présents dans le fichier
    projectList, trueNum = projectListBuilder(inputs)
    i = 0
    while isinstance(projectList[i], type(projectList[0])):
        i += 1
    # i est le dernier indice des résidentiels
    residList = projectList[:i]
    utilList = projectList[i:]

    print("fichiers chargés\n\nconstructions des batiments ...")

    listWeightsR = weight(residList)

    bestCity = None
    bestCityScore = 0
    for simuCourrante in range(nbSimu):
        # on effectue un certain nombre de simulations sur city et on garde la meilleure dans bestCity

        if inputs.rows == 1000:
            city = Grid(inputs.rows//10, inputs.columns//10)
        else:
            city = Grid(inputs.rows, inputs.columns)

        # on construit les deux premiers batiments au milieu de la map
        initialization = True
        while initialization:

            firstProjectResid = selectRandResid(residList, listWeightsR)
            firstProjectUtil = selectRandUtil(utilList, projectList, maximumDistance, city.buildedU, city.buildedR)

            residRandCo = (random.randint(0, city.grows - firstProjectResid.rows), random.randint(0, city.gcolumns - firstProjectResid.columns))
            utilRandCo = (random.randint(0, city.grows - firstProjectResid.rows), random.randint(0, city.gcolumns - firstProjectResid.columns))

            residBuildable = city.isBuildable(firstProjectResid, residRandCo)
            utilBuildable = city.isBuildable(firstProjectUtil, utilRandCo)

            # Si on arrive à placer les 2 bâtiments, on les place et on passe au placement unitaire
            if residBuildable and utilBuildable:
                city.buildProject(firstProjectResid, residRandCo)
                city.buildProject(firstProjectUtil, utilRandCo)

                initialization = False

        # on construit le plus de batiment possible avec le meilleur score possible
        constructing = True
        while constructing:

            bestCoords = (-1, -1)
            bestScore = 0

            constructR = (True if random.randint(0, 1) == 1 else False)
            proj = (selectRandResid(residList, listWeightsR) if constructR else utilList[random.randint(0, len(utilList) - 1)])

            # pour le projet choisi, on teste un certain nombre de coordonnées aléatoires et on garde celles qui rapportent le plus de score
            for nbTests in range(nbErreurs):
                curentCoords = (random.randint(0, city.grows - proj.rows), random.randint(0, city.gcolumns - proj.columns))
                if city.isBuildable(proj, curentCoords):
                    if constructR:
                        curentScore = getResidScore(projectList, (proj.numProject, curentCoords, proj.capacity), maximumDistance, city.buildedU)
                    else:
                        curentScore = getUtilScore(projectList, (proj.numProject, curentCoords, proj.utilType), maximumDistance, city.buildedR, city.buildedU)

                    if curentScore > bestScore:
                        bestScore = curentScore
                        bestCoords = curentCoords

            if bestCoords != (-1, -1):
                city.buildProject(proj, bestCoords)
            else:
                constructing = False

        scoreSimu = getGridScore(projectList, maximumDistance, city.buildedR, city.buildedU, False)
        if scoreSimu > bestCityScore:
            bestCity = copy.deepcopy(city)
            bestCityScore = scoreSimu

    finalCity = duplicate(bestCity, 10, 10, projectList)

    inputs.close()

    print("limite de {} simulations atteinte".format(nbSimu) + " : grille construite")

    out = OutManager("{} {}".format(Const.FILE_NAMES[choixExercice], time.strftime('%d-%m-%Y %H-%M-%S')))

    # city.showNumProject() # Prend beaucoup de ressources.

    print("nombre de batiments résidentiels : ", len(finalCity.buildedR), " / utilitaires : ", len(finalCity.buildedU), "\n")

    # on calcule le score et on l'écrit dans un fichier et dans le terminal
    score = getGridScore(projectList, maximumDistance, finalCity.buildedR, finalCity.buildedU, True)
    out.writeScore(score)
    out.writeProjects(getBuildedNums(finalCity.buildedR + finalCity.buildedU, trueNum))
    print("score = ", score)
    # printGrid(city, projectList) # Affichage avec TKinter
    Grid.show(city) # Affiche la grille dans la console


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