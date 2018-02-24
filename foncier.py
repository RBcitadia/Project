
# coding: utf-8

# ### Paramètres généraux

# In[1]:


#!/usr/bin/env python3
# coding: utf-8

__author__ = ['[Citadia](https://gitlab.com/Citadia)']
__date__ = '2017.12.08'

import pandas as pd
import geopandas as gpd
import numpy as np
import time
import os
import pprint
from tkinter import *
from numpy import mean
from numpy import median

t = time.process_time()
get_ipython().magic('matplotlib notebook')


# ### Paramètres utilisateur

# In[2]:


# #uf non bâtie
# desserte = float(input("Distance en mètre entre la voirie et l'unité foncière non bâtie"))
# surf_min_uf_non_batie = float(input("surface minimum des unités foncières non bâties"))

# #uf bâtie
# ces_max = float(input("CES maximum des grandes unités foncières bâties"))
# surf_min_uf_batie = float(input("surface minimum des grandes unités foncières bâties"))

desserte = 50
surf_min_uf_non_batie = 500
ces_max = 10
surf_min_uf_batie = 2000


# ### Import des données

# ## Orientation objet

# In[ ]:


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

        def prep(self, info, num):
            info = gpd.read_file(self + "/" + data_shp[num])
            info = info.to_crs({'init':'epsg:2154'})
            info = info[["geometry"]]

        def nettoyage(nom_donnee):
            nom_donnee = nom_donnee[nom_donnee["geometry"].notnull()]
            nom_donnee = nom_donnee[nom_donnee["geometry"].is_valid]


# In[3]:


choix_du_dossier = input("Indiquez le chemin du dossier contenant les données : ")
data(choix_du_dossier) # définition du dossier utilisateur
data.listing(choix_du_dossier) # listing des fichiers shape
data.dictionnaire(choix_du_dossier) # Association des fichiers à un numéro (index)


# In[ ]:


# ## Paramétrage utilisateur
## Une fois que les fichiers shape ont été associé à un numéro, l'utilisateur pourra sélectionner les fichiers shape par leur numéro (index) correspondant
# Choix de la donnée!!!!
fenetre = tk()
label = label(fenetre, text="Choix de l'info")
label.pack()
info = listbox(fenetre)
info.insert(1, "parcelle")
info.insert(2, "bati")
info.insert(3, "surf_hydro")
info.insert(4, "voie_ferree")
info.insert(5, "route")
info.insert(6, "enveloppe")
info.insert(7, "filtres_excluants")
info.pack()


# In[ ]:


# 1 Choix de la donnée : parcelle
print("Choix de la donnée : Parcelle")
parcelle = ""
while 1:
    choix_parcelle = int(input("Indiquez le numero de la donnée correspondant aux parcelles (BD parcellaire, Cadastre DGFiP, ...) : "))
    if choix_parcelle in dict_shp:
        prep(parcelle, choix_parcelle)
        nettoyage(parcelle)
        print("La couche parcelle a été défini!")

# 2 Choix de la donnée : bâti
print("Choix de la donnée : Bâti")
bati = ""
while 1:
    choix_bati = int(input("Indiquez le numero de la donnée correspondant aux bâti (BD parcellaire, Cadastre DGFiP, ...) : "))
    if choix_bati in dict_shp:
        prep(bati, choix_bati)
        nettoyage(bati)
        print("La couche bati a été défini!")
        break

# 3 Choix de la donnée : surface en eau
print("\nChoix de la donnée : Surface en eau")
surf_hydro = ""
while 1:
    choix_hydro = int(input("Indiquez le numero de la donnée correspondant à la surface en eau : "))
    if choix_hydro in dict_shp:
        prep(surf_hydro, choix_hydro)
        print("La couche surface en eau a été défini!")
        break

# 4 Choix de la donnée : Voie ferrée
print("\nChoix de la donnée : Voie ferrée")
voie_ferree = ""
while 1:
    choix_voie_ferree = int(input("Indiquez le numero de la donnée correspondant aux voies ferrées : "))
    if choix_voie_ferree in dict_shp:
        prep(voie_ferree, choix_voie_ferre)
        print("La couche des voies ferrées a été défini!")
        break

