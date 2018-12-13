#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Créé le 30 Oct 2018

@author: UlysseGuyon
'''

from src.project import *
from src.constants import Const


def projectListBuilder(inputs):
    """
    Fonction retournant une liste réduite des projets présents dans le fichier .in
    elle enlève les redondances et les projets résidentiels dont la capacité est inferieure
    à un autre projet structurellement égal

    :param inputs: (InManager) variable permettant d'accéder au fichier .in
    :return listRes: (list[Project]) liste de projets renvoyés, à utiliser pour la construction de grille
    :return trueNum: (list[int]) list des numéros de projet originaux à sauvegarder pour l'output
    """

    projectList = []
    trueNum = []

    reading = inputs.loadNextProject()
    while reading:

        # ici on construit la variable projet à partir des données lues dans le fichier .in
        if inputs.isProjResidential() :
            p = Residential(inputs.getProjProperty(), inputs.getProjNum(), inputs.getProjRows(), inputs.getProjCol(), inputs.getProjBuildings())
        else:
            p = Utility(inputs.getProjProperty(), inputs.getProjNum(), inputs.getProjRows(), inputs.getProjCol(), inputs.getProjBuildings())

        # ici on test si ce n'est pas un projet redondant
        exists = False
        for test in projectList:
            if isinstance(p, type(test)):
                if p.isResid():
                    if p.occupiedCells == test.occupiedCells and p.capacity == test.capacity:
                        exists = True
                else:
                    if p.occupiedCells == test.occupiedCells and p.utilType == test.utilType:
                        exists = True
        if not exists:
            projectList.append(p)

        reading = inputs.loadNextProject()

    # ici on test pour chaque projet résidentiel si il en existe un équivalent mais avec une meilleur capacité
    listRes = []
    for p in projectList:
        ok = True
        for test in projectList:
            if p.occupiedCells == test.occupiedCells and test.isResid() and p.isResid():
                if p.capacity < test.capacity:
                    ok = False
        if ok:
            listRes.append(p)

    for i in range(len(listRes)):
        trueNum.append(listRes[i].numProject)
        listRes[i].numProject = i

    return listRes, trueNum

def getBuildedNums(builded, trueNum):
    """
    Fonction permettant de rendre les bon numéros de projets pour l'output

    :param builded: buildedR et buildedU de la grille finale
    :param trueNum: (list[int]) trueNum renvoyé par buildProjectList
    :return builded: variable builded mise à jour
    """

    for i in range(len(builded)):
        builded[i][Const.NUM_PROJ] = trueNum[builded[i][Const.NUM_PROJ]]

    return builded
