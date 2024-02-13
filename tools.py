from math import sqrt

from pathfinding.core.diagonal_movement import DiagonalMovement                         #Le pathfiniding sert à calculer les trajectoire les plus optimiser dns le quadriallage
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

def norme(vec):                   #retourne la norme du vecteur 
	return sqrt(vec[0]**2+vec[1]**2)

def create_vect(p1,p2,norme):	#creer un vecteur

	x,y = p1
	x2,y2 = p2
	dx = x2-x
	dy = y2-y
	dxy = sqrt((x-x2)**2+(y-y2)**2)
	ratio = dxy/norme
	if not ratio:
		return (0,0)
	vx = dx/ratio
	vy = dy/ratio
	return vx,vy

def create_path(start,end,matrix):            #Creer le chemin le plus corut (sous forme de liste)
	grid = Grid(matrix=matrix)
	start = grid.node(*start)
	end = grid.node(*end)

	finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
	path, runs = finder.find_path(start, end, grid)
	return path
	
	
def generator(matrice,n,size_chunk):
	pass
	
	

def straight_length(p1,p2):							#Retourne la distance entre 2 points
	return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)