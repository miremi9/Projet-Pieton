from math import sqrt,isclose                                                           #Importation de la fonction sqrt et isclose
import tkinter as tk                                                                    #Importation de tkinter
from random import randint,choice                                                       #Importation de la fonction randint et choice
import time                                                                             #Importation d'une horloge
import re                                                                               #Importation de re

from PIL import Image, ImageTk

import tools as tl
from person import Person
from objects import *

from generator import *

SPEED =100


class World:                                      #Definition de la classe monde, il va contenir tout(mur,personnes,rectangle,mouvements....)
	chunk =50
	def __init__(self,root,path_map):

		self.root = root
		self.matrice,self.walls,self.goal,list_pos,li_exit,EMPTY,GOAL,WALL,World.chunk=parse(path_map,self)         #Recuperation de toutes les informations
		self.mob = set()
		self.time = 0
		for k in list_pos:                                            #Création des personnes           
			self.mob.add(Person(k,self.matrice,root,self))
		self.mob_alive = self.mob.copy()	
		
	def rect_in(self,rect,pos):	#permet de verifier sur un rectangle est dans une case de la matrice
		return (rect.top > pos[1]*type(self).chunk and rect.left > pos[0]*type(self).chunk and rect.right < (1+pos[0])*type(self).chunk and rect.bottom < (1+pos[1])*type(self).chunk)

	def move(self):                                         #Sert à mettre a jour la position 
		self.time +=1
		to_remove = set()
		for k in sorted(self.mob_alive,key=lambda x: tl.straight_length(x.rect.pos,x.objectif_coo)):
			if k.update(self.mob.union(self.walls))=="end":
				to_remove.add(k)
		self.mob_alive.difference_update(to_remove)
		if not len(self.mob_alive):
			return self.time
			
	def rollback(self,n):
		n = int(n)
		for k in self.mob:
			try:
				k.set_position(*k.li_pos[n])
			except IndexError:
				k.set_position(-100,-100)

	def get_matrice_f_pos(self,pos):
		return int(pos[0]//World.chunk),int(pos[1]//World.chunk)

	def center(self,pos):                             #Retourne le centre d'un personnage
		return World.chunk*(pos[0]+0.5),World.chunk*(pos[1]+0.5)

	def average(self):
		a = map((lambda x :x.stat_collision[0]/x.stat_collision[1]),self.mob)

		return sum(a)/len(self.mob)


class Win(tk.Frame):                                    #L'affichage sous Tkinter
	size = 800,800
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.pack()
		
		self.value = tk.DoubleVar()
		
		
		
		self.cadre = tk.Canvas(self,width = 800,height= 800)
		self.cadre.pack()
		
		self.world = World(self.cadre,"map.txt")
		time.sleep(1)
		self.update()
	
	def update(self):
		time =  self.world.move()
		if not time:
			self.after(SPEED ,self.update)
		else:
			self.label = tk.Label(text=f"Il a fallut {time} secondes pour evacuer la piece")
			self.label.pack()
			
			self.label2 = tk.Label(text=f"Il y a {int(self.world.average()*100)}% de contact")
			self.label2.pack()
			self.scale = tk.Scale(self,orient='horizontal', from_=0, to=time+1, variable=self.value,resolution=1,length = 500,command =self.world.rollback)
			self.scale.pack()	

def adapte_pos(case:tuple,size_case,pos):
	return (case[0]*size_case+pos[0],case[1]*size_case+pos[1])

def parse(path_map,world):      #Va transformer le fichier texte 
		root = world.root

		list_pos = set()
		walls = set()
		goal = set()
		exi = set()
		data = parsing_map(parsing_texte(path_map))
		matrice = data["MAP"]
		PERSON_SIZE  = data["PERSON_SIZE"]
		CHUNK_SIZE  = data["CHUNK_SIZE"]

		ratio = max((CHUNK_SIZE*len(matrice[0]))/Win.size[0],(CHUNK_SIZE*len(matrice))/Win.size[1])       #Redimmensionne l'image par rapport à l'écran 
		print(ratio)
		
		Person.size = PERSON_SIZE/ratio, PERSON_SIZE/ratio

		
		
		if "FILE" in data:
			img = ImageTk.PhotoImage(Image.open(data["FILE"]).resize(map(int,Person.size)))
			Person.image = img
		empty_cases  =set()
		CHUNK_SIZE = CHUNK_SIZE/ratio                 #Dimensionement de la salle(mur,rectangles...)
		print(CHUNK_SIZE)
		for y,ligne in enumerate(matrice):
			for x,elem in enumerate(ligne):
				p1 = x*CHUNK_SIZE,y*CHUNK_SIZE
				p2 = (x+1)*CHUNK_SIZE,(y+1)*CHUNK_SIZE

				if elem ==data["WALL"]:
					walls.add(Wall(p1,p2,root))
					matrice[y][x] = 0

				elif elem == data["GOAL"]:
					goal.add((x,y))
					matrice[y][x] = 1
					exi.add(Exit(p1,p2,root))

				elif elem == data["EMPTY"]:
					matrice[y][x] = 1
					root.create_rectangle(*p1,*p2)
					empty_cases.add((x,y))
				else:
					raise ValueError(f"elem inconnu : {elem}")
		

		if "LIST" in data:
			list_pos.update(set(data["LIST"]))
		#creation of random points
		if "DENSITY" in data:
			n = data["DENSITY"]
			size = CHUNK_SIZE-PERSON_SIZE
			for case in empty_cases:
				liste = generate_random_points(data["DENSITY"],size-PERSON_SIZE,size-PERSON_SIZE,PERSON_SIZE)
				list_pos.update(set(map(lambda x: adapte_pos(case,CHUNK_SIZE,x) , liste)))

		return (matrice,walls,goal,list_pos,exi,data["EMPTY"],data["GOAL"],data["WALL"],CHUNK_SIZE)

Win().mainloop()

