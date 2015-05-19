## --------------------------------------
## Clients : qui passe des commandes
## --------------------------------------


## Etape 1 : Connexion / Choisir un client
## Etape 2 : Recuperer le catalogue
## Etape 3 : Creer un ou plusieurs commandes

import cx_Oracle
import random
import base.log as L
import pdb


## -------------------
## Connexion a la base
## -------------------
def connexion():
	## --------------------
	## Quelques variables
	##--------------------
	USER='adv/tiger'
	HOST='10.3.10.83'
	SID='X3TEST'

	CNX='%s@%s/%s' % (USER, HOST, SID)

	## Init connexion
	con = cx_Oracle.connect(CNX)

	## Auto commit = True
	con.autocommit=True
	return con

## ----------------------
## Choisissons un client
## ----------------------
def choose_cli(con):
	cur = con.cursor()
	cur.execute("select ID from clients")
	all_cli = cur.fetchall()
	r = random.choice(all_cli)
	cur.close()
	return int(r[0])

## ----------------------
## recup du catalogue
## ----------------------
def get_catalog(con):
	cur = con.cursor()
	cur.execute("select codpro from catalogue_client")
	all_pro = cur.fetchall()
	r = random.sample(all_pro, random.randint(1,len(all_pro)))
	r = [ x[0] for x in r ]
	cur.close()
	return r

## ------------------------------
## generation de commande client
## ------------------------------
def gnr_comcli(con, client, cde):
	cur = con.cursor()
	req_e = "insert into COMCLI values (0, SYSDATE, %s)" % client
	cur.execute(req_e)
	NCOM = cur.execute("select CCL_SEQ.currval from dual").fetchone()
	L.log("Commande No : %s " %  NCOM[0])
	n = 1
	for l in cde:
		req_l = """
		insert into LIGCLI (NUMCOM, NUMLIG, PRODUIT, QCOM, PRIX)
		values ( %s, %s, %s , %s , 0)
		""" % ( NCOM[0], n, l[0], l[1])
		#print req_l
		cur.execute(req_l)
		n += 1
	update_prix(con, NCOM[0])
	cur.close()

def update_prix(con, ncom):
	cur = con.cursor()
	req = """
	update LIGCLI 
		set LIGCLI.PRIX = (select PRIX from PRODUITS where LIGCLI.PRODUIT=PRODUITS.ID)
		where LIGCLI.NUMCOM=%s
	""" % ncom
	cur.execute(req)
	cur.close()
	

## ----------------------
## Traitement principal
## ----------------------
def compute(con):
	F = "client.py"
	L.log("Debut de %s" % F )
	L.log("Choix du client")
	client = choose_cli(con)
	L.log( "Client : %s " % client )
	catalog = get_catalog(con)
	L.log( "Catalog : %s " % catalog )
	## Combien pour chaque produit
	cde = [ (x,random.randint(1,500)) for x in catalog ]
	L.log( "Commande : %s " % cde )
	L.log( "Generation des commandes" )
	gnr_comcli(con, client, cde)
	L.log("Fin de %s" % F )


## -------------
## MAIN LOOP
## -------------
def main():
	con = connexion()
	compute(con)
	con.close()

if __name__ == '__main__':
	main()
