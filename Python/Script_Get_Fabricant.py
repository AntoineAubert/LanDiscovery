#Description: Ce script permet de récupérer le nom du fabricant d'un PC distant en utilisant le module subprocess et la commande wmic.
#Auteur : Edouard Guidez / Antoine Aubert
#Date : 02/01/2024

# Importation des bibliothèques nécessaires
import subprocess
import wmi

# Fonction pour récupérer le nom du fabricant d'un PC distant
def recuperer_nom_fabricant(identifiant_pc):
    try:
        # Exécute la commande pour obtenir les informations du système d'un PC distant, que ce soit par IP ou par nom
        resultat = subprocess.check_output(['wmic', '/node:' + identifiant_pc, 'csproduct', 'get', 'vendor'], shell=True)
        # Convertit le résultat en chaîne de caractères
        resultat_str = resultat.decode()
        # Nettoie la sortie pour obtenir uniquement le nom du fabricant
        fabricant = resultat_str.split('\n')[1].strip()
        return fabricant
    except Exception as e:
        print("erreur en recuperant l'ip :")
        print(e)
        #return 'Inconnu'

# Spécifiez le nom ou l'adresse IP du PC distant
def get_remote_windows_version(remote_computer):
    try:
        # Connexion au PC distant
        conn = wmi.WMI(remote_computer)
        # Récupération de la version de Windows
        for os in conn.Win32_OperatingSystem():
            print(os.Caption, os.Version)
            return os.Caption
# Gestion des erreurs
    except Exception as e:
        print(f"Erreur: {e}")