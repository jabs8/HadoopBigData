import sys
import heapq
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import sys
from collections import defaultdict

# Dictionnaire pour stocker la fidélité cumulée et les informations des clients
# Chaque client a un dictionnaire d'objets qui est un defaultdict de dict pour stocker les quantités et points
clients = defaultdict(lambda: {
    'fidélité': 0,
    'nom': '',
    'prenom': '',
    'ville': '',
    'departement': '',
    'objets': defaultdict(lambda: {'quantite': 0, 'points': 0})  # Note ici que 'objets' est un defaultdict
})

# Lire les lignes du mapper
for line in sys.stdin:
    # Supposons que le mapper envoie des informations séparées par des tabulations
    # Format : client_id \t nom \t prénom \t ville \t département \t nom_objet \t quantité \t fidélité
    data = line.strip().split('\t')

    if len(data) == 9:
        nom = data[0]
        prenom = data[1]
        ville = data[2]
        departement = data[3]
        nom_objet = data[4]
        quantite = int(data[5])
        client_id = data[7]
        fidelite = float(data[8])  # La fidélité est la somme (points * quantité)

        # Mettre à jour les informations du client dans le dictionnaire
        clients[client_id]['fidélité'] += fidelite
        clients[client_id]['nom'] = nom
        clients[client_id]['prenom'] = prenom
        clients[client_id]['ville'] = ville
        clients[client_id]['departement'] = departement

        # Cumul des quantités et des points pour chaque objet commandé par le client
        clients[client_id]['objets'][nom_objet]['quantite'] += quantite
        clients[client_id]['objets'][nom_objet]['points'] += fidelite

# Trier les clients par fidélité décroissante
clients_tries = sorted(clients.items(), key=lambda x: x[1]['fidélité'], reverse=True)

# Ne prendre que les 10 clients les plus fidèles
top_10_clients = clients_tries[:10]

# Préparer les données pour le DataFrame
data = []
for client_id, infos in top_10_clients:
    score_total = infos['fidélité']
    nom = infos['nom']
    prenom = infos['prenom']
    ville = infos['ville']
    departement = infos['departement']
    objets = infos['objets']

    # Pour chaque produit commandé par le client (regroupé), on ajoute une ligne dans les données
    for nom_objet, details in objets.items():
        quantite_totale = details['quantite']
        points = details['points']

        data.append([
            nom,
            prenom,
            ville,
            departement,
            nom_objet,
            quantite_totale
        ])

# Création du DataFrame
df = pd.DataFrame(data, columns=[
    "Nom", "Prénom", "Ville", "Département", "Nom de l'objet", "Quantité commandée"
])

# Exporter le DataFrame en fichier Excel
output_excel_file = '/datavolume1/top_10_clients_fideles.xlsx'  # Modifier selon le chemin de sortie souhaité
df.to_excel(output_excel_file, index=False)

print("Le fichier Excel 'top_10_clients_fideles.xlsx' a ete cree avec les details des produits pour les 10 clients les plus fideles.")

# Création des graphiques
output_pdf_file = '/datavolume1/repartition_produits_par_client.pdf'

with PdfPages(output_pdf_file) as pdf:
    for client in df[['Nom', 'Prénom']].drop_duplicates().values:
        nom, prenom = client
        client_data = df[(df['Nom'] == nom) & (df['Prénom'] == prenom)]

        # Calculer la répartition des produits
        product_distribution = client_data.groupby('Nom de l\'objet')['Quantité commandée'].sum()

        # Créer le graphique
        plt.figure(figsize=(10, 8))
        plt.pie(product_distribution.values, labels=product_distribution.index, autopct='%1.1f%%')
        plt.title("Repartition des produits commandes par {} {}".format(prenom, nom))
        plt.axis('equal')

        # Ajouter le graphique au PDF
        pdf.savefig()
        plt.close()

print("Les graphiques de repartition des produits ont ete crees et exportes dans '{}'".format(output_pdf_file))

