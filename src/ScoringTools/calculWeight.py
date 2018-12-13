#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Créé le 9 Nov 2018

@author: SachaWanono
'''

import random
import copy
import sys
import os
sys.path.insert(0, "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-2])+"/")
from src.constants import Const
from src.project import *
from src.ScoringTools.calculScore import typeUtilUsed


def weight(listProjects):
    """
    Fonction qui calcule le poids de chaque projet résidentiel d'une liste et retourne une liste constituée des poids

    :param listProjects: (list[Residential]) liste de projets pour lesquels on veut calculer le poids
    :param listWeights: (list[int]) liste des poids que l'on vient de calculer
    """

    nbProjects = len(listProjects)
    listWeights = []

    for i in range(nbProjects):
        # on récupère les caractéristiques du projet
        rows = listProjects[i].rows
        columns = listProjects[i].columns
        capacity = listProjects[i].capacity

        # on calcule le poids et l'ajoute à listWeights
        weight = int(abs(capacity**2 + Const.LIMIT_SIZE_WEIGHT/float(rows*columns)))
        listWeights.append(weight)

    # ensuite on s'assure qu'aucun poids n'est égal
    for i in range(nbProjects):
        equalWeights = []

        for j in range(nbProjects):
            if listWeights[i] == listWeights[j]:
                equalWeights.append(j)

        for k in range(len(equalWeights)):
            listWeights[equalWeights[k]] += float(k)/float(len(equalWeights))

    return listWeights


def weightUtil(listUtil, listProjectIn, maxDist, buildedU, buildedR):
    """
    Fonction permettant de calculer le poids de chaque projet utilitaire et qui les renvoie dans une liste
    Cette fonction possède une complexité élevée, à ne pas répéter trop de fois

    :param listUtil: (list[Utility]) liste de projets pour lesquels on veut calculer le poids
    :param listProjectIn: (list[Project]) liste des projets présents dans le fichier input
    :param maxDist: (int) distance maximum entre deux projets permettant de compter les points
    :param buildedR: liste des projets résidentiels construits dans la grille
    :param buildedU: liste des projets utilitaires construits dans la grille
    :return listWeights: (list[int]) liste des poids que l'on vient de calculer
    """

    nbUtils = len(listUtil)
    listWeights = []

    for i in range(nbUtils):
        # on récupère les caractéristiques du projet
        rows = listUtil[i].rows
        columns = listUtil[i].columns
        type = listUtil[i].utilType

        # on va calculer un coef d'utilité en fonct° de si ce type d'utilitaire est déjà beaucoup compté dans la grille
        countUsefull = 0
        countUseless = 0

        for resid in buildedR:
            if type in typeUtilUsed(listProjectIn, resid, maxDist, buildedU):
                countUseless += 1
            else:
                countUsefull += 1

        coef = float(countUsefull)/float(countUsefull + countUseless + 1)

        listWeights.append(coef * Const.LIMIT_SIZE_WEIGHT / float(rows * columns))

    # ensuite on s'assure qu'aucun poids n'est égal
    for i in range(nbUtils):
        equalWeights = []

        for j in range(nbUtils):
            if listWeights[i] == listWeights[j]:
                equalWeights.append(j)

        for k in range(len(equalWeights)):
            listWeights[equalWeights[k]] += float(k)/float(len(equalWeights))

    return listWeights


def selectRandResid(listResid, listWeights):
    """
    Fonction permettant de sélectionner "aléatoirement" un projet parmis une liste de projets pondérés

    :param listProjects: (list[Residential/Utility]) liste des projets résidentiels du fichier input
    :return listProjects[j]: (Residential/Utility) projet sélectionné
    """

    listWeightSort = copy.deepcopy(listWeights)
    listWeightSort.sort()

    totalWeight = sum(listWeightSort)

    rand = random.random()*totalWeight

    i = 0
    sumWeight = 0.0
    while sumWeight < rand and i < len(listWeightSort) - 1:
        sumWeight += float(listWeightSort[i])
        i += 1

    j = 0
    while listWeights[j] != listWeightSort[i] and j < len(listWeightSort) - 1:
        j += 1

    return listResid[j]


def selectRandUtil(listUtil, listProjectIn, maxDist, buildedU, buildedR):
    """
    Fonction permettant de sélectionner "aléatoirement" un projet parmis une liste de projets pondérés

    :param listProjects: (list[Utility]) liste des projets utilitaires du fichier input
    :return listProjects[j]: (Utility) projet sélectionné
    """

    listWeights = weightUtil(listUtil, listProjectIn, maxDist, buildedU, buildedR)
    listWeightSort = copy.deepcopy(listWeights)
    listWeightSort.sort()

    totalWeight = sum(listWeightSort)

    rand = random.random()*totalWeight

    i = 0
    sumWeight = 0.0
    while sumWeight < rand and i < len(listWeightSort) - 1:
        sumWeight += float(listWeightSort[i])
        i += 1

    j = 0
    while listWeights[j] != listWeightSort[i] and j < len(listWeightSort) - 1:
        j += 1

    return listUtil[j]