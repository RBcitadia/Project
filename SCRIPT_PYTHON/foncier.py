
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


t = time.process_time()
get_ipython().magic('matplotlib notebook')


# ### Paramètres utilisateur

# In[2]:


# #parcelle non bâtie
# desserte = float(input("Distance en mètre entre la voirie et l'unité foncière non bâtie"))
# surf_min_parcelle_non_batie = float(input("surface minimum des parcelles non bâties"))

# #parcelle bâtie
# ces_max = float(input("CES maximum des grandes parcelles bâties"))
# surf_min_parcelle_batie = float(input("surface minimum des grandes parcelles bâties"))

desserte = 50
surf_min_parcelle_non_batie = 500
ces_max = 10
surf_min_parcelle_batie = 2000


# ### Import des données

# In[3]:

# ## Dossier de données utilisateur

#data = raw_input("Indiquez le chemin du dossier contenant les données : ")
#data = "C:/Users/Citadia/Desktop/DEV/foncier/data/"
#data = raw_input("Indiquez le chemin du dossier contenant les données : ")
import os
data = "C:/Users/remi_/foncier"

def shapefile(pathname): ## fonction permettant de placer les fichiers shape du dossier dans la liste "donnee"
    donnee = []
    for shape in os.listdir(pathname):
        if shape.endswith('.shp'):
            donnee.append(shape)
        else:
            pass
    print(donnee) 

shapefile(data)    # Application de la fonction "shapefile" sur le dossier utilisateur

# ## Etablissement d'un dictionnaire pour guider l'utilisateur dans le choix des données à utiliser

index = [] # Création de la liste d'index du dictionnaire
i = 1
for shp in donnee: # Création d'une liste d'index pour le dictionnaire correspondant au nombre de fichier présent dans le dossier data utilisateur
    index.append(y)
    i = i + 1

dict_shp = {} # Création du dictionnaire
y = 0
for x in index: # Association des listes "index" et "donnee" en dictionnaire
    dict_shp[x] = donnee[y]
    y = y + 1
    print(dict_shp[y])

# ## Paramétrage utilisateur

'''from sys import version
 
print("1.Zonage CNIG")
print("2.Enveloppe urbaine")
while 1:
    reponse = input("Choisissez 1 ou 2: ")
    if reponse in ['1', '2']:
        break
    else:
        print ("Choix incorrect !")
if reponse == 1 :
    cadastre = zonage
else: cadastre = enveloppe'''
    
# data_parcelle = int(input("Indiquez le numero de la donnée correspondant aux parcelles (BD parcellaire, Cadastre DGFiP, ...) : "))
# data_bati = int(input("Indiquez le numero de la donnée correspondant au Bâti : "))
# data_filtre_excluant = int(input("Indiquez le ou les numéros des données correspondant aux filtres excluants : "))


##parcelle = gpd.read_file(r"C:\Users\Citadia\Desktop\DEV\foncier\data\PARCELLE_region.shp")
# 
data_parcelle = data + "uf.shp"
parcelle = gpd.read_file(data_parcelle)

data_bati = data + "BATI_region.shp"
bati = gpd.read_file(data_bati)

#zonage CNIG avec un champ TYPEZONE
data_zonage = data + "ZONE U PLUi_ENNEZAT.shp"
zonage = gpd.read_file(data_zonage)

data_cimetiere = data + "BD_TOPO_ENNEZAT_cimetiere_2015_01_limagneennezat_2154.shp"
cimetiere = gpd.read_file(data_cimetiere)
data_terrain_sport = data + "BD_TOPO_ENNEZAT_terrainsport_2015_01_limagneennezat_2154.shp"
terrain_sport = gpd.read_file(data_terrain_sport)
data_surf_hydro = data + "BD_TOPO_ENNEZAT_surfaceeau_2015_01_limagneennezat_2154.shp"
surf_hydro = gpd.read_file(data_surf_hydro)
data_route = data + "AXE_ROUTIER_polyline.shp"
route = gpd.read_file(data_route)
data_voie_ferree = data + "BD_TOPO_ENNEZAT_tronconvoieferree_2015_01_limagneennezat_2154.shp"
voie_ferree = gpd.read_file(data_voie_ferree)

# ### Nettoyage de la donnée

# In[4]:

def nettoyage(couche):
    couche = couche.to_crs({'init':'epsg:2154'})
    couche = couche[["geometry"]]
    
nettoyage(parcelle)
parcelle = parcelle[parcelle["geometry"].notnull()]
parcelle = parcelle[parcelle["geometry"].is_valid]

nettoyage(bati)
bati = bati[bati["geometry"].notnull()]
bati = bati[bati["geometry"].is_valid]

zonage = zonage.to_crs({'init':'epsg:2154'})
zonage.columns = map(str.lower, zonage.columns)
zonage = zonage[zonage["typezone"] == 'U']
zonage = zonage[["libelle", "typezone", "destdomi", "insee", "geometry"]]

nettoyage(cimetiere) 
nettoyage(terrain_sport)
nettoyage(route)
nettoyage(surf_hydro)
nettoyage(voie_ferree)

# ### Index spatial

# In[5]:


# def index_spatial(ref_geom, target_geom):
#     target_geom = target_geom.unary_union
#     spatial_index = ref_geom.sindex #index spatial sur les parcelles
#     possible_index = list(spatial_index.intersection(target_geom.bounds)) #récupération de l'index des parcelles qui intersecte la bounding box du bati
#     possible = ref_geom.iloc[sorted(possible_index)]
#     precise = possible[possible.intersects(target_geom)] #récupération des parcelles qui intersecte le bati
#     return(precise)


