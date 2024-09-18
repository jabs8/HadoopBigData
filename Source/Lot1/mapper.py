#!/usr/bin/env python
"""mapper.py"""

import sys
from datetime import datetime

# On ignore l'en tete
header = True
for line in sys.stdin:
    if header:
        header = False
        continue

    # Pré-traitement (séparateur du csv et suppression des espace set des guillemets)
    line = line.strip() 
    field = line.split(',') 
    fields = [element.replace('"', '') for element in field]

    # Identification des champs de données et attribution a une clé
    codcli = int(fields[0])
    nom = fields[2]
    prenom = fields[3]    
    cpcli = fields[4]
    # extraire département de cpcli et filtrer
    if len(cpcli) == 5:
        # On vérifie le format
        if cpcli.isdigit():
            try:
                # On prend les deux premiers chiffres du code postal
                departement = int(cpcli[:2])
            except ValueError:
                continue
        else:
            continue
    elif len(cpcli) == 4:
        # On vérifie le format
        if cpcli.isdigit():
            try:
                # On prend le premier chiffre du code postal
                departement = int(cpcli[:1])
            except ValueError:
                continue
        else:
            continue
    else: continue

    ville = fields[5]

    datcde = fields[7]
    # extraire l'année de la date
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
        # Vérifier si points est négatif
        if points < 0:
            continue

    except ValueError:
        # Si points ne peut pas être converti en entier, ignorer la ligne
        continue


    # Filtre du dataset avec vérification pour éviter les None et les chaînes vides
    if not nom or not prenom or nom.strip() == '' or prenom.strip() == '':
        continue

    # On filtre sur les années et départements voulus
    filter_dep = ['53', '61', '75', '28']
    filter_year = ['2008', '2009', '2010', '2011', '2012']
    if departement not in filter_dep and year not in filter_year:
        continue

    # Calcul de la fidélité
    fidelite = int(qte*points)


    print('%s\t%s\t%s\t%i\t%s\t%i\t%i\t%i\t%i' % (nom, prenom, ville, departement, nom_objet, qte, points, codcli, fidelite))