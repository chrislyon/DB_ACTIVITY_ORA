## -----------------------
## Faire les livraisons
## -----------------------

## Attention plantage si pas de STOCK
## devrait generer une erreur

## Etape 1 : generer les BL
## Etape 2 : allouer en fonction du stock
## Etape 3 : Valider les BL

import cx_Oracle
import pdb

USER='adv/tiger'
HOST='10.3.10.83'
SID='X3TEST'

CNX='%s@%s/%s' % (USER, HOST, SID)

## Init connexion
con = cx_Oracle.connect(CNX)
print con.version

## Auto commit = True
con.autocommit=True

##
## Consultation du STOCK d'un produit
##
def get_stock_pro(pro):
	cur = con.cursor()
	req = """
		select QSTOCK from STOCK where PRODUIT=%s and DEPOT='D1'
	""" % pro
	cur.execute(req)
	r = cur.fetchone()
	cur.close()
	return r[0]

## ------------------------------------
## Allocation d'un ligne de commande
## Pas de controle
## ------------------------------------
def alloc_lig_com(ncom, lig, p, qcom, depot='D1'):
	## Mise a jour ligne de commande
	r1 = "update LIGCLI set QLIV=%s where NUMCOM=%s and NUMLIG=%s" % (qcom, ncom, lig)
	r2 = "update stock set QSTOCK=QSTOCK-%s where PRODUIT=%s and DEPOT='%s'" % (qcom, p, depot)
	cur = con.cursor()
	print "R1 ", cur.execute(r1)
	print "R2 ", cur.execute(r2)
	cur.close()

## --------------------------------------------
## Allocation d'un produit
## Recherche des lignes de commande a allouer
## si stock suffisant alors allocation
## --------------------------------------------
def bl_alloc(pro):
	stock = get_stock_pro(pro)
	print "Produit = %s stock = %s " % (pro, stock)
	## Recherche des lignes a allouer avec ce produit
	cur = con.cursor()
	req = """
		select * from BL_ALIV where PRODUIT=%s
	""" % pro
	cur.execute(req)
	for l in cur:
		ncom = l[0]
		lig = l[1]
		p = l[2]
		qcom = int(l[3])
		print "Com %s Lig %s Produit=%s " % (ncom, lig, p),
		if (stock-qcom) >= 0 :
			stock -= qcom
			print "Allocation stock=%s qcom=%s" % (stock, qcom)
			alloc_lig_com(ncom, lig, p, qcom)
		else:
			print "Non alloue stock=%s qcom=%s" % (stock, qcom)
	print "========= Stock restant : %s " % stock

## -------------
## MAIN LOOP
## -------------
cur = con.cursor()
req = """
	select distinct produit from BL_ALIV
"""
cur.execute(req)
for pro in cur:
	print "Produit : %s " % pro
	bl_alloc(pro[0])

## -------
## Final
## -------
## Verifier que les commandes totalement livrees soit flagges

cur.close()
con.close()
