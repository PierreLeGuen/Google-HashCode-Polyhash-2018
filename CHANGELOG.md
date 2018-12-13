# Versions de PolyHash 2019 - Groupe P
## Version 0.1

* Ajout d'un module InputManager permettant d'accéder facilement aux fichiers input fournis par Google
* Ajout d'un module OutputManager permettant de rédiger les fichiers d'output finaux à partir d'un tableau contenant déjà les informations voulues
* Ajout du module main permettant de lancer le programme
* Ajout du module grid qui crée la grille de la ville
* Ajout du module project qui crée la classe project modélisant le projet courant
* Première version du placement aléatoire des bâtiments, randomCity.py.
* Ajout d'un module pour calculer la distance de manhattan (en développement)

## Version 0.2

* Fix du calcul de la distance de manhattan : plus de boucle infinie
* Ajout du calcul du score dans la classe Grid
    * temps de calcul : 2h/20000 batiments; 15min/9000 batiments (équirépartis, estimations approximatives)
* Ajout d'un affichage terminal permettant de se repérer dans l'execution du code
* Création d'un meilleur arrangement pour les modules
* Fix du calcul du score :
    * Calcul itératif complet utilisé pour l'instant pour obtenir un score exact
    * Calcul optimisé en cours de développement
    
## Version 0.3

* Calcul de distance et de score raisonnablement optimisés
    * temps de calcul du score pour une grille entière : max 1 heure
* Ajout d'unefonction calculant un poids pour les batiments résidentiels (représente si ils sont intéresseants)

## Version 0.4

* Première version de UnitDispSolver par Ulysse et Sacha. Cet algorithme fait appel au calcul de poids de chaque batiments développés précedemment. 
    * Principe : test le placement d'un bâtiments à différents endroit de la grille afin d'obtenir le meilleur score 
* Corrections de bugs
* Ajout d'une fonction calculant un poids pour les batiments résidentiels (représente si ils sont intéresseants)
* Ajout d'une fonction calculant un poids pour les batiments utilitaires
* Ajout d'une fonction éliminant les batiments inutiles ou redondants lors de l'input

## Version 0.5 

* Amélioration UnitDispSolver, correction de bugs
* Première version de LocalAdjSolver
    * Principe : division de la grille n fois. Puis nous faisons x simulations en gardant le meilleur des résultats. Ensuite duplication de cette grille maximisée.
* Ajout d'un fichier contenant les constantes importantes du programme

## Version 1.0

* Fix des bugs de solveurs
* Cleaning du code
