#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Créé le 29 Oct 2018

@author: UlysseGuyon
'''

import sys
import os
sys.path.insert(0, "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-2])+"/")
from src.constants import Const


def getEdges(project, up, left):
    """
    Fonction renvoyant les cases d'un projet qui sont les plus proches
    d'un des coins du rectangle entourant ce projet

    :param project: (Project) variable projet contenant les cases occupées
    :param up: (bool) vrai si le coin voulu est en haut du rectangle, faux sinon
    :param left: (bool) vrai si le coin voulu est à gauche du rectangle, faux sinon
    :return coords: (list[tuple[int, int]]) liste des coordonnées des cases retenues après sélection
    """

    coords = []
    maxSum = 0

    for i in range(len(project.occupiedCells)):
        # pour toutes les cases occupées, on fait la somme de ses deux coordonnées (modifiées en fonction du coin)
        sum = (project.rows - project.occupiedCells[i][0] if up else project.occupiedCells[i][0])\
              + (project.columns - project.occupiedCells[i][1] if left else project.occupiedCells[i][1])

        if sum >= maxSum :
            # si cette somme est plus grande que la somme max précédemment trouvée,
            # c'est qu'elle est plus proche du coin cherché
            if sum > maxSum :
                maxSum = sum
                coords = []
            coords.append(project.occupiedCells[i])

    return coords


def getBorder(project, border):
    """
    Fonction renvoyant les cases d'un projet qui sont les plus proches
    d'un des côtés du rectangle entourant ce projet;
    on en sélectionne une seule pour chaque ligne ou une seule pour chaque colonne selon la bordure

    :param project: (Project) variable projet contenant les cases occupées
    :param border: (int) bordure sélectionnée : 0 = haut / 1 = gauche / 2 = bas / 3 = droite
                                            je me suis peut-être embrouillé sur la ces valeurs. Ulysse
    :return coords: (list[tuple[int, int]]) liste des coordonnées des cases retenues après sélection
    """

    coords = []

    for i in range(project.rows if border == Const.LEFT or border == Const.RIGHT else project.columns):
        # avec i on parcours les colonnes si on cherche la bordure du haut ou du bas, on parcours les lignes sinon
        ok = False

        # on initialise j à 0 si on cherche la bordure du haut ou de gauche, au max sinon
        j = 0 if border == Const.UP or border == Const.LEFT else (project.columns - 1 if border == Const.RIGHT else project.rows - 1)
        while not ok :
            # on parcours la ligne ou la colonne jusqu'à trouver la première case occupée et on l'ajoute a coords
            currentCo = (i, j) if border == Const.LEFT or border == Const.RIGHT else (j, i)
            if currentCo in project.occupiedCells :
                ok = True
                coords.append(currentCo)

            j += 1 if border == Const.LEFT or border == Const.UP else -1

            if abs(j) > project.rows and abs(j) > project.columns:
                print("erreur : bug dans getBorder()")
                ok = True

    return coords


def getFullBorder(project):
    """
    Fonction renvoyant toutes les cases externes d'un projet

    :param project: (Project) variable projet contenant les cases occupées
    :return coords: (list[tuple[int, int]]) liste des coordonnées des cases retenues après sélection
    """

    coords = []

    # on sélectionne d'abords toutes les cases sur les bords du rectangle entourant le projet
    for i in range(project.rows):

        # bord gauche
        if (i, 0) in project.occupiedCells and (i, 0) not in coords:
            coords.append((i, 0))

        # bord droite
        if (i, project.columns - 1) in project.occupiedCells and (i, project.columns - 1) not in coords:
            coords.append((i, project.columns - 1))

    for i in range(project.columns):

        # bord haut
        if (0, i) in project.occupiedCells and (0, i) not in coords:
            coords.append((0, i))

        # bord bas
        if (project.rows - 1, i) in project.occupiedCells and (project.rows - 1, i) not in coords:
            coords.append((project.rows - 1, i))

    # ensuite on sélectionne toutes les cases exterieures du projet (touchant une case non construite)
    for i in range(project.rows):
        for j in range(project.columns):
            if (i, j) not in project.occupiedCells:
                if (i - 1, j) in project.occupiedCells and (i - 1, j) not in coords:
                    coords.append((i - 1, j))
                if (i + 1, j) in project.occupiedCells and (i + 1, j) not in coords:
                    coords.append((i + 1, j))
                if (i, j - 1) in project.occupiedCells and (i, j - 1) not in coords:
                    coords.append((i, j - 1))
                if (i, j + 1) in project.occupiedCells and (i, j + 1) not in coords:
                    coords.append((i, j + 1))

    return coords