# 5 Choix de la donnée : Route
print("\nChoix de la donnée : Route")
route = ""
while 1:
    choix_route = int(input("Indiquez le numero de la donnée correspondant aux routes : "))
    if choix_route in dict_shp:
        prep(route, choix_route)
        print("La couche des routes a été défini!")
        break

# 6 Choix de la donnée : Enveloppe urbaine
print("\nChoix de la donnée : enveloppe urbaine")
enveloppe = ""
while 1:
    choix_enveloppe = int(input("Indiquez le numero de la donnée correspondant à l'enveloppe urbaine (ou le zonage) : "))
    if choix_enveloppe in dict_shp:
        question = input("S'agit-il d'une couche de l'enveloppe urbaine (e) ou d'un zonage (z)? Veuillez préciser e ou z : ")
        if question == "z":
            enveloppe = gpd.red_file(choix_du_dossier + "/" + dict_shp[choix_enveloppe])
            enveloppe = enveloppe.to_crs({'init':'epsg:2154'})
            enveloppe.columns = map(str.lower, enveloppe.columns)
            enveloppe = enveloppe[enveloppe["typezone"] == 'U']
            enveloppe = enveloppe[["libelle", "typezone", "destdomi", "insee", "geometry"]]
        else:
            prep(enveloppe, choix_enveloppe)
        print("La couche de l'enveloppe urbaine a été défini!")
        break

# 7 Choix de la donnée : filtres excluants (cimetière, terrains de sport, etc)
print("Choix de la donnée : Filtres excluants")
filtre_1 = ""
filtre_2 = ""
filtre_3 = ""

question_1 = input(" \n Sélectionner une donnée comme filtre exluant? : o (oui) ou n (non) \n")
if question_1 == "o":
    choix_filtre_1 = int(input("Indiquez le numero de la donnée correspondant aux filtres excluants (terrain de sport, cimetière, ...), en l'absence de filtres excluants supplémentaires appuyez sur la touche entrer: ")) # introduire la possibilité d'entrer plusieurs couches
    while 1:
        if filtre_1 in dict_shp:
            prep(filtre_1, choix_filtre_1)
            print("La couche filtre exluant n°1 a été défini!")
            break
    question_2 = input("\n Sélectionner une autre donnée comme filtre exluant? : o (oui) ou n (non) \n")
    if question_2 == "o":
        choix_filtre_2 = int(input("Indiquez le numero de la donnée correspondant aux filtres excluants (terrain de sport, cimetière, ...), en l'absence de filtres excluants supplémentaires appuyez sur la touche entrer: ")) # introduire la possibilité d'entrer plusieurs couches
        while 1:
            if filtre_1 in dict_shp:
                prep(filtre_2, choix_filtre_2)
                print("La couche filtre exluant n°2 a été défini!")
                break
        question 3 =  input("\n Sélectionner une autre donnée comme filtre exluant? : o (oui) ou n (non) \n")
        if question_3 == "o":
            choix_filtre_3 = int(input("Indiquez le numero de la donnée correspondant aux filtres excluants (terrain de sport, cimetière, ...), en l'absence de filtres excluants supplémentaires appuyez sur la touche entrer: ")) # introduire la possibilité d'entrer plusieurs couches
            while 1:
                if filtre_3 in dict_shp:
                    prep(filtre_3, choix_filtre_3)
                    print("La couche filtre exluant n°3 a été défini!")
                    break
else:
    pass


# ### Index spatial

# In[ ]:


def index_spatial(ref_geom, target_geom):
    target_geom = target_geom.unary_union
    spatial_index = ref_geom.sindex #index spatial sur les parcelles
    possible_index = list(spatial_index.intersection(target_geom.bounds)) #récupération de l'index des parcelles qui intersecte la bounding box du bati
    possible = ref_geom.iloc[sorted(possible_index)]
    precise = possible[possible.intersects(target_geom)] #récupération des parcelles qui intersecte le bati
    return(precise)


