
from math import isclose,sqrt

import tools as tl
from objects import *


class Person:                                                                             #Définition d'une Classe personne
	size =10,10                                                                    #Taille de l'objet Personne
	speed = 2                                                                            #Vitesse de la personne
	image =None
	def __init__(self,pos,matrice,canvas,world):                                          #Initialisation de l'objet personne
		
		self.rect = Rect(*pos,*self.size)
		self.pos_matrice = world.get_matrice_f_pos(self.rect.center)                        #Initialisation de sa position dans la matrice(quadriallage)
		self.objectif = world.goal
		self.li_pos = [self.rect.pos]
		self.stat_collision= (0,0)
		length = float("inf")
		for objectif in self.objectif:

                                                                                    #Défintion de la trajectoire pour les personnes
			path = tl.create_path(self.pos_matrice,objectif,matrice)
			if len(path)< length:                                                           #Choix du parcours le plus court 
				length = len(path)
				self.path = path
				self.objectif_coo = world.center(objectif)
				self.objectif = objectif
				
		if Person.image:
			self.id = canvas.create_image(*pos,image=Person.image,anchor= "nw")                    #Création d'une image pour la personne
			self.type = "image"
		else:
			self.id = canvas.create_rectangle(*pos,pos[0]+Person.size[0],pos[1]+Person.size[1],fill="blue")
			self.type = "rect"

		self.world = world
		self.root = canvas
		self.aim = False
		self.status = ("move",)
		
	def update(self,li):                                                    #Fonction qui appel l'objet à bouger
		pos = self.rect.center
		
		if not self.path:
			return 

		if not self.aim :
			for coo in reversed(self.path):
				if self.can_go(coo,self.world.walls):
					self.aim = (self.world.center(coo),coo)
					break
			else:
				raise ValueError("NoWhere2go")
		vect = tl.create_vect(self.aim[0],self.rect.center,-type(self).speed)          #Création du vecteur de mouvement
		speed = type(self).speed
		
		
		if self.status[0] == "stuck":
			side = self.status[1]
			
			if  ("bottom" == side or  "top" == side)and vect[1] != 0:
				if vect[0] > 0:
					vect =[speed,0]
				else:
					vect =[ -speed,0]
					
				if "bottom" in side:
					vect[1] = 1
				else:
					vect[1] = -1
			
			elif   ("left" == side or "right" == side):
				if vect[1] > 0:
					vect =[0,speed]
				else:
					vect =[0,speed]
				
				if "left" ==side:
					vect[0] =-1
				else:
					vect[0] =1
					
		sides,data = self.move(vect,li)                                                      #La personne se deplace
		
		self.li_pos.append(self.rect.pos)
		
		
		if self.world.rect_in(self.rect,self.aim[1]):
			self.aim = False
			if self.world.rect_in(self.rect,self.objectif):

				self.set_position(-100,-100)
				self.rect.set_pos(-100,-100)
				return "end"
			
			
		if data == "done":
			if self.type !="image":
				self.root.coords(self.id,int(self.rect.pos[0]),int(self.rect.pos[1]),int(self.rect.pos[0]+Person.size[0]),int(self.rect.pos[1]+Person.size[1]))
				self.root.itemconfig(self.id, fill='green')
			else:
				self.root.coords(self.id,int(self.rect.pos[0]),int(self.rect.pos[1]))	
		
		if data == 'stuck': 
			self.root.itemconfig(self.id, fill='#F92727')
			self.status = "stuck",next(iter(sides))
			
		if data == "ok" and self.type!="image":
				self.root.itemconfig(self.id, fill='#00400D')	

		if self.status[0] == "stuck":
			if not self.status[1] in sides:
				self.status = ("move",)
				
		coll,nb = self.stat_collision

		if data in ("stuck","ok"):
			self.stat_collision = coll+1,nb+1
		else:
			self.stat_collision = coll,nb+1



	def move(self,vect,liste_object):                               #Définiton de la fonction move (déplacement de la personne)
		start = self.rect.pos
		rect_projection = Rect(self.rect.pos[0]+vect[0],self.rect.pos[1]+vect[1],*type(self).size)	#position hypothetique 

		long_vec = tl.norme(vect)
		collide_side= self.check_collide(rect_projection,liste_object)                              #On regarde si il y a une collision, et si il y a collison, on rectifie la trajectoire


		self.rect.set_pos(*rect_projection.pos)                                       #le rectangle va sur sa projection      

		x,y,*_  = self.root.coords(self.id)                                           #Sert a l'affiche sur Tkinter

		end = self.rect.pos
		done = tl.sqrt((start[0]-end[0])**2+(start[1]-end[1])**2)
		
		if long_vec - done<.001:			                                        #Cas où le personnage ne se prend pas de murs
			return collide_side,"done"

		todo = long_vec-done                                                      #Cas ou le personnage se prend un mur 
		if not ("bottom" in collide_side or "top" in collide_side) and vect[1] != 0:
			if vect[1] > 0:
				vect =0,-todo*0.8
			else:
				vect = 0,todo*0.8

		elif  not ("left" in collide_side or "right" in collide_side):
			if vect[0] > 0:
				vect =todo*0.8,0
			else:
				vect =-todo*0.8,0
		rect_projection = Rect(self.rect.pos[0]+vect[0],self.rect.pos[1]+vect[1],*type(self).size)          #On recommence une projection


		self.check_collide(rect_projection,liste_object)
		self.rect.set_pos(*rect_projection.pos)
		
		end = self.rect.pos
		done = sqrt((start[0]-end[0])**2+(start[1]-end[1])**2)
		
				
		x,y,*_  = self.root.coords(self.id)
		self.set_position(*self.rect.pos)
				
		if done< tl.norme(vect) and len(collide_side)==1:
			return collide_side,"ok"
			return collide_side,"stuck"

		return collide_side,"ok"
		
	def set_position(self,x,y,*arg):
		if self.type!="image":
			self.root.coords(self.id,x,y,x+Person.size[0],y+Person.size[1])
		else:
			self.root.coords(self.id,x,y)
						
		
		
	def check_collide(self,rect_projection,liste):                  #Sert a vérifier qu'il n'y est pas de rectangles qui se touchent
		collide_side = set()


		for obj in liste:
			if obj == self:
				continue
			if rect_projection.collides_with(obj.rect):

				collide_side.update(self.correct(rect_projection,obj.rect))


		return collide_side

	def correct(self,rect_projection,obj):                                    #Sert à la correction des rectangles  
		vtarget = self.rect
		target = rect_projection
		wall = obj
		collid = set()
		if (target.top <= wall.bottom or isclose(target.top,wall.bottom)) and (vtarget.top >= wall.bottom or isclose(vtarget.top,wall.bottom)):   #down
			target.set_top(wall.bottom)
			collid.add("top")

		if (target.bottom >= wall.top or isclose(target.bottom,wall.top) ) and (vtarget.bottom <= wall.top or isclose(vtarget.bottom,wall.top)):  #up
			target.set_bottom(wall.top)
			collid.add("bottom")

		if (target.left <= wall.right or isclose(target.left,wall.right))and (vtarget.left >= wall.right or isclose(vtarget.left,wall.right)): #left

			target.set_left(wall.right)
			collid.add("left")
		if (target.right >= wall.left or isclose(target.right,wall.left)) and (vtarget.right <= wall.left or isclose(vtarget.right,wall.left)) :   #right
			target.set_right(wall.left)
			collid.add("right")

		return collid

	def can_go(self,coo,liste):                                     #Verifie que le chemin rectiligne est possible
		goto = self.world.center(coo)
		length = tl.straight_length(self.rect.center,goto)
		nb = int(length//type(self).speed)

		for k in range(1,nb):
			vect = tl.create_vect(self.rect.center,goto,type(self).speed*k)
			rect_projection = Rect(self.rect.pos[0]+vect[0],self.rect.pos[1]+vect[1],*type(self).size)
			if self.check_collide(rect_projection,liste):
				return False



		return True

	def __str__(self):
		return f"Perso num {self.id}"