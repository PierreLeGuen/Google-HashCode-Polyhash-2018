#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Créé le 16 Oct 2018

@author: UlysseGuyon
'''


import sys
import os
sys.path.insert(0, "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-2])+"/")
from Solvers import randomCity
from Solvers import UnitDispSolver
from Solvers import LocalAdjSolver

def main():
        randomCity.randomSolver(5000, 1)
        LocalAdjSolver.BestCitySolver(500, 1, 100)
        UnitDispSolver.placementUnitOpti(200, 1, 1000)

        #### POUR LES TESTS :
        # for i in range(6):
        #         randomCity.randomSolver(5000, i)
        #         LocalAdjSolver.BestCitySolver(500, i, 100)
        #         UnitDispSolver.placementUnitOpti(200, i, 1000)

if __name__ == "__main__":
    main()