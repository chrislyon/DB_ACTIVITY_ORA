## ----------------------
## Commande fournisseurs
## ----------------------


## Etape 1 : recuperer la liste des besoins
## Etape 2 : Pour chaque produit selectionner 1 ou plusieurs fou
## Etape 3 : stocker les commandes par fournisseurs 
## Etape 4 : generer les commandes 

import cx_Oracle
import random
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

## ------------------------------
## generation de commande Fourn
## ------------------------------
def gnr_comfou(con, fou, cde):
	cur = con.cursor()
	NCOM = cur.execute("select LFO_SEQ.nextval from dual").fetchone()
	print NCOM[0]
	DELAI = cur.execute("select DELAI from fournisseurs where id=%s" % fou ).fetchone()
	n = 1
	for l in cde:
		req_l = """
		insert into LIGFOU (NUMCOM, NUMLIG, PRODUIT, FOU, QCOM, DPREVU, PRIX)
		values ( %s, %s, %s , %s , %s, sysdate+%s, 0)
		""" % ( NCOM[0], n, l[0], fou, l[1], DELAI[0])
		print req_l
		cur.execute(req_l)
		n += 1
	cur.close()

## ----------------------
## Choisissons un Fourn
## ----------------------
def choose_fou(con):
	cur = con.cursor()
	cur.execute("select ID from fournisseurs")
	all = cur.fetchall()
	r = random.choice(all)
	cur.close()
	return int(r[0])
	
## ----------------------
## Calcul des besoins
## ----------------------
def get_besoins(con):
	cur = con.cursor()
	cur.execute("select * from qte_a_commander")
	r = cur.fetchall()
	cur.close()
	return r

## -----------------------------
## Preparation des commandes
## -----------------------------
def prep_cmd_fou(con):
	C = {}
	cur = con.cursor()
	cur.execute("select ID from fournisseurs")
	for f in cur.fetchall():
		C[f[0]] = []
	return C

## ----------------------
## Traitement principal
## ----------------------
def compute(con):
	print "Debut du traitement "
	print "Calcul des besoins"
	besoins = get_besoins(con)
	print besoins
	print "Preparation ..."
	Cdes = prep_cmd_fou(con)
	print Cdes
	for b in besoins:
		fou = choose_fou(con)
		print "Cde chez %s : %s " % (fou, b)
		Cdes[fou].append(b)
	print "Liste des commandes a passer"
	for k,v in Cdes.items():
		print "Fou = %s / v = %s " % (k,v)
		gnr_comfou(con, k, v)
	print "Fin du traitement"


## -------------
## MAIN LOOP
## -------------
def main():
	con = connexion()
	compute(con)
	con.close()

if __name__ == '__main__':
	main()
