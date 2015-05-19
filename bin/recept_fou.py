## ----------------
## SCRIPTS DE BASE
## ----------------


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

## ----------------------------
## Reception de commande fou
## ----------------------------
def recept_a_faire(con):
	cur = con.cursor()
	qr = cur.execute("select * from cde_fou_a_receptionner").fetchall()
	cur.close()
	return qr

def reception(con, row):
	cur = con.cursor()
	NCOM = row[0]
	NLIG = row[1]
	PRO = row[2]
	QREC = row[3]
	cur.execute(" update LIGFOU set QRECU=%s where NUMCOM=%s and NUMLIG=%s " % (QREC, NCOM, NLIG) )
	cur.execute(" update STOCK set QSTOCK = QSTOCK + %s where PRODUIT=%s " % (QREC, PRO) )
	print "reception de %s/%s Produit = %s QREC=%s " % ( NCOM, NLIG, PRO, QREC )
	cur.close()

## ----------------------
## Traitement principal
## ----------------------
def compute(con):
	print "Debut du traitement "
	for l in recept_a_faire(con):
		reception(con, l)
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
