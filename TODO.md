# Fonctionnalités à implanter/améliorer

## Fonctions obligatoires (Ulysee Guyon)

* Trouver les meilleurs bâtiments dans un exemple d'input (a,b,c,d,e,f);
  * Appliquer un poids aux bâtiments résidentiels (le meilleur en fonction de la taille et du nb de résidents)

## Algorithme d'adjacence locale (Pierre Le Guen & Louis Canu)

1. Diviser la taille de la grille (3 fois taille du bâtiment le plus haut et plus large);
2. Dans cette nouvelle grille mettre par ~5 bâtiments par défaut (R ou U );
3. Fonction qui vérifie si un projet résidentiel sera posé à côté d'un utilitaire;
4. Placement des bâtiments random avec contraintes (être à côté d'un autre bâtiment);
5. Répétition de ces étapes et arrêt au bout d'un certain nb d'erreurs consécutives;
6. Duplication pour remplir la grille originelle.

## Algorithme de placement unitaire optimisé (Ulysse Guyon & Sacha Wanono)

1. Poser deux bâtiments de type différent, de base dans la grille
2. A chaque étape, poser un bâtiment sur la grille en random x fois
3. Garder la meilleur position en fonction du score (!!À faire Ulysse)
4. Si le batiment est "not buildable" sur les x fois testées on arrête l'algo

## Visualisation graphique de la grille finale (Louis Canu)

1. Utiliser tkinter ou autres pour l'interface graphique
2. Afficher les batiments résidentiels d'une couleur différente des bâtiments utilitaires
3. Si possible tracer un trait plus épais autours de chaque bâtiment pour différencier ceux du même type