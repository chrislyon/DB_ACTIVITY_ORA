##
## generation de fichiers fixtures.sql
##

## 4 Fichiers :
## CLIENTS / PRODUITS / FOURNISSEURS / STOCK

import random


def gnr_client(nb, FMT_CLE):
	print "-- CLIENTS --"
	REQ="insert into CLIENTS values (%s, '%s');"
	for c in range(1, nb+1):
		cle = FMT_CLE % c
		print REQ % (c, cle)

def gnr_fou(nb, FMT_CLE):
	print "-- FOURNISSEURS --"
	REQ="insert into FOURNISSEURS values (%s, '%s', '%s');"
	for c in range(1, nb+1):
		cle = FMT_CLE % c
		delai = random.randint(1, 15)
		print REQ % (c, cle, delai)

def gnr_pro_stock(nb, FMT_CLE, DEPOT):
	print "-- PRODUITS --"
	REQP="insert into PRODUITS values (%s, '%s', %s);"
	REQS="insert into STOCK values ('%s', %s, %s);"
	for c in range(1, nb+1):
		cle = FMT_CLE % c
		prix = random.randint(1, 500)
		print REQP % (c, cle, prix)
		print REQS % (DEPOT, c, 0)

def run():
	NB_CLIENT = 10
	NB_PRODUIT = 100
	NB_FOURN = 10

	gnr_client(NB_CLIENT, 'CLIENT%03d' )
	gnr_fou(NB_FOURN, 'FOU%03d')
	gnr_pro_stock(NB_PRODUIT, 'PRO%04d', 'D1')


if __name__ == '__main__':
	run()
