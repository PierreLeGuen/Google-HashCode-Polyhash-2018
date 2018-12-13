#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Créé le 16 Oct 2018

@author: PierreLeGuen
'''


class Project:
    """ Classe permettant de réupérer les attributs communs à tout les bâtiments du projet """
    def __init__(self, numProject, rows, columns, occupiedCells):
        """
        Constructeur de la classe Project chargeant toutes ses variables sauf les cases ocupées

        :param numProject: (int) numéro du projet (dans l'ordre de lecture du fichier normalement)
        :param rows: (int) nombre de lignes pour ce projet
        :param columns: (int) nombre de colonnes pour ce projet
        :param occupiedCells: (list[tuple[int, int]]) liste des coordonnées de cases occupées par les batiments
        """
        self.numProject = numProject
        self.rows = rows
        self.columns = columns
        self.occupiedCells = occupiedCells

    def isResid(self, resid):
        """
        méthode permettant d'identifier le type de projet

        :param resid: (bool) True si le projet est résidentiel, False sinon
        """
        return resid


class Residential(Project):
    """ Classe héritant de Project, elle s'occupe des bâtiments résidentiels """
    def __init__(self, capacity, numProject, rows, columns, occupiedCells):
        super(Residential, self).__init__(numProject, rows, columns, occupiedCells)
        self.capacity = capacity

    def isResid(self):
        return super(Residential, self).isResid(True)


class Utility(Project):
    """ Classe héritant de Project, elle s'occupe des bâtiments utilitaires """
    def __init__(self, utilType, numProject, rows, columns, occupiedCells):
        super(Utility, self).__init__(numProject, rows, columns, occupiedCells)
        self.utilType = utilType

    def isResid(self):
        return super(Utility, self).isResid(False)
