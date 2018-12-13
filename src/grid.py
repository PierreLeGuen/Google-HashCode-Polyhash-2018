#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Créé le 16 Oct 2018

@author: LouisCanu
'''


from src.constants import Const

class Grid :
    """ classe stockant la grille de la ville """

    def __init__ (self, grows, gcolumns):
        """
        Constructeur de la grille

        :param rows: (int) nombre de lignes de la grille
        :param columns: (int) nombre de colonnes de la grille
        """
        self.grows = grows
        self.gcolumns = gcolumns

        self.grid = []  # grille de construction représentant la ville
        self.nbProject = 0  # indice du projet à écrire dans la grille lors de sa construction

        self.buildedR = []  # liste des projets résidentiels construits dans la grille
        self.buildedU = []  # liste des projets utilitaires construits dans la grille
                            # (len(self.buildedR) + len(self.buildedU) = nombre de projets construits)
                            # contiennent le num de projet, ses coords en haut à gauche et sa caractéristique

        for i in range(grows):
            self.grid.append([])
            for j in range(gcolumns):
                self.grid[i].append(Const.GRID_EMPTY_TUPLE)

    def isBuildable (self, project, coords):
        """
        méthode vérifiant si on peut construire un projet aux coordonnées données

        :param project: (class) projet courant de construction
        :param coords: (tuple) coordonnées où l'on veut construire le projet

        :return check: (bool) vrai si le projet peut être construit, faux sinon
        """
        check = True

        # si c'est en dehors de la grille, on ne peut pas construire
        if coords[0] + project.rows > self.grows:
            check = False
        elif coords[1] + project.columns > self.gcolumns:
            check = False
        else:
            # si une des cases qu'on veut construire est déjà occupée, on ne peut pas construire
            for i in project.occupiedCells:
                if self.grid[i[0] + coords[0]][i[1] + coords[1]] != Const.GRID_EMPTY_TUPLE:
                    check = False

        return check

    def buildProject (self, project, coords):
        """
        méthode construisant un projet dans la grille grid.

        :param project: (class) projet courant de construction
        :param coords: (tuple) coordonnées où l'on construit le projet
        """
        if self.isBuildable(project, coords):
            # à chaque nouveau projet construit, on associe un nouveau numéro dans la grille : len(self.builded)

            if project.isResid():
                self.buildedR.append([project.numProject, coords, project.capacity])
            else:
                self.buildedU.append([project.numProject, coords, project.utilType])

            for i in project.occupiedCells :
                self.grid[i[0] + coords[0]][i[1] + coords[1]] = (len(self.buildedR) + len(self.buildedU), project.numProject)

    def show(self):
        """ méthode permettant d'afficher la grille dans le terminal """
        for i in range(len(self.grid)):
            line = []
            for j in range(len(self.grid[0])):
                line.append(self.grid[i][j][0])
            print(line)

    def showNumProject(self):
        """ méthode permettant d'afficher la grille dans le terminal (différement) """
        for i in range(len(self.grid)):
            line = []
            for j in range(len(self.grid[0])):
                line.append(self.grid[i][j][1])
            print(line)
