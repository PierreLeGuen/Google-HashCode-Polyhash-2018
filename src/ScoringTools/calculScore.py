#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Créé le 29 Oct 2018

@author: UlysseGuyon
'''


import sys
import os
sys.path.insert(0, "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-2])+"/")
import time
from src.ScoringTools.calculDist import distMan1 as manhattanOpti
from src.constants import Const


def getGridScore(listProjectIn, maxDist, buildedR, buildedU, printing):
    """
    méthode calculant le score de la grille actuelle

    :param listProjectIn: (list[Project]) liste des projets présents dans le fichier input
    :param maxDist: (int) distance maximum entre deux projets permettant de compter les points
    :param buildedR: liste des projets résidentiels construits dans la grille
    :param buildedU: liste des projets utilitaires construits dans la grille
    :return score: score calculé à partir du nombre d'habitants dans un batiment résidentiel
    """

    if printing:
        print("Calcul du score en cours ...")

    score = 0

    timePrint = not printing
    i = 0
    maxi = len(buildedR) * len(buildedU)
    t = time.clock()

    # pour chaque projet résidentiel, on regarde si il est assez proche de chaque utilitaire
    for res in buildedR:

        projectR = listProjectIn[res[Const.NUM_PROJ]]
        countTypeUtil = []  # cette liste sert à ne pas compter 2 fois le même type de batiment utilitaire

        for util in buildedU:

            # affichage et calcul du temps total pris par cette fonction
            if not timePrint:
                i += 1
                if (100 * i / maxi) >= Const.THRESH_TIME_PRINT:
                    t = (time.clock() - t) * 1000
                    m = int((t / 60) % 60) + 1
                    h = int(t / 3600)

                    print("temps approximatif estimé pour le calcul : {} heure(s) et {} minute(s) ...".format(h, m))
                    timePrint = True

            # ce n'est pas la peine d'aller plus loin dans le tests si on a déjà compté ce type d'utilitaire
            if not util[Const.CARAC_PROJ] in countTypeUtil:

                projectU = listProjectIn[util[Const.NUM_PROJ]]

                # on teste d'emblé si les deux batiments ne sont pas ostensiblement trop écartés
                if not ((res[Const.COORD_PROJ][0] - util[Const.COORD_PROJ][0] - projectU.rows > maxDist + Const.SAFE_DIST
                    or util[Const.COORD_PROJ][0] - res[Const.COORD_PROJ][0] - projectR.rows > maxDist + Const.SAFE_DIST)
                   and (res[Const.COORD_PROJ][1] - util[Const.COORD_PROJ][1] - projectU.columns > maxDist + Const.SAFE_DIST
                    or util[Const.COORD_PROJ][1] - res[Const.COORD_PROJ][1] - projectR.columns > maxDist + Const.SAFE_DIST)):

                    manTrue = manhattanOpti(projectR, res[Const.COORD_PROJ], projectU, util[Const.COORD_PROJ])

                    if manTrue <= maxDist:
                        score += res[Const.CARAC_PROJ]
                        countTypeUtil.append(util[Const.CARAC_PROJ])

    return score


def getResidScore(listProjectIn, residBuilded, maxDist, buildedU):
    """
    Fonction permettant de calculer le score d'un seul batiment résidentiel

    :param listProjectIn: (list[Project]) liste des projets présents dans le fichier input
    :param residBuilded: ([int, [int, int], int]) données du projet résidentiel construit
    :param maxDist: (int) distance maximum entre deux projets permettant de compter les points
    :param buildedU: liste des projets utilitaires construits dans la grille
    :return score: score calculé à partir du nombre d'habitants dans un batiment résidentiel
    """

    score = 0
    projectR = listProjectIn[residBuilded[Const.NUM_PROJ]]
    countTypeUtil = []  # cette liste sert à ne pas compter 2 fois le même type de batiment utilitaire

    for util in buildedU:

        if util[Const.CARAC_PROJ] not in countTypeUtil:

            projectU = listProjectIn[util[Const.NUM_PROJ]]

            # on teste d'emblé si les deux batiments ne sont pas ostensiblement trop écartés
            if not ((residBuilded[Const.COORD_PROJ][0] - util[Const.COORD_PROJ][0] - projectU.rows > maxDist + 2
                or util[Const.COORD_PROJ][0] - residBuilded[Const.COORD_PROJ][0] - projectR.rows > maxDist + 2)
               and (residBuilded[Const.COORD_PROJ][1] - util[Const.COORD_PROJ][1] - projectU.columns > maxDist + 2
                or util[Const.COORD_PROJ][1] - residBuilded[Const.COORD_PROJ][1] - projectR.columns > maxDist + 2)):

                manTrue = manhattanOpti(projectR, residBuilded[Const.COORD_PROJ], projectU, util[Const.COORD_PROJ])

                if manTrue <= maxDist:
                    score += residBuilded[Const.CARAC_PROJ]
                    countTypeUtil.append(util[Const.CARAC_PROJ])

    return score


def getUtilScore(listProjectIn, util, maxDist, buildedR, buildedU):
    """
    Fonction permettant de calculer le score potentiellement ajouté par un nouveau batiment utilitaire

    :param listProjectIn: (list[Project]) liste des projets présents dans le fichier input
    :param util: ([int, [int, int], int]) nouvel utilitaire dont on calcule le score potentiel
    :param maxDist: (int) distance maximum entre deux projets permettant de compter les points
    :param buildedR: liste des projets résidentiels construits dans la grille
    :param buildedU: liste des projets utilitaires construits dans la grille
    :return score: (int) score potentiel calculé pour cet utilitaire
    """

    score = 0
    projectU = listProjectIn[util[Const.NUM_PROJ]]

    for resid in buildedR:

        projectR = listProjectIn[resid[Const.NUM_PROJ]]

        # on teste d'emblé si les deux batiments ne sont pas ostensiblement trop écartés
        if not ((resid[Const.COORD_PROJ][0] - util[Const.COORD_PROJ][0] - projectU.rows > maxDist + 2
            or util[Const.COORD_PROJ][0] - resid[Const.COORD_PROJ][0] - projectR.rows > maxDist + 2)
           and (resid[Const.COORD_PROJ][1] - util[Const.COORD_PROJ][1] - projectU.columns > maxDist + 2
            or util[Const.COORD_PROJ][1] - resid[Const.COORD_PROJ][1] - projectR.columns > maxDist + 2)):

            countTypeUtil = typeUtilUsed(listProjectIn, resid, maxDist, buildedU)
            manTrue = manhattanOpti(projectR, resid[Const.COORD_PROJ], projectU, util[Const.COORD_PROJ])

            if (util[Const.CARAC_PROJ] not in countTypeUtil) and manTrue <= maxDist:
                score += resid[Const.CARAC_PROJ]

    return score


def typeUtilUsed(listProjectIn, resid, maxDist, buildedU):
    """
    Fonction permettant de donner la liste des types d'utilitaires
    qui sont assez proche d'un résidentiel en particulier

    :param listProjectIn: (list[Project]) liste des projets présents dans le fichier input
    :param resid: ([int, [int, int], int]) projet résidentiel dont on cherche la liste des types d'utilitaires utilisés
    :param maxDist: (int) distance maximum entre deux projets permettant de compter les points
    :param buildedU: liste des projets utilitaires construits dans la grille
    :return countTypeUtil: (list[int]) liste des types d'utilitaires utilisés pour un projet résidentiel
    """

    projectR = listProjectIn[resid[Const.NUM_PROJ]]
    countTypeUtil = []  # cette liste sert à ne pas compter 2 fois le même type de batiment utilitaire

    for util in buildedU:

        if util[Const.CARAC_PROJ] not in countTypeUtil:

            projectU = listProjectIn[util[Const.NUM_PROJ]]

            # on teste d'emblé si les deux batiments ne sont pas ostensiblement trop écartés
            if not ((resid[Const.COORD_PROJ][0] - util[Const.COORD_PROJ][0] - projectU.rows > maxDist + 2
                or util[Const.COORD_PROJ][0] - resid[Const.COORD_PROJ][0] - projectR.rows > maxDist + 2)
               and (resid[Const.COORD_PROJ][1] - util[Const.COORD_PROJ][1] - projectU.columns > maxDist + 2
                or util[Const.COORD_PROJ][1] - resid[Const.COORD_PROJ][1] - projectR.columns > maxDist + 2)):

                manTrue = manhattanOpti(projectR, resid[Const.COORD_PROJ], projectU, util[Const.COORD_PROJ])

                if manTrue <= maxDist:
                    countTypeUtil.append(util[Const.CARAC_PROJ])

    return countTypeUtil