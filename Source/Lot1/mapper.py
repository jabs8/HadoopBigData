#!/usr/bin/env python
"""mapper.py"""

import sys
from datetime import datetime

header = True
# input comes from STDIN (standard input)
for line in sys.stdin:
    if header:
        header = False
        continue

    # Pré-traitement
    line = line.strip() 
    field = line.split(',') 
    fields = [element.replace('"', '') for element in field]
    #fields=fields.replace('"', '')

    codcli = int(fields[0])
    nom = fields[2]
    prenom = fields[3]    
    cpcli = fields[4]
    # extraire département de cpcli et filtrer
    if len(cpcli) == 5:
        if cpcli.isdigit():
            try:
                departement = int(cpcli[:2])
            except ValueError:
                continue
        else:
            continue
    elif len(cpcli) == 4:
        if cpcli.isdigit():
            try:
                departement = int(cpcli[:1])
            except ValueError:
                continue
        else:
            continue
    else: continue

    ville = fields[5]
    datcde = fields[7]
    # extraire l'année pour filtrer
    year = datcde[:4]
    qte = fields[15]
    if qte == 'NULL':
        continue
    else: qte = int(qte)
    nom_objet = fields[17]
    points = fields[20]

    # Vérifier si points est 'NULL'
    if points == 'NULL':
        continue

    try:
        # Convertir points en entier
        points = int(points)

        # Vérifier si points est négatif et le mettre à 0 si nécessaire
        if points < 0:
            continue

    except ValueError:
        # Si points ne peut pas être converti en entier, ignorer la ligne
        continue


    # Filtre du dataset avec vérification pour éviter les None et les chaînes vides
    if not nom or not prenom or nom.strip() == '' or prenom.strip() == '':
        continue

    filter_dep = ['53', '61', '75', '28']
    filter_year = ['2008', '2009', '2010', '2011', '2012']
    if departement not in filter_dep and year not in filter_year:
        continue
    
    fidelite = int(qte*points)


    print('%s\t%s\t%s\t%i\t%s\t%i\t%i\t%i\t%i' % (nom, prenom, ville, departement, nom_objet, qte, points, codcli, fidelite))