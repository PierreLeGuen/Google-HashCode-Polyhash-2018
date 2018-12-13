#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Créé le 9 Nov 2018

@author: LouisCanu
'''

import sys
import os
sys.path.insert(0, "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-2])+"/")
from tkinter import *


def printGrid(grid, projectList):
    """
    Fonction permettant l'affichage graphique de la grille créée

    :param grid: (Grid) objet grille créé précédement dans l'execution du programme
    :param projectList: (list[Project]) liste des projets lus dans le fichier input
    """
    window = Tk()
    canvas = Canvas(window, width=grid.gcolumns, height=grid.grows)
    canvas.pack()

    for i in range(len(grid.grid)):
        for j in range(len(grid.grid)):
            if grid.grid[i][j][1] != -1:
                if projectList[grid.grid[i][j][1]].isResid():
                    canvas.create_rectangle(i, j, i+1, j+1, fill="red", width=0)
                else:
                    canvas.create_rectangle(i, j, i+1, j+1, fill="green", width=0)
    mainloop()

