# Projet-Pieton
simulation de foule 

Ce code propose la simulation de carré sortant d'une piece en python.

requis : librairie Pillow, Tkinter, et re

```

EMPTY = 0
WALL = 1
GOAL = X
CHUNK_SIZE =50
PERSON_SIZE = 25

MAP = [
000000001
000000001
000000001
1X1100001
111111111
]

LIST = [
0,0
]
DENSITY = 1
```

structure basique d'une map, la densité demande au programme de faire un apparaitre des `n`carrés par case de maniere aleatoire. /!\ ne prend pas en compte la superposition avec les point proposé dans la LIST
les autres parametres de l'exemple sont obligatoire pour le lancement de la simulation. 
