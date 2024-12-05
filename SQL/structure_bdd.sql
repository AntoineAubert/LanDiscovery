create database Landiscovery_bdd;
use Landiscovery_bdd;

CREATE TABLE ScanEquipement (
	id INT auto_increment NOT NULL PRIMARY KEY,
	nom varchar(35) NOT NULL,
	adresseMac varchar(17) NOT NULL,
	typeEquipement varchar(45) NOT NULL,
	fabricant varchar(35) DEFAULT 'Inconnu' NOT NULL,
	nombreConnexion INT NOT NULL,
	adresseIp varchar(15) NOT NULL,
    dateScan DATE NOT NULL
)