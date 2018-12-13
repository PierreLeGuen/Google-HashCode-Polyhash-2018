# Projet d'algorithmique -  Finale du Google Hash Code 2018

![Logo équipe manhattan](logo_manhattan.png)

L'objectif de ce projet,  Poly#, est d'approfondir nos compétences en algorithmie, ainsi qu'en Python. PolyHash 2019 a lieu lors de notre semestre 5 à Polytech' Nantes, en formation initiale d'informatique durant 10 semaines.
Dans ce projet, le but est d'optimiser le placement de batiments dans une grille en fonction de certaines caractéristiques de cette grille et de ces batiments.
Les grilles et les différents batiments que l'on peut placer dedans sont fournis dans 6 fichiers inputs différents. A partir de ça, on doit créer des fichiers output contenant chaque projet construit et ses coordonnées.

Les outils principaux utilisés sont les suivants:
* Git : un logiciel de gestion de versions;
* Python3 : Nouvelle version de Python;
* Librairies Python :
  * TKinter

## Membres du groupe et attribution des rôles

* Pierre Le Guen
  * Chef de projet
  * Rédaction de documentation
  * Solveur Random
  * Solveur Adjacence locale
* Ulysse Guyon
  * Gestion des fichiers inputs
  * Calcul du score
  * Solveur Placement unitaire
  * Débugage de l'ensemble du code
* Sacha Wanono
  * Gestion des fichiers créés en output
  * Création de liste de poids pour les bâtiments
  * Solveur Placement unitaire
* Louis Canu
  * Affichage graphique
  * Gestion de la grille
  * Montage Vidéo

## Stratégies d'optimisation

### Algo d'adjacence locale
  * On travaille dans une grille plus petite
  * Placement d'un batiment de chaque type (Résid/Util) en initialisation
  * Faire un certain nombre de simulations :
    * Pour chaque batiment à placer, on le place seulement si il est à côté d'un batiment de l'autre type
    * Après avoir remplis la petite grille, on regarde son score
  * On garde la simulation avec le meilleur score et on la dulique sur la taille de la grille réelle

Performance : selon les paramètres :
  * élevés : durée de calcul très élevée mais score assez optimisé pour des batiments petits
  * faibles : durée de calcul assez rapide mais score médiocre

### Algo de placement unitaire
  * On travaille dans une grille plus petite
  * Placement d'un batiment de chaque type (Résid/Util) en initialisation
  * Faire un certain nombre de simulations :
    * Pour chaque batiment à placer, on test un certain nombre de coordonnées aléatoires
    * On garde les coordonnées qui fournissent le meilleur score 
    * Après avoir remplis la petite grille, on regarde son score
  * On garde la simulation avec le meilleur score et on la dulique sur la taille de la grille réelle

Performance : complexité acceptable (~ n*m) pour des score généralement bons (> 1.000.000 pour < 1h de calcul)

## Organisation du code

* Dossier principal
  * Documentation (README, CHANGELOG, DOCKERFILE, ...)
  * Dossier src
    * main
    * constants
    * grid
    * project
    * projectDisplay
    * projectListBuilder
    * Dossier inputs (contenant les fichiers fournis par Google)
    * Dossier outputs (contenant les fichiers résultants de la construction des grilles)
    * Dossier ScoringTools
      * calculDist
      * calculScore
      * cellSelector
      * calculWeight
    * Dossier InOutManager
      * inputmanager
      * ouputmanager
    * Dossier Solvers
      * randomCity
      * unitDispSolver
      * localAdjSolver

## Limitations connues

* Calculs des poids surtout adaptés aux batiments fournis par Google
* Les algos de duplication de grille ne s'appliquent que pour les grilles de dimensions 1000x1000

## Installation et execution sur votre machine

### Docker

Télécharger le répertoire PolyHash du Groupe P

```shell
$ git clone https://gitlab.univ-nantes.fr/E166236R/equipe-p---projetalgo2018.git
```

Construire l'image docker pour PolyHash

```shell
~/equipe-p---projetalgo2018$ docker build -t polyhash .
```

Démarrer le conteneur Docker :

```shell
~/equipe-p---projetalgo2018$ docker run polyhash
```

### Linux

Télécharger le répertoire PolyHash du Groupe P

```shell
$ git clone https://gitlab.univ-nantes.fr/E166236R/equipe-p---projetalgo2018.git
```

Préparer un env virtuel Python3 : 

```shell
$ python3 -m venv polyhash2019
```

Si la commande échoue : 

```shell
$ rm -rf polyhash2019/
$ virtualenv -p python3 polyhash2019
```

Puis entrer dans l'env virtuel :

```shell
$ source polyhash2019/bin/activate
```

Puis lancer l'application :

```shell
$ cd polyhash2019/src/
$ python3 main.py
```

Pour désactiver l'env virtuel :

```shell
$ deactivate
```

### Windows

(Utiliser le PowerShell "_PS_")

Télécharger le répertoire PolyHash du Groupe P :

```powershell
PS C:\> git clone https://gitlab.univ-nantes.fr/E166236R/equipe-p---projetalgo2018.git
```

Vérifier si Python est installé grâce à :

```powershell
PS C:\> python
Python 3.x (v3.7.0:1bf9cc5093, Jun 27 2018, 04:59:51) [MSC v.1914 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
```

Sinon installer Python via le [site officiel](https://www.python.org/downloads/release)

Vérifier si _pip_ est installé : 

```powershell
PS C:\> pip
Usage:
    pip <command> [options]
```

Sinon suivre les instructions sur le [site officiel de pip](https://pip.pypa.io/en/latest/installing/#using-the-installer)

Installer virtualenv :

```powershell
PS C:\> pip install virtualenv
```

Création de l'environnement virtuel Python3 (à l'endroit du répertoire courant) :

```powershell
PS C:\> virtualenv PolyHash2019
```

Démarrer l'environnement virtuel :

```powershell
PS C:\> PolyHash2019\Scripts\activate
```

Pour désactiver l'env virtuel :

```powershell
PS C:\> deactivate
```