# ### Prise en compte des zones U

# In[6]:


parcelle_urbaine = gpd.overlay(parcelle, zonage, how ='intersection')
parcelle_urbaine.insert(0, "id_par", range(1, 1 + len(parcelle_urbaine)))
parcelle_urbaine.insert(1, "surf_par", parcelle_urbaine["geometry"].area)


# ### Prise en compte des filtre techniques

# In[7]:


# Supression des parcelles intersectant un cimetiere
cimetiere_centroid = cimetiere
cimetiere_centroid['geometry'] = cimetiere.centroid
parcelle_urbaine = parcelle_urbaine[parcelle_urbaine.disjoint(cimetiere_centroid.unary_union)]

# Supression des parcelles intersectant un terrain de sport
terrain_sport_centroid = terrain_sport
terrain_sport_centroid['geometry'] = terrain_sport.centroid
parcelle_urbaine = parcelle_urbaine[parcelle_urbaine.disjoint(terrain_sport_centroid.unary_union)]

# Suppression des surfaces intersectant des surfaces en eau
parcelle_urbaine = gpd.overlay(parcelle_urbaine, surf_hydro, how='difference')

# Suppression des parcelles intersectant des voies ferrées
voie_ferree_buffer = voie_ferree
voie_ferree_buffer['geometry'] = voie_ferree.buffer(1) # le traitement ne foncitonne pas entre une couche ligne et une couche polygone!
parcelle_urbaine = parcelle_urbaine[parcelle_urbaine.disjoint(voie_ferree_buffer.unary_union)]

# ### Calcul du CES

# In[8]:


# parcelle_urbaine = index_spatial(parcelle_urbaine, bati)

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

#nettoyer la donnée
ces = ces[['id_par', 'surf_par', 'surf_bat', 'ces', 'shape', 'shape2', 'libelle', 'typezone', 'destdomi', 'insee', 'geometry']]
ces.crs = {'init':'epsg:2154'}

# Info sur le CES à la commune

from numpy import mean
from numpy import median

ces_moyen = mean(ces["ces"])
ces_median = median(ces["ces"])
ces_min = min(ces["ces"])
ces_max = max(ces["ces"])
print("Informations sur le Coefficient d'emprise au sol de la commune")
print("Coefficient d'emprise au sol moyen : " + str(ces_moyen) + "%")
print("Coefficient d'emprise au sol médian : " + str(ces_median) + "%")
print("Coefficient d'emprise au sol minimum : " + str(ces_min) + "%")
print("Coefficient d'emprise au sol maximum : " + str(ces_max) + "%")

# Info sur les parcelles urbanisées
parcelle_urbaine_moyenne = mean(parcelle_urbaine[("surf_par")])
parcelle_urbaine_median = median(parcelle_urbaine["surf_par"])
parcelle_urbaine_min = min(parcelle_urbaine["surf_par"])
parcelle_urbaine_max = max(parcelle_urbaine["surf_par"])
print("Informations sur les parcelles urbanisées de la commune")
print("Superficie moyenne des parcelles urbanisées : " + str(parcelle_urbaine_moyenne) + "m²")
print("Superficie médiane des parcelles urbanisées : " + str(parcelle_urbaine_median) + "m²")
print("Superficie minimale des parcelles urbanisées : " + str(parcelle_urbaine_min) + "m²")
print("Superficie maximale des parcelles urbanisées : " + str(parcelle_urbaine_max) + "m²")


# ### Sélection parcelles

# In[9]:


parcelle_vide = ces[(ces["ces"] < 0.5) & (ces["surf_par"]> surf_min_parcelle_non_batie) & (ces["shape"]<2.5) & (ces["shape2"]<8)]
parcelle_batie = ces[(ces["ces"]<ces_max) & (ces["ces"]> 0.5) & (ces["surf_par"]> surf_min_parcelle_batie)]


# ### Position du bati au sein de la parcelle

# In[10]:


centroid_parcelle = parcelle_batie['geometry'].centroid
bati_buffer = bati['geometry'].buffer(5)
centroid_retenu = centroid_parcelle[centroid_parcelle.disjoint(bati_buffer.unary_union)]
parcelle_batie = parcelle_batie[parcelle_batie.intersects(centroid_retenu)]


# ### Desserte voirie

# In[11]:


buffer_route = route["geometry"].buffer(desserte)
parcelle_vide = parcelle_vide[parcelle_vide.intersects(buffer_route.unary_union)]


# ### Export de la donnée

# In[12]:

# data_export = raw_input("Indiquez le dossier de destination pour exporter les données : ")
data_export = "C:/Users/Citadia/Desktop/DEV/foncier/"
ces.to_file(data_export + "ces.shp")
parcelle_vide.to_file(data_export + "uf_vide3.shp")
parcelle_batie.to_file(data_export + "uf_batie.shp")


# ### Calcul temps traitement

# In[13]:


elapsed_time = time.process_time() - t
elapsed_time


# ### Qualification du potentiel

# In[14]:


t2 = time.process_time()


# ### Création des couches de filtres excluants / limitants / favorisant

# In[15]:






# In[ ]:


elapsed_time2 = time.process_time() - t2
elapsed_time2

