#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Créé le 15 Oct 2018

@author: SachaWanono
'''

import os

class OutManager :
    """
    Classe permettant l'écriture du fichier output correspondant à un input donné
    """

    def __init__(self, fileName):
        """
        Méthode  permettant la création du fichier output en extension .out
        
        :param fileName: (str) nom du fichier de sorti, il doit être le même que le fichier input
        """
        # ici on crée le fichier dans le dossier outputs et on le stocke dans la variable self.file 
        # le paramètre 'w' indique que si le fichier existe déjà, on l'écrase avant de le recréer
        path = os.path.dirname(os.path.abspath(__file__))
        if len(path.split("/")) == 1:
            path = "/".join(path.split("\\"))
        absPath = "/".join(path.split("/")[:-1]) + "/outputs/" + fileName
        self.file = open(absPath + ".out", 'w')
        self.fileScore = open(absPath + ".score", 'w')

    def writeScore(self, score):
        """
        Méthode permettant d'écrire le score dans un fichier

        :param score: (int) score final de la grille
        """
        self.fileScore.write(str(score))

    def writeProjects(self, projects):
        """
        Méthode remplissant le fichier output en fonction des normes imposées par l'énoncé et
        des différents projets placés dans notre carte 

        :param projects: (list) double tableau comportant le type de projet et son emplacement (colonne, ligne)
        """

        # la taille du tableau donne le nombre de bâtiment placé
        nbBuildings = len(projects) 

        # on écrit ce nombre dans le fichier :
        self.file.write(str(nbBuildings) + "\n")

        # on parcours les différents projets :
        for i in range(nbBuildings):
            noProject = projects[i][0] # indique le type de projet
            locationX = projects[i][1][0] # indique la position x (la ligne) du haut-gauche du projet
            locationY = projects[i][1][1] # indique la position y (la colonne) du haut-gauche du projet

            self.file.write(str(noProject) + " " + str(locationX) + " " + str(locationY) + "\n")

        # le fichier ne nécessite plus aucune lecture ou modification, on le ferme
        self.file.close()
        self.fileScore.close()

