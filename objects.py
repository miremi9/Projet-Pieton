class Rect:                                                                             #Création d'une classe Rectangle
	def __init__(self,x,y,sx,sy):                                                       #Initialisation de la classe

		self.top = y
		self.bottom = y+sy
		self.left =x
		self.right = x+sx


	def set_left(self,val):                                                             #Fonction liée au déplacement vers la gauche du Rectangle
		change =val-self.left
		self.left = val
		self.right +=change

	def set_right(self,val):                                                            #Fonction liée au déplacement vers la droite du rectangle
		change =val-self.right
		self.right = val
		self.left +=change

	def set_top(self,val):                                                              #Fonction liée au déplacement du rectangle vers le haut
		change =val-self.top
		self.top = val
		self.bottom +=change

	def set_bottom(self,val):                                                           #Fonction liée au déplacmenet du rectangle vers le bas
		change =val-self.bottom
		self.bottom = val
		self.top +=change


	def set_pos(self,x,y):                                                             #Fonction qui défini une postion au rectangle
		self.set_left(x)
		self.set_top(y)

	@property								#fonction qui return l'appel de l'attribut pos
	def pos(self):
		return self.left,self.top

	@property               #Fonction qui retoune l'appel de l'attribut center
	def center(self):
		return (self.left+self.right)/2,(self.top+self.bottom)/2

	def collides_with(self, other):															                                          #return si deux rectangles sont en 	collision (True or False)
		return self.left < other.right and self.right > other.left and self.top < other.bottom and self.bottom > other.top






class Wall:                                             #Definition d'une classe Mur
	def __init__(self,p1,p2,root,color = "black"):         #Initialisation de la calsse mur
		self.p1 = p1
		self.p2 = p2
		mx = p2[0]-p1[0]
		my =  p2[1]-p1[1]
		self.id = root.create_rectangle(*p1,*p2,fill=color)
		self.rect = Rect(*p1,mx,my)
	def __str__(self):
		return f"Mur num {self.id}"

class Exit(Wall):                                   #Definition de la classe sortie (le trou dans le mur )
	def __init__(self,p1,p2,root,color="green"):
		Wall.__init__(self,p1,p2,root,color)
