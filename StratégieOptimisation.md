# Stratégies envisageable

## Pré-algorithme

Sélectionner préférentiellement des projets résidentiels avec un fort taux de rendement ( population / nombre de cases occupées ).

Supprimer les projets inutiles, exemple : dans b_short_walk.in on peut supprimer "R 1 2 1" car on a un "R 1 2 2".

(Supprimer aussi les redondances dans les inputs)

## Méta-heuristique

problème complexe dont on ne sait pas si on peut appliquer une solution unique optimisée.
Donc nécessité de trouver des solutions approchée

### Algorithme génétique et évolutionnaire

Evolution de différents états sur une population donnée.
Ici, la grille de la ville est l'environnement, les projets sont la population.
Il faut trouver des manières d'évoluer la population et de garder les meilleurs individus.
idées :

- réduction au maximum des cases vides dans la grille;
- maximisation du nombre d'utilitaires d'un projet résidentiel;
- répartition selon la taille des projets et selon la distance D;
- surface d'utilitaires et surface de résidentiels la plus égale possible.

### Algorithme Glouton

- Optimisation sur une partie locale du problème.
- Ici, faire en sorte qu'un résidentiel en particulier aie un score maximal, soit le plus d'utilitaires différents à la distance D.

## Codage de la grille 

- Idée : coder la grille comme une liste en deux dimensions, sans tuples. On met un 0 si la case est inoccupée. On met des nombres positifs pour les utilitaires
et des négatifs pour les résidentiels. On garde une liste des résidentiels construits et une liste des utilitaires construits pour récupérer le nomre d'haitants
et le type d'utilitaire.

## Codage du score

- Précalculer une distance rapide approximative (2\*D ou 3\*D) pour réduire le temps de calcul du score en éliminant en gros les utilitaires loin du résidentiel.