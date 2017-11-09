#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

# Apenas uma funçao que adiciona uma linea no arquivo "fichier-test.csv"
# uma linea sendo as coordenadas (latitudas, longituda) de um novo ponto calculado pela soluçao

import csv


def add_entry(lat,lon):
	cr = csv.reader(open("fichier-test.csv".encode('utf-8'),"rb")) 
	datalist  = list(cr) 
	c = csv.writer(open("fichier-test.csv".encode('utf-8'),"wb"))
	c.writerows(datalist + [[lat,lon]])


print("latituda ?")
lat = input()
print("longituda ?")
lon = input()

add_entry(lat,lon)


#démarrer un script python avec des arguments :
#importer sys
#remplir la variable/liste sys.argv avec dans l'ordre :
#le nom du script
#puis les arguments 1 par 1
#ensuite : execfile("nom_du_script.py")

#autre méthode (type parallélisation) :
#import os
#os.system("nom_du_script.py arg1 arg2")