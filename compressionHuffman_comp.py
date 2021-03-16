import heapq
import os

class Huffman:
	def __init__(self, chemin):
		self.chemin = chemin
		self.ensemble = []
		self.codes = {}
		
        
        
        
	class arbre:
		def __init__(self, caract, freq):
			self.caract = caract
			self.freq = freq
			self.left = None
			self.right = None

		def __lt__(self, other):
			return self.freq < other.freq

		def __eq__(self, other):
			return self.freq == other.freq
#Creation de l’arbre : l’arbre prend comme paramétre le caractère et sa fréquence	. On initialise aussi le fils gauche et le fils droit.
#Utilisation de heapq qui permet de créer des arbres binaires pour lesquels chaque nœud fils a une valeur inférieure ou égale au nœud parent et donc il est nécessaire de prendre en compte cette paramétre dans la construction 


	def frequence(self, text):
		frequence = {}
		for caract in text:
			if not caract in frequence:
				frequence[caract] = 0              
			frequence[caract] += 1
		return frequence
#Dictionary de frequence : calcul la frequence de chaque caractères
#Récuperation de toutes les chaines de caractères et leur occurrence avec la fonction for qui permet de tous les parcourir. Et en incrementant à chaque fois.

    
        
	def priority(self, frequence):
		for i in frequence:
			noeud_caract = self.arbre(i, frequence[i])
			heapq.heappush(self.ensemble, noeud_caract)
#prioriité : tas : faire la priorité : file d’attente
#Self.ensemble est la liste dans laquelle on va ajouter les nœuds(caractères) au fur et à mesure
#On recupere alors chaque caractere qui est dans fréquence en respectant la construction càd du plus petit au plus grand. Chaque caractere est considéré comme un nœud. Ensuite on ajoute dans self.ensemble au fur et à mesure de la boucle heapq.heappush. 
#Ainsi à la fin on notre liste d’attente des caractères 

            
            

	def arbre_construction(self):
		while(len(self.ensemble)>1):
			noeud1 = heapq.heappop(self.ensemble)
			noeud2 = heapq.heappop(self.ensemble)

			fusion = self.arbre(None, noeud1.freq + noeud2.freq)
			fusion.left = noeud1
			fusion.right = noeud2

			heapq.heappush(self.ensemble, fusion)
#Fusion : construction de l’arbre, save root node in heap
#Après avoir rempli la file d’attente, on met en place l’algorithme de Huffman qui consiste dans un premier temps de récupérer les 2 plus petits nœuds avec heappop qui PERMET DE retourner le plus petit élément de notre ensemble qu’on fait 2 fois.
#On fusionne les deux nœuds sélectionnés en un nœud père dont la fréquence sera la somme des 2 et ces derniers deviendront le nœud de gauche et le nœud de droite 
#On ajoute la fusion dans self.ensemble 
#Ainsi on continue à faire jusqu’à avoir autant de mini arbres possibles
#Tant que self.ensemble comporte au moins 2 éléments

            
	def recup_crypt(self, racine, crypt):
        #hauffman

		if(racine.caract != None):
			self.codes[racine.caract] = crypt
			
			return

		self.recup_crypt(racine.left, crypt + "0")
		self.recup_crypt(racine.right, crypt + "1")
#Recup_crypt : permet d’écrire la syntaxe qu’il faut mettre pour coder avec l’algorithme de Hauffman : càd mettre pour tous les fils gauche 0 et les dorit droite 1 et concanéter au fur et à mesure. Cette fonction nous permettra de coder chaque caractère*
        

	def coder(self):
        #coder les caractères
		noeud = heapq.heappop(self.ensemble)
		code = ""
		self.recup_crypt(noeud, code)
#Coder  : coder les charactères
#Pour chaque élément(nœud ou caractère) de self.ensemble on le soumet à recup_crypt qui permet d’avoir son codage après la fusion. On stocke les nœuds et leur codages dans self.codes
#Donc chaque caractère est codé

        
        
        
	def code_texte(self, text):
		code_texte = ""
		for i in text:
			code_texte += self.codes[i]
		return code_texte
#Texte codé : remlacer chaque caractères par leur codes pour avoir le texte entier codé
    
    
	def ajout(self, code_texte):
		extra_padding = 8 - len(code_texte) % 8
		for i in range(extra_padding):
			code_texte += "0"

		padded_info = "{0:08b}".format(extra_padding)
		code_texte = padded_info + code_texte
		return code_texte


	def get_byte_array(self, code_texte_ajout):

		b = bytearray()
		for i in range(0, len(code_texte_ajout), 8):
			byte = code_texte_ajout[i:i+8]
			b.append(int(byte, 2))
		return b
#si la longueur totale du flux binaire codé final n'est pas multiple de 8, ajoutez un peu de remplissage au texte
#stocker ces informations de remplissage (en 8 bits) au début du train de bits codé
#Pour différencier les bits des bytes ou octets, il faut savoir que : 1 octet, ou byte en anglais, vaut 8 bits. Le poids des objets téléchargés est indiqué en octets et non en bits. 
    

	def compression(self):
		fichier, fichier_extension = os.path.splitext(self.chemin)
		resultat = fichier + ".bin"
        

		with open(self.chemin, 'r+', encoding="utf-8") as txt, open(resultat, 'wb') as compress:
			text = txt.read()
			print(len(text))
            
			
			frequence = self.frequence(text)
			self.priority(frequence)
			self.arbre_construction()
			self.coder()

			code_texte = self.code_texte(text)
			ajout = self.ajout(code_texte)

			b = self.get_byte_array(ajout)
			compress.write(bytes(b))

  
                
            
            
		print("Compression réussie")
		#print(os.path.getsize(resultat))
		#a=sorted(frequence)
		print(frequence)
    
		return resultat
        
        
    
    
   

        

    
    
    
chemin= 'C:/Users/Utilisateur/Documents/IDU/S6/Proj631_Algorithmique/Huffman/alice.txt'

H= Huffman(chemin)
H.compression()


#Codage des caractères
print(H.codes)

#taux de compression
chemin2= chemin[:-3]
chemin2= chemin2 + "bin"

TAUX=((1-((os.path.getsize(chemin2))/(os.path.getsize(chemin))))*100)
print("Le taux de compression est de",TAUX,"%")
print("Le nombre est passé de",(os.path.getsize(chemin)),"à",(os.path.getsize(chemin2)),"octets")

with open(chemin, 'r+', encoding="utf-8") as txt:
		text = txt.read()
		moyen= len(text)/(os.path.getsize(chemin2))  #*8
		print("La longueur du texte est",len(text),". Donc le nombre moyen de bits de stockage est",moyen)






