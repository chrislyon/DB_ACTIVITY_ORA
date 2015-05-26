-- ----------------------
-- SCHEMA DE TEST
-- ----------------------

-- Correction : QTE A Commander ne tenait pas compte du stock en cours

-- ----------------
-- CLIENTS
-- ----------------

CREATE TABLE CLIENTS (
	ID          NUMBER(8)    NOT NULL,
	NOM  		VARCHAR2(20)  NOT NULL
	);

ALTER TABLE CLIENTS ADD (
CONSTRAINT cli_k1 PRIMARY KEY (ID));

CREATE SEQUENCE CLI_SEQ;

CREATE OR REPLACE TRIGGER CLIENT_ID
BEFORE INSERT ON CLIENTS
FOR EACH ROW

BEGIN
SELECT CLI_SEQ.NEXTVAL
INTO   :new.id
FROM   dual;
END;
/

-- ----------------
-- PRODUITS
-- ----------------

CREATE TABLE PRODUITS (
	ID          NUMBER(8)    NOT NULL,
	DESIG  		VARCHAR2(20)  NOT NULL,
	PRIX		NUMBER(8)  NOT NULL
	);

ALTER TABLE PRODUITS ADD (
CONSTRAINT pro_k1 PRIMARY KEY (ID));

CREATE SEQUENCE PRO_SEQ;

CREATE OR REPLACE TRIGGER PRODUIT_ID
BEFORE INSERT ON PRODUITS
FOR EACH ROW

BEGIN
SELECT PRO_SEQ.NEXTVAL
INTO   :new.id
FROM   dual;
END;
/

-- ----------------
-- FOURNISSEUR
-- ----------------

CREATE TABLE FOURNISSEURS (
	ID          NUMBER(8)    NOT NULL,
	NOM  		VARCHAR2(20)  NOT NULL,
	DELAI		NUMBER(2) DEFAULT 7 NOT NULL
	);

ALTER TABLE FOURNISSEURS ADD (
CONSTRAINT fou_k1 PRIMARY KEY (ID));

CREATE SEQUENCE FOU_SEQ;

CREATE OR REPLACE TRIGGER FOURN_ID
BEFORE INSERT ON FOURNISSEURS
FOR EACH ROW

BEGIN
SELECT FOU_SEQ.NEXTVAL
INTO   :new.id
FROM   dual;
END;
/

-- TODO : TARIF FOU

-- ----------------
-- STOCK / DEPOT
-- ----------------
create table STOCK (
	DEPOT VARCHAR(10) NOT NULL,
	PRODUIT NUMBER(8) NOT NULL,
	QSTOCK NUMBER(6) NOT NULL
);

ALTER TABLE STOCK
	ADD CONSTRAINT stk_pro
	  FOREIGN KEY ( PRODUIT ) REFERENCES PRODUITS(ID);

ALTER TABLE STOCK ADD (
	CONSTRAINT STK_UNIQ UNIQUE (DEPOT, PRODUIT)
		);
-- -------------------
-- COMMANDES CLIENT
-- -------------------

-- TODO : ajout totalement livre

CREATE TABLE COMCLI (
	NUMCOM NUMBER(8) NOT NULL,
	DATCOM DATE NOT NULL,
	CLIENT NUMBER(8) NOT NULL,
	FACTURE NUMBER(8) default 0
	);

ALTER TABLE COMCLI ADD (
	CONSTRAINT ccl_k1 PRIMARY KEY (NUMCOM)
);

ALTER TABLE COMCLI
	ADD CONSTRAINT ccl_cli
	  FOREIGN KEY ( CLIENT ) REFERENCES CLIENTS(ID);

CREATE SEQUENCE CCL_SEQ START WITH 1000;

CREATE OR REPLACE TRIGGER COMCLI_NUM
BEFORE INSERT ON COMCLI
FOR EACH ROW

BEGIN
SELECT CCL_SEQ.NEXTVAL
INTO   :new.NUMCOM
FROM   dual;
END;
/

CREATE TABLE LIGCLI (
	NUMCOM NUMBER(8) NOT NULL,
	NUMLIG NUMBER(2) NOT NULL,
	PRODUIT NUMBER(8) NOT NULL,
	QCOM  NUMBER(5) NOT NULL,
	PRIX NUMBER(8) NOT NULL,
	QLIV NUMBER(5) DEFAULT 0 NOT NULL,
	QFAC NUMBER(5) DEFAULT 0 NOT NULL
	);

ALTER TABLE LIGCLI ADD (
	CONSTRAINT LCL_UNIQ UNIQUE (NUMCOM, NUMLIG)
		);
ALTER TABLE LIGCLI
	ADD CONSTRAINT lcl_ccl 
	  FOREIGN KEY ( NUMCOM ) REFERENCES COMCLI(NUMCOM);

