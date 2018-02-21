
# ## Dossier de données utilisateur
#data = "C:/Users/Citadia/Desktop/DEV/foncier/data"

import os
import pprint
import geopandas as gpd
donnee = []
dict_shp = {}

class data: # class permettant de définir le dossier de données indiqué par l'utilisateur
    def __init__(self, nom):
        self.nom = nom
        print('Initialisation du dossier de donnée : {})'.format(self.nom))

    def listing(self):  # Fonction listing permettant de selectionner les fichier shapefile contenu dans le dossier utilisateur
        for shape in os.listdir(self):
            if shape.endswith('.shp'):
                donnee.append(shape)
            else:
                pass

    def dictionnaire(self):  # ## Etablissement d'un dictionnaire pour guider l'utilisateur dans le choix des données à utiliser
        index =[]
        i = 1
        for shp in donnee:  # Création de la liste d'index du dictionnaire
            index.append(i)
            i = i + 1
        y = 0
        for x in index:  # La liste des couches shape sera contenu dans le dictionnaire dict_shp dont chaque fichier shape sera associé à un index
            dict_shp[x] = donnee[y]
            y = y + 1
        pprint.pprint(dict_shp) # Permettant de lister l'ensemble des couches shape du dossier associé à un numéro


choix_du_dossier = input("Indiquez le chemin du dossier contenant les données : ")
data(choix_du_dossier) # définition du dossier utilisateur
data.listing(choix_du_dossier) # listing des fichiers shape
data.dictionnaire(choix_du_dossier) # Association des fichiers à un numéro (index)


# ## Paramétrage utilisateur
## Une fois que les fichiers shape ont été associé à un numéro, l'utilisateur pourra sélectionner les fichiers shape par leur numéro (index) correspondant

# 1 Choix de la donnée : parcelle
print("Choix de la donnée : Parcelle")

while 1:
    choix_parcelle = int(input("Indiquez le numero de la donnée correspondant aux parcelles (BD parcellaire, Cadastre DGFiP, ...) : "))
    if choix_parcelle in dict_shp:
        parcelle = gpd.read_file(choix_du_dossier+ "/" + dict_shp[choix_parcelle])
        print("La couche parcelle a été défini!")
        break

# 2 Choix de la donnée : bâti
print("Choix de la donnée : Bâti")

while 1:
    choix_bati = int(input("Indiquez le numero de la donnée correspondant aux bâti (BD parcellaire, Cadastre DGFiP, ...) : "))
    if choix_bati in dict_shp:
        bati = gpd.read_file(choix_du_dossier+ "/" + dict_shp[choix_bati])
        print("La couche bati a été défini!")
        break



# 3 Choix de la donnée : filtres excluants (cimetière, terrains de sport, etc)
print("Choix de la donnée : Filtres excluants")

filtres_1 = input("Sélectionner une donnée comme filtre exluant? : o (oui) ou n (non) \n")
if filtres == "o":
    filtres_1 = int(input("Indiquez le numero de la donnée correspondant aux filtres excluants (terrain de sport, cimetière, ...), en l'absence de filtres excluants supplémentaires appuyez sur la touche entrer: ")) # introduire la possibilité d'entrer plusieurs couches
    while 1:
        if filtres_1 in dict_shp:
            filtres_1 = gpd.read_file(choix_du_dossier+ "/" + dict_shp[filtres_1])
            print("La couche filtre exluant n°1 a été défini!")
            break
else:
    pass

filtres_2 = input("Sélectionner une donnée comme filtre exluant? : o (oui) ou n (non) \n")
if filtres_2 == "o":
    filtres_2 = int(input("Indiquez le numero de la donnée correspondant aux filtres excluants (terrain de sport, cimetière, ...), en l'absence de filtres excluants supplémentaires appuyez sur la touche entrer: ")) # introduire la possibilité d'entrer plusieurs couches
    while 1:
        if filtres_2 in dict_shp:
            filtres_2 = gpd.read_file(choix_du_dossier+ "/" + dict_shp[filtres_2])
            print("La couche filtre exluant n°2 a été défini!")
            break
else:
    pass

# 4 Choix de la donnée : surface en eau
print("Choix de la donnée : Surface en eau")

while 1:
    choix_hydro = int(input("Indiquez le numero de la donnée correspondant à la surface en eau : "))
    if choix_hydro in dict_shp:
        surf_hydro = gpd.read_file(choix_du_dossier+ "/" + dict_shp[choix_hydro])
        print("La couche surface en eau a été défini!")
        break

# 5 Choix de la donnée : Voie ferrée
print("Choix de la donnée : Voie ferrée")

while 1:
    choix_voie_ferree = int(input("Indiquez le numero de la donnée correspondant aux voies ferrées : "))
    if choix_voie_ferree in dict_shp:
        voie_ferree = gpd.read_file(choix_du_dossier+ "/" + dict_shp[choix_voie_ferree])
        print("La couche des voies ferrées a été défini!")
        break
