## ----------------
## FACTURATION CLIENT
## Chris (2015)
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

	## Auto commit
	con.autocommit=False
	return con

def get_numfac(con):
	c = con.cursor()
	n = c.execute("select FCL_SEQ.nextval from dual").fetchone()
	return n[0]

def facturation_client(con):
	cur = con.cursor()
	req = """
		select to_char(DATCOM, 'MM-YY'), CLIENT, NUMCOM, NUMLIG, PRODUIT, QLIV, PRIX from A_FACTURER
		order by to_char(DATCOM, 'MM'), CLIENT, PRODUIT
	"""
	cur.execute(req)
	old_mois = None
	old_cli = None
	old_pro = None
	nb = 1
	nb_lig_fac = 1
	tot_qte = 0
	for l in cur:
		mois = l[0]
		cli = l[1]
		com = l[2]
		lig = l[3]
		pro = l[4]
		qte = l[5]
		prix = l[6]
		if old_mois <> mois or old_cli<>cli:
			if old_mois or old_cli:
				print "Commit precedente facture %s lignes" % nb
				nb_lig_fac = 0
				con.commit()
			## Creation d'une nouvelle facture
			print "Nouvelle facture mois=%s client=%s" % (mois, cli)
			print "Begin"
			con.begin()
			print "Attribution du numero"
			numfac = get_numfac(con)
			print "Creation entete"
			ent = con.cursor()
			ent.execute("insert into FACCLI ( CLIENT, DATFAC, NUMFAC ) VALUES (%s, sysdate, %s)" % (cli, numfac))
			ent.close()
			nb = 1
		old_mois = mois
		old_cli = cli
		## Generation des lignes
		print "Maj lig Commande cli lig=%10s qte=%10s tot_qte=%10s " % (nb, qte, tot_qte)
		c_lig = con.cursor()
		r_maj_lig = "update LIGCLI set NUMFAC=%s, QFAC=QCOM where NUMCOM=%s and NUMLIG=%s" % (numfac, com, lig)
		c_lig.execute(r_maj_lig)
		if old_pro and old_pro <> pro:
			print "Creation lig de facture"
			print "-- lig=%s pro=%s tot_qte=%s prix=%s tot_lig=%s" % (nb, pro, tot_qte, prix, tot_qte*prix)
			r_cr_lig = "insert into LIGFCL (NUMFAC, NUMLIG, PRIX, PRODUIT, QFAC) VALUES (%s,%s,%s,%s,%s)" % (numfac, nb_lig_fac, prix, pro, tot_qte)
			print r_cr_lig
			c_lig.execute(r_cr_lig)
			tot_qte = 0
			nb_lig_fac += 1
			c_lig.close()
		tot_qte += qte
		old_pro = pro
		nb += 1
	## fin
	con.commit()
	cur.close()



## ----------------------
## Traitement principal
## ----------------------
def compute(con):
	F = __file__
	L.log( "Debut de %s " % F)
	L.log( "Connexion " )
	con = connexion()
	facturation_client(con)
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
