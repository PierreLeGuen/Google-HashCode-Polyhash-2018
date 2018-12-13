#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Créé le 17 Oct 2018

@author: UlysseGuyon
'''
import sys
import os
sys.path.insert(0,"/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-2])+"/")
from src.ScoringTools.cellSelectors import *
from src.constants import Const


def distMin(listCo1, listCo2):
    """
    fonction trouvant la distance minimum existant entre deux listes de cases

    :param listCo1: (list[tuple[int, int]]) première liste de coordonnées de points
    :param listCo2: (list[tuple[int, int]]) deuxième liste de coordonnées de points
    :return minDist: distance de manhattan minimale trouvée
    """

    minDist = None
    for coord1 in listCo1:
        for coord2 in listCo2:
            # pour chaque case de chaque liste, on calcule la distance de manhattan entre les deux
            dist = abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

            # si cette distance est plus petite que celles trouvées avant, on la retient
            if minDist is None:
                minDist = dist
            elif minDist > dist:
                minDist = dist

    return minDist


def distManIter(project1, coords1, project2, coords2) :
    """
    Fonction retournant la plus petite distance de manhattan entre deux projets sans se soucier de l'optimisation

    cette fonction est correcte mais non optimisée
    à utiliser tant qu'aucune fonction optimisée n'a été trouvée

    :param project1: (Project) variable du premier projet analysé
    :param coords1: (tuple[int, int]) coordonnées haut-gauche du premier projet
    :param project2: (Project) variable du deuxième projet analysé
    :param coords2: (tuple[int, int]) coordonnées haut-gauche du deuxème projet
    :return dist: distance de manhattan minimale trouvée
    """

    select1 = []
    select2 = []
    for i in project1.occupiedCells:
        select1.append(list(i))
    for i in project2.occupiedCells:
        select2.append(list(i))

    for i in range(len(select1)):
        select1[i][0] += coords1[0]
        select1[i][1] += coords1[1]
    for i in range(len(select2)):
        select2[i][0] += coords2[0]
        select2[i][1] += coords2[1]

    dist = distMin(select1, select2)

    return dist


def getRealCoords(listCoords, gridCoords):
    """
    Fonction renvoyant les coordonnées réelles de toutes les cases d'un projet sur la grille
    à partir de ses coordonnées en haut à gauche et de ses cases à coordonnées relatives

    :param listCoords: (list[tuple[int, int]]) liste des coordonnées relatives de chaque case du projet
    :param gridCoords: (tuple[int, int]) coordonnées en haut à gauche du projet
    :return listGridCoords: coordonnées réelles de chaque case
    """

    listGridCoords = []

    for co in listCoords :
        listGridCoords.append((co[0] + gridCoords[0], co[1] + gridCoords[1]))

    return listGridCoords


def distMan1(project1, coords1, project2, coords2):
    """
    Fonction optimisant la rechèrche d'une distance de manhattan entre deux projets
    en fonction de leurs configurations l'un par rapport à l'autre

    cette fonction est correcte et jusqu'à 5 fois plus rapide que le calcul itératif

    :param project1: (Project) variable du premier projet analysé
    :param coords1: (tuple[int, int]) coordonnées haut-gauche du premier projet
    :param project2: (Project) variable du deuxième projet analysé
    :param coords2: (tuple[int, int]) coordonnées haut-gauche du deuxème projet
    :return dist: distance de manhattan minimale trouvée
    """

    dist = 0

    # listes des coordonnées de chaque coin des deux projets
    # dans l'ordre : haut-gauche / bas-gauche / bas-droite / haut-droite
    co1 = [coords1, (coords1[0] + project1.rows, coords1[1]),
           (coords1[0] + project1.rows, coords1[1] + project1.columns), (coords1[0], coords1[1] + project1.columns)]
    co2 = [coords2, (coords2[0] + project2.rows, coords2[1]),
           (coords2[0] + project2.rows, coords2[1] + project2.columns), (coords2[0], coords2[1] + project2.columns)]

    if co1[0][0] > co2[2][0] and co1[0][1] > co2[2][1] :
        # si la coord haut-gauche projet 1 est en bas-droite de la coord bas-droite projet 2
        select1 = getRealCoords(getEdges(project1, True, True), coords1)
        select2 = getRealCoords(getEdges(project2, False, False), coords2)

        dist = distMin(select1, select2)
    elif co1[1][0] < co2[3][0] and co1[1][1] > co2[3][1] :
        # si la coord bas-gauche projet 1 est en haut-droite de la coord haut-droite projet 2
        select1 = getRealCoords(getEdges(project1, False, True), coords1)
        select2 = getRealCoords(getEdges(project2, True, False), coords2)

        dist = distMin(select1, select2)
    elif co1[2][0] < co2[0][0] and co1[2][1] < co2[0][1] :
        # si la coord bas-droite projet 1 est en haut-gauche de la coord haut-gauche projet 2
        select1 = getRealCoords(getEdges(project1, False, False), coords1)
        select2 = getRealCoords(getEdges(project2, True, True), coords2)

        dist = distMin(select1, select2)
    elif co1[3][0] > co2[1][0] and co1[3][1] < co2[1][1] :
        # si la coord haut-droite projet 1 est en bas-gauche de la coord bas-gauche projet 2
        select1 = getRealCoords(getEdges(project1, True, False), coords1)
        select2 = getRealCoords(getEdges(project2, False, True), coords2)

        dist = distMin(select1, select2)
    elif co1[0][0] > co2[2][0] :
        # si le projet 1 est en dessous du projet 2
        select1 = getRealCoords(getBorder(project1, Const.UP), coords1)
        select2 = getRealCoords(getBorder(project2, Const.DOWN), coords2)

        dist = distMin(select1, select2)
    elif co1[2][1] < co2[0][1] :
        # si le projet 1 est à gauche du projet 2
        select1 = getRealCoords(getBorder(project1, Const.RIGHT), coords1)
        select2 = getRealCoords(getBorder(project2, Const.LEFT), coords2)

        dist = distMin(select1, select2)
    elif co1[2][0] < co2[0][0] :
        # si le projet 1 est en haut du projet 2
        select1 = getRealCoords(getBorder(project1, Const.DOWN), coords1)
        select2 = getRealCoords(getBorder(project2, Const.UP), coords2)

        dist = distMin(select1, select2)
    elif co1[0][1] > co2[2][1] :
        # si le projet 1 est à droite du projet 2
        select1 = getRealCoords(getBorder(project1, Const.LEFT), coords1)
        select2 = getRealCoords(getBorder(project2, Const.RIGHT), coords2)

        dist = distMin(select1, select2)
    else :
        # cas général utilisation des bordures de deux projets  !!! : peut-être non optimal
        select1 = getRealCoords(getFullBorder(project1), coords1)
        select2 = getRealCoords(getFullBorder(project2), coords2)

        dist = distMin(select1, select2)

    return dist