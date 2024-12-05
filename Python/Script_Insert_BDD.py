# Description: Script python pour insérer des données dans une table MySQL à partir d'un fichier CSV
# Auteur : Edouard Guidez / Antoine Aubert
# Date : 02/01/2024

# Importation des différentes bibliothèques
import csv
import mariadb
import logging
from dotenv import load_dotenv
import os

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# Récupération des informations de connexion à partir des variables d'environnement
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = int(os.getenv('DB_PORT'))  # Conversion en entier
db_database = os.getenv('DB_DATABASE')

# Configuration du logger
logging.basicConfig(filename='logs.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf8')
logging.info('Connection à la BDD')

# Connexion à la base de données
conn = mariadb.connect(user=db_user, password=db_password, host=db_host, port=db_port, database=db_database)
cur = conn.cursor(buffered=True)

############################################### EQUIPEMENT
logging.info('Lecture du fichier result.csv')
# Ouvrez le fichier CSV pour déterminer les noms des colonnes
with open('result.csv', 'r') as fichier_csv:
    lecteur_csv = csv.reader(fichier_csv, delimiter=';')
    entetes = next(lecteur_csv)  # Récupérez l'en-tête du fichier CSV

# Affichez les noms des colonnes
print(entetes)
print(", ".join(entetes))

# Réinsérez les données en utilisant les noms de colonnes récupérés
with open('result.csv', 'r') as fichier_csv:
    lecteur_csv = csv.reader(fichier_csv, delimiter=';')
    next(lecteur_csv, None)  # Ignorez l'en-tête déjà lu
    logging.info('Insertion en BDD')
    for ligne in lecteur_csv:
        print(ligne)
        # Insérez les données dans la table
        try:
            cur.execute(f'INSERT INTO ScanEquipement ({", ".join(entetes)})  VALUES (%s, %s, %s, %s, %s, %s)', ligne)
            print('valeur ajoutée:' + ligne[0])
        # Gestion des erreurs dans les logs
        except Exception as e:
            logging.error(e)
            logging.debug("Numéro de ligne du fichier csv: " + str(lecteur_csv.line_num) + " Valeurs:" + '"' + (",").join(ligne) + '"')

############################################### FIN EQUIPEMENT
############################################### FIN SCAN

# Validez les insertions et fermez la connexion
conn.commit()
conn.close()
logging.info('Fermeture de la connexion à la BDD')
