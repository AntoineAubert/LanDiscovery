# Le script a pour but d'initier une analyse nmap afin de récupérer toutes les informations sur les serveurs connectés au réseau Advitam, 
# y compris leur système d'exploitation, leurs adresses IP et leurs adresses MAC.
# Auteur : Edouard Guidez / Antoine Aubert
# Date : 02/01/2024

# Importation des différentes bibliothèques
import subprocess
import csv
import logging
from Script_Get_Fabricant import *

# Configuration du logger
logging.basicConfig(filename='logs.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')


# Commande exécutée dans NMAP
cmd = "nmap -sS -O --defeat-rst-ratelimit --fuzzy --osscan-guess 172.16.220.0/16 192.168.0.0/16"
#cmd = "nmap -sS -O --fuzzy --osscan-guess 172.16.224.10"
# Renvoie la sortie sous forme de chaîne d'octets
logging.info('Début de la commande NMAP: '+ cmd)
returned_output = subprocess.check_output(cmd)
logging.info('Fin de la commande NMAP')
logging.info('Début du traitement de la commande NMAP')
commande = returned_output.decode(encoding='ISO-8859-1')
outputSplit = commande.split('Network Distance:')
result = []
# On parcourt la sortie de la commande NMAP
for output in outputSplit:
    try:
        tableresult = []
        # Permet de recupere le nom de la machine dans le contenue
        indexNmap = output.index('Nmap scan report')
        indexR = output.find('\r',indexNmap)
        indexParenthese = output.find('(',indexNmap)
        #S'il y a une parenthèse avant un \r dans le outpout (permet de recuperer l'ip entre parenthèse dans le nom de la machine)
        if indexR > indexParenthese :
            firstIndex = output.index('Nmap scan report') + 21
            endIndex = output.find('(',firstIndex)
            nomMachine = output[firstIndex:endIndex-1]
            print(nomMachine)
            tableresult.append(nomMachine)
        #Sinon on recupere le nom de la machine sans parenthèse
        else:
            firstIndex = output.index('Nmap scan report') + 21
            endIndex = output.find('\r',firstIndex)
            nomMachine = output[firstIndex:endIndex]
            print(nomMachine)
            tableresult.append(nomMachine)
        # Permet de recupere la MACADRESS dans le contenue
        try:
            firstIndex = output.index('MAC Address: ') + 13
            endIndex = output.find('(',firstIndex)
            macadress = output[firstIndex:endIndex-1]
            tableresult.append(macadress)
            print(macadress)
        #Si on ne trouve pas de MACADRESS on met Inconnu
        except:
            macadress="Inconnu"
            print(macadress)
            tableresult.append(macadress)

        # Permet de recupere l'OS dans le contenue en venir selectionner celui avec le plus gros pourcentage
        print('On est dans le EXCEPT OS')
        #On regarde si on trouve un OS dans le output
        if output.find('Aggressive OS guesses') != -1:
            firstIndex = output.index('Aggressive OS guesses') + 23
            endIndex = output.find('(',firstIndex)
            os = output[firstIndex:endIndex-1]
            print(os)
            #on verifie que l'os est un windows ou microoft)
            
            print(('microsoft' or 'windows') in os.lower())
            if ('microsoft' or 'windows') in os.lower():
            #Si oui on recupere la version exact du windows en wmi
                tableresult.append(get_remote_windows_version(tableresult[0]))   
            else:    
                tableresult.append(os)
        #On regarde si on trouve un OS dans le output
        elif output.find('OS details: ') != -1:
            firstIndex = output.index('OS details: ') + 12
            endIndex = output.find('\r',firstIndex + 1 )
            os = output[firstIndex:endIndex]
            print(os)
            print(('microsoft' or 'windows') in os.lower())
            if ('microsoft' or 'windows') in os.lower():
            #Si oui on recupere la version exact du windows en wmi
                tableresult.append(get_remote_windows_version(tableresult[0]))   
            else:    
                tableresult.append(os)
        #On regarde si on trouve un OS dans le output
        elif output.find('No OS matches for host')!= -1:
            tableresult.append("Inconnu")
        #On regarde si on trouve un OS dans le output
        else:
            firstIndex = output.index('OS') + 3
            endIndex = output.find('(',firstIndex)
            os = output[firstIndex:endIndex-1]
            print(os)
            tableresult.append(os)
        
        last_os = tableresult[-1]
        #IP MACHINE + FABRICANT

        # Permet de recupere l'IP dans le contenue
        indexNmap = output.index('Nmap scan report')
        indexR = output.find('\r',indexNmap)
        indexParenthese = output.find('(',indexNmap)
        #S'il y a une parenthèse avant un \r dans le outpout (permet de recuperer l'ip entre parenthèse dans le nom de la machine)
        if indexR > indexParenthese :
            firstIndex = output.index('Nmap scan report')
            intermediaire = output.find('(',firstIndex) + 1
            endIndex = output.find(')',intermediaire)
            ip = output[intermediaire:endIndex]
            print(ip)

            #On recupere le fabricant de l'ip
            #on verifie si le dernier os est un windows
            print(('microsoft' or 'windows') in os.lower())
            if ('microsoft' or 'windows') in str(last_os).lower():
                #si oui on recupere le fabricant en wmi 
                print(recuperer_nom_fabricant(ip))
                tableresult.append(recuperer_nom_fabricant(ip))
            #Si on ne trouve pas de fabricant on met Inconnu
            else:
                print('Impossible de trouver Fabricant')
                tableresult.append('Inconnu')
            tableresult.append(ip)
        #Sinon on recupere l'ip sans parenthèse
        else:
            firstIndex = output.index('Nmap scan report') + 21
            endIndex = output.find('\r',firstIndex)
            ip = output[firstIndex:endIndex]
            print(ip)
            #On recupere le fabricant de l'ip
            #on verifie si le derneir os est un windows
            print(('microsoft' or 'windows') in os.lower())
            if ('microsoft' or 'windows') in str(last_os).lower():
                #si oui on recupere l'info en wmi
                print(recuperer_nom_fabricant(ip))
                tableresult.append(recuperer_nom_fabricant(ip))
            #Si on ne trouve pas de fabricant on met Inconnu
            else:
                print('Impossible de trouver Fabricant')
                tableresult.append('Inconnu')
            tableresult.append(ip)

        #FIN IP MACHINE / FABRICANT
            
        # On ajoute les résultats dans le tableau de résultat.    
        result.append(tableresult)
        
    # Si on ne trouve pas de nom de machine, d'adresse MAC ou d'OS, on affiche un message d'erreur.
    except ValueError as error:
        print(error)
        print('not found')
logging.info('Fin du traitement de la commande NMAP')
# On affiche les résultats
logging.info('Insertion des résultats dans le fichier result.csv')
# On écrit les résultats dans le fichier csv result pour le nom de machine, adresse_Mac et l'OS de la machine.
with open('result.csv',mode='w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile,delimiter=';')
    csv_writer.writerow(['nom','adresseMac','typeEquipement',"fabricant","adresseIp","dateScan"])
    from datetime import datetime
    date = datetime.now().strftime("%Y-%m-%d")
    for ligne in result:
        csv_writer.writerow(ligne + [date])
# On affiche un message pour indiquer que l'insertion dans le fichier result.csv est terminée.
logging.info("Fin de l'insertion dans le fichier result.csv")