# ### Prise en compte des zones U

# In[5]:


parcelle_urbaine = gpd.overlay(parcelle, enveloppe, how ='intersection')
parcelle_urbaine.insert(0, "id_par", range(1, 1 + len(parcelle_urbaine)))
parcelle_urbaine.insert(1, "surf_par", parcelle_urbaine["geometry"].area)


# ### Prise en compte des filtre techniques

# In[6]:


filtre_centroid = ""
def suppr(filtre):
    filtre_centroid = filtre
    filtre_centroid["geometry"] = filtre.centroid
    parcelle_urbaine = parcelle_urbaine[parcelle_urbaine.disjoint(filtre_centroid.unry_union)]
# Supression des parcelles intersectant le filtre_1
if filtre_1 =! "":
    suppr(filtre_1)
else:
    pass
# Supression des parcelles intersectant le filtre_2
if filtre_2 = ! "":
    suppr(filtre_2)
else:
    pass

# Supression des parcelles intersectant le filtre_3
if filtre_3 = ! "":
    suppr(filtre_3)
else:
    pass

# Suppression des surfaces intersectant des surfaces en eau
parcelle_urbaine = gpd.overlay(parcelle_urbaine, surf_hydro, how='difference')

# Suppression des parcelles intersectant des voies ferrées
voie_ferree_buffer = voie_ferree
voie_ferree_buffer['geometry'] = voie_ferree.buffer(1) # le traitement ne foncitonne pas entre une couche ligne et une couche polygone!
parcelle_urbaine = parcelle_urbaine[parcelle_urbaine.disjoint(voie_ferree_buffer.unary_union)]


# ### Calcul du CES

# In[7]:


parcelle_urbaine = index_spatial(parcelle_urbaine, bati)

#intersection bati/parcelle urbaine
intersection = gpd.overlay(bati, parcelle_urbaine, how='intersection')

#dissolve par id_par
dissolve = intersection.dissolve(by='id_par').reset_index()
dissolve.insert(4, "surf_bat", dissolve["geometry"].area)
dissolve["surf_bat"] = dissolve["geometry"].area
dissolve.drop("geometry", axis=1, inplace=True)

#calcul du ces
ces = parcelle_urbaine.merge(dissolve, how='left', on='id_par', suffixes=('', '_y'))
ces['ces'] = ces['surf_bat']/ces['surf_par']*100
ces = ces.fillna(0)

#calcul de la forme
ces.insert(4, "shape", ((ces.boundary.length)/(2*np.sqrt(np.pi*ces["surf_par"]))))
ces.insert(5, "shape2", ((ces.boundary.length)/(np.sqrt(ces["surf_par"]))))

#nettoyage de la donnée CES
ces = ces[['id_par', 'surf_par', 'surf_bat', 'ces', 'shape', 'shape2', 'libelle', 'typezone', 'destdomi', 'insee', 'geometry']]
ces.crs = {'init':'epsg:2154'}


# ### Calcul du ces route

# In[9]:


parcelle_urbaine = index_spatial(parcelle, enveloppe)
parcelle_urbaine.insert(0, "id_par", range(1, 1 + len(parcelle_urbaine)))
parcelle_urbaine.insert(1, "surf_par", parcelle_urbaine["geometry"].area)
parcelle_urbaine.to_file("parcelle_urbaine.shp")

# buffer de 5m sur les routes
route_buffer=route
route_buffer['geometry']= route_buffer.buffer(5)

# CES des routes dans les parcelles
intersection=gpd.overlay(route_buffer, parcelle_urbaine, how='intersection')
dissolve = intersection.dissolve(by='id_par').reset_index()
dissolve.insert(2, "surf_route", dissolve["geometry"].area)
dissolve["surf_route"] = dissolve["geometry"].area
dissolve.to_file("dissolve.shp")
dissolve.drop("geometry", axis=1, inplace=True)

