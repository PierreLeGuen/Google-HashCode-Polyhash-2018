#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Créé le 12 Nov 2018

@author: UlysseGuyon
'''


class Const:
    """
    Classe regroupant les constantes utiles de chaque module

    pour l'importer depuis un sous-package, il faut écrire ces lignes en début de module :
    import sys
    import os
    sys.path.insert(0, "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-2]) + "/")
    from src.constants import Const
    """

    # coef associé à la taille du batiment dans l'équation du poids
    LIMIT_SIZE_WEIGHT = 50.0

    # tuple signifiant une case vide dans la grille
    GRID_EMPTY_TUPLE = (-1, -1)

    # noms des fichiers à utiliser dans les In/Out Managers
    FILE_NAMES = ("a_example", "b_short_walk", "c_going_green", "d_wide_selection", "e_precise_fit", "f_different_footprints", "g_test_ulysse", "h_test_pierre")

    # seuil à partir duquel on peut afficher le temps de calcul du score
    THRESH_TIME_PRINT = 0.1

    # à ajouter à la distance max quand on détermine une zone au dela de laquelle on ne teste plus de calcul de distance
    SAFE_DIST = 2

    # dans les listes comme buildedR/U, à utiliser en indice pour obtenir ce que l'on veut du projet
    NUM_PROJ = 0
    COORD_PROJ = 1
    CARAC_PROJ = 2

    # constantes correspondant à la bordure de projet sélectionnée
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3