ALTER TABLE LIGCLI
	ADD CONSTRAINT lcl_pro
	  FOREIGN KEY ( PRODUIT ) REFERENCES PRODUITS(ID);

-- --------------------------
-- COMMANDE FOURNISSEUR
-- --------------------------
CREATE SEQUENCE LFO_SEQ START WITH 5000;

CREATE TABLE LIGFOU (
	NUMCOM NUMBER(8) NOT NULL,
	NUMLIG NUMBER(2) NOT NULL,
	FOU NUMBER(8) NOT NULL,
	PRODUIT NUMBER(8) NOT NULL,
	QCOM  NUMBER(5) NOT NULL,
	PRIX NUMBER(8) NOT NULL,
	DPREVU DATE NOT NULL,
	QRECU NUMBER(5) DEFAULT 0 NOT NULL
	);

ALTER TABLE LIGFOU ADD (
	CONSTRAINT LFO_UNIQ UNIQUE (NUMCOM, NUMLIG)
		);
ALTER TABLE LIGFOU
	ADD CONSTRAINT lfo_pro
	  FOREIGN KEY ( PRODUIT ) REFERENCES PRODUITS(ID);

ALTER TABLE LIGFOU
	ADD CONSTRAINT lfo_fou
	  FOREIGN KEY ( FOU ) REFERENCES FOURNISSEURS(ID);

--
-- Petit test avec une vue
--
create or replace view commandes
as select 
	LIGCLI.NUMCOM,
	LIGCLI.NUMLIG,
	CLIENTS.NOM,
	COMCLI.DATCOM,
	PRODUITS.DESIG,
	LIGCLI.QCOM,
	LIGCLI.PRIX
from COMCLI, LIGCLI, PRODUITS, CLIENTS
where 
	COMCLI.NUMCOM = LIGCLI.NUMCOM
	AND COMCLI.CLIENT = CLIENTS.ID
	AND LIGCLI.PRODUIT = PRODUITS.ID
	;

-- ------------------------
-- Mise a jour des prix
-- ------------------------
update LIGCLI set LIGCLI.PRIX = (select PRIX from PRODUITS where LIGCLI.PRODUIT=PRODUITS.ID);

--- ----------------------------------
--- Utile pour la generation des BL
--- ----------------------------------
create view BL_ALIV
as select 
	NUMCOM, NUMLIG, PRODUIT, QCOM, 0 "QLIV"
from LIGCLI
where QCOM > QLIV
order by NUMCOM, NUMLIG
;

-- --------------------
-- Catalogue client 
-- --------------------
create or replace view catalogue_client
as select
ID "CODPRO", DESIG "DESIGNATION", PRIX "PRIX"
from PRODUITS
;

-- --------------------
-- Calcul des besoins 
-- --------------------
-- create or replace view qte_a_commander
-- as select PRODUIT, sum(QCOM-QLIV) "QACOM"
-- from ADV.LIGCLI
-- where QCOM-QLIV > 0
-- group by PRODUIT
-- order by PRODUIT
CREATE OR REPLACE FORCE VIEW QTE_A_COMMANDER ( PRODUIT, QACOM)
	  AS
SELECT L.PRODUIT, SUM (QCOM - QLIV) "QACOM"
FROM ADV.LIGCLI L, ADV.STOCK S
WHERE  L.PRODUIT = S.PRODUIT and DEPOT='D1' and QCOM - QLIV -QSTOCK > 0
GROUP BY L.PRODUIT
ORDER BY L.PRODUIT;

-- -------------------------------
-- Commande fou a receptionner
-- -------------------------------
create or replace view cde_fou_a_receptionner
as select NUMCOM, NUMLIG, PRODUIT, QCOM-QRECU "QARCPT", DPREVU
from ADV.LIGFOU
Where QCOM-QRECU > 0
AND to_char(DPREVU, 'YYMMDD') <= to_char(SYSDATE,'YYMMDD')
order by PRODUIT
;

-- -----------------------
-- COMMANDE A FACTURER
-- -----------------------
CREATE OR REPLACE FORCE VIEW ADV.A_FACTURER
( DATCOM, CLIENT, NUMCOM, NUMLIG, QLIV, PRIX )
AS
SELECT DATCOM, CLIENT, COMCLI.NUMCOM, NUMLIG, QLIV, PRIX
FROM ADV.COMCLI INNER JOIN ADV.LIGCLI ON (COMCLI.NUMCOM = LIGCLI.NUMCOM)
WHERE QFAC = 0 AND QCOM = QLIV
ORDER BY DATCOM, CLIENT, COMCLI.NUMCOM, NUMLIG;


exit
