#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Créé le 10 Oct 2018

@author: UlysseGuyon
'''

import os

class ProjectParse :
    """Petite classe permettant de stocker les données d'un projet de batiment"""

    def __init__(self, numProject, isResid, rows, columns, prop):
        """
        Constructeur de la classe Project chargeant toutes ses variables sauf les cases ocupées

        :param numProject: (int) numéro du projet (dans l'ordre de lecture du fichier normalement)
        :param isResid: (bool) vrai si le batiment est de type résidentiel, faux sinon
        :param rows: (int) nombre de lignes pour ce projet
        :param columns: (int) nombre de colonnes pour ce projet
        :param prop: - (int) capacité de résidents si isResid est vrai
                     - (int) type d'utilité si isResid est faux
        """

        self.numProject = numProject
        self.isResid = isResid
        self.rows = rows
        self.columns = columns
        self.prop = prop
        self.occupiedCells = []  # il faut rajouter les cases occupées après l'initialisation

class InManager :
    """
    Classe permettant d'ouvrir un seul fichier du dossier inputs à la fois
    et d'en récupérer les données facilement
    """

    def __init__(self, fileName):
        """
        Constructeur de la classe InManager
        Ouvre un fichier qu'il faudra fermer avec la fonction close()
        Enregistre les données générales écrites sur la première ligne du fichier

        :param fileName: (str) nom simple du fichier avec son extension (.in) sans spécifier de chemin
        """

        # ouverture du fichier en mode lecture
        path = os.path.dirname(os.path.abspath(__file__))
        if len(path.split("/")) == 1:
            path = "/".join(path.split("\\"))
        absPath = "/".join(path.split("/")[:-1]) + "/inputs/" + fileName + ".in"
        self.file = open(absPath, 'r')

        # ici on lit la première ligne du fichier et on l'enregistre dans les quatre variables suivantes
        line = self.file.readline().split()

        self.rows = int(line[0])         # nombre de lignes dans la grille
        self.columns = int(line[1])      # nombre de colonnes dans la grille
        self.walkDist = int(line[2])     # distance max entre deux batiments pour compter les points
        self.nbPlans = int(line[3])      # nombre de plans de batiments

        self.project = None         # variable utilisée pour stocker les données du projet courant

    def loadNextProject(self):
        """
        Méthode chargeant dans self.project les données du prochain projet à lire dans le fichier

        :return: (bool) vrai si on a réussi à charger le projet suivant / faux si on est à la fin du fichier
        """

        # on stocke les données du projet dans line et le numéro du projet dans numProj
        line = self.file.readline().split()

        if line:

            numProj = self.project.numProject + 1 if self.project else 0

            # on stocke un nouveau projet ici
            self.project = ProjectParse(numProj, line[0] == 'R', int(line[1]), int(line[2]), int(line[3]))

            # on parcours les lignes avec i et les colonnes avec j
            for i in range(int(line[1])):

                lineCell = list(self.file.readline())  # ligne courante

                for j in range(len(lineCell)):

                    # si on trouve un '#' alors on ajoute les coordonnées (i, j) aux cases occupées par un batiment
                    if lineCell[j] == '#':
                        self.project.occupiedCells.append((i, j))

            return True

        else:
            self.project = None
            return False

    def close(self):
        """Méthode fermant le fichier ouvert par le constructeur"""
        self.file.close()


    """Les méthodes suivantes servent à acceder facilement aux paramètres de self.project"""

    def getProjNum(self):
        if self.project :
            return self.project.numProject
        else :
            print("tentative d'accès à un projet inexistant -> loadNextProject() utilisé trop de fois")
            return None

    def getProjRows(self):
        if self.project :
            return self.project.rows
        else :
            print("tentative d'accès à un projet inexistant -> loadNextProject() utilisé trop de fois")
            return None

    def getProjCol(self):
        if self.project :
            return self.project.columns
        else :
            print("tentative d'accès à un projet inexistant -> loadNextProject() utilisé trop de fois")
            return None

    def getProjProperty(self):
        if self.project :
            return self.project.prop
        else :
            print("tentative d'accès à un projet inexistant -> loadNextProject() utilisé trop de fois")
            return None

    def getProjBuildings(self):
        if self.project :
            return self.project.occupiedCells
        else :
            print("tentative d'accès à un projet inexistant -> loadNextProject() utilisé trop de fois")
            return None

    def isProjResidential(self):
        if self.project :
            return self.project.isResid
        else :
            print("tentative d'accès à un projet inexistant -> loadNextProject() utilisé trop de fois")
            return None