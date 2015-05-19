## ----------------
## SCRIPTS DE BASE
## ----------------


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
## Traitement principal
## ----------------------
def compute(con):
	F = "base.py"
	L.log( "Debut de %s " % F)
	L.log( "Fin de %s" % F)


## -------------
## MAIN LOOP
## -------------
def main():
	con = connexion()
	compute(con)
	con.close()

if __name__ == '__main__':
	main()
