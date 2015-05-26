-- -------------------
-- FACTURES CLIENT
-- -------------------

CREATE TABLE FACCLI (
	NUMFAC NUMBER(8) NOT NULL,
	DATFAC DATE NOT NULL,
	CLIENT NUMBER(8) NOT NULL
	);

ALTER TABLE FACCLI ADD (
	CONSTRAINT fcl_k1 PRIMARY KEY (NUMFAC)
);

ALTER TABLE FACCLI
	ADD CONSTRAINT fcl_cli
	  FOREIGN KEY ( CLIENT ) REFERENCES CLIENTS(ID);

CREATE SEQUENCE FCL_SEQ START WITH 1;

CREATE TABLE LIGFCL (
	NUMFAC NUMBER(8) NOT NULL,
	NUMLIG NUMBER(2) NOT NULL,
	PRODUIT NUMBER(8) NOT NULL,
	QFAC NUMBER(5) DEFAULT 0 NOT NULL,
	PRIX NUMBER(8) NOT NULL,
	NUMCOM NUMBER(8) NOT NULL,
	NCOMLIG NUMBER(2) NOT NULL
	);

ALTER TABLE LIGFCL ADD (
	CONSTRAINT FCL_UNIQ UNIQUE (NUMFAC, NUMLIG)
		);
ALTER TABLE LIGFCL
	ADD CONSTRAINT faccli_ligfcl
	  FOREIGN KEY ( NUMFAC ) REFERENCES FACCLI(NUMFAC);

ALTER TABLE LIGFCL
	ADD CONSTRAINT flcl_pro
	  FOREIGN KEY ( PRODUIT ) REFERENCES PRODUITS(ID);