ces_route=parcelle_urbaine.merge(dissolve, how='left', on='id_par', suffixes=('', '_y'))
ces_route.to_file("test_ces_routeTEMP.shp")
ces_route['ces_route'] = ces_route['surf_route']/ces_route['surf_par']*100
ces_route=ces_route.fillna(0)
ces_route = ces_route[['id_par', 'surf_par', 'ces_route', 'geometry']]
ces_route.crs = {'init':'epsg:2154'}

#Selection de la voirie cadastrée (ces_route > 40%)
ces_route = ces_route[(ces_route["ces_route"] > 40)]

#Suppression du cadastre d'étude de  la voirie cadastrée sélectionnée
ces = gpd.overlay(ces, ces_route, how = "difference")

# ces.to_file("ces2.shp")
# route_buffer.to_file("route_buffer.shp")
# ces_route.to_file("test_ces_route2.shp")


# ### Information sur le CES à la commune

# In[ ]:


def info_ces(couche_ces):
    print("\n Informations sur le Coefficient d'emprise au sol de la commune \n")
    print("Coefficient d'emprise au sol moyen : " + str(mean(couche_ces["ces"])) + "%")
    print("Coefficient d'emprise au sol médian : " + str(median(couche_ces["ces"])) + "%")

info_ces(ces)


# ### Information sur les parcelles urbanisées

# In[ ]:


def info_parcelle(couche_parcelle):
    print("\n Informations sur les parcelles urbanisées de la commune \n")
    print("Superficie moyenne des parcelles urbanisées : " + str(mean(couche_parcelle["surf_par"])) + "m²")
    print("Superficie médiane des parcelles urbanisées : " + str(median(couche_parcelle["surf_par"])) + "m²")
    print("Superficie minimale des parcelles urbanisées : " + str(min(couche_parcelle["surf_par"])) + "m²")
    print("Superficie maximale des parcelles urbanisées : " + str(max(couche_parcelle["surf_par"])) + "m²")

info_parcelle(parcelle_uraine)


# ### Sélection parcelles

# In[ ]:


parcelle_vide = ces[(ces["ces"] < 0.5) & (ces["surf_par"]> surf_min_uf_non_batie) & (ces["shape"]<2.5) & (ces["shape2"]<8)]
parcelle_batie = ces[(ces["ces"]<ces_max) & (ces["ces"]> 0.5) & (ces["surf_par"]> surf_min_uf_batie)]


# ### Position du bati au sein de la parcelle

# In[ ]:


centroid_parcelle = parcelle_batie['geometry'].centroid
bati_buffer = bati['geometry'].buffer(5)
centroid_retenu = centroid_parcelle[centroid_parcelle.disjoint(bati_buffer.unary_union)]
parcelle_batie = parcelle_batie[parcelle_batie.intersects(centroid_retenu)]


# ### Desserte voirie

# In[ ]:


buffer_route = route["geometry"].buffer(desserte)
parcelle_vide = parcelle_vide[parcelle_vide.intersects(buffer_route.unary_union)]


# ### Export de la donnée

# In[ ]:


data_export = input("Indiquez le dossier de destination pour exporter les données : ")
ces.to_file(data_export + "/ces.shp")
parcelle_vide.to_file(data_export + "/dents_creuses.shp")
parcelle_batie.to_file(data_export + "/potentiel_divisible.shp")


# ### Calcul temps traitement

# In[ ]:


elapsed_time = time.process_time() - t
elapsed_time


# ### Qualification du potentiel

# In[ ]:


t2 = time.process_time()


# ### Création des couches de filtres excluants / limitants / favorisant

# In[ ]:


# paramètres utilisateurs
# hiérarchisation entre : 
#     - la proximité des équipements spécifiques (à préciser : publiques, commerciaux, sportifs, etc.)
#     - la proximité des transports (stations de métro, de bus, de gare)
#     - ...

# import automatique de la BD TOPO equipement présent dans le dossier utilisateur :
for i in os.listdir(choix_du_dossier):
    if i = "nom de la donnée des equipement de la BD TOPO":
        equipement = gpd.read_file(choix_du_dossier + "/" + i)
        equipement = equipement.to_crs({'init':'epsg:2154'})


# In[ ]:


elapsed_time2 = time.process_time() - t2
elapsed_time2

