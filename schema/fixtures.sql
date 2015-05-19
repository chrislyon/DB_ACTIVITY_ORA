-- ----------------------
-- SCHEMA DE TEST
-- ----------------------

-- ----------------
-- CLIENTS
-- ----------------

insert into CLIENTS VALUES ( 0, 'CLIENT1' );
insert into CLIENTS VALUES ( 0, 'CLIENT2' );
insert into CLIENTS VALUES ( 0, 'CLIENT3' );
insert into CLIENTS VALUES ( 0, 'CLIENT4' );
insert into CLIENTS VALUES ( 0, 'CLIENT5' );
insert into CLIENTS VALUES ( 0, 'CLIENT6' );
insert into CLIENTS VALUES ( 0, 'CLIENT7' );
insert into CLIENTS VALUES ( 0, 'CLIENT8' );
insert into CLIENTS VALUES ( 0, 'CLIENT9' );
insert into CLIENTS VALUES ( 0, 'CLIENT0' );

-- ----------------
-- PRODUITS
-- ----------------

insert into PRODUITS values (0, 'PRODUIT1', 50);
insert into PRODUITS values (0, 'PRODUIT2', 100);
insert into PRODUITS values (0, 'PRODUIT3', 120);
insert into PRODUITS values (0, 'PRODUIT4', 20);
insert into PRODUITS values (0, 'PRODUIT5', 170);
insert into PRODUITS values (0, 'PRODUIT6', 30);
insert into PRODUITS values (0, 'PRODUIT7', 110);
insert into PRODUITS values (0, 'PRODUIT8', 100);
insert into PRODUITS values (0, 'PRODUIT9', 80);
insert into PRODUITS values (0, 'PRODUIT0', 180);

-- ----------------
-- FOURNISSEUR
-- ----------------
insert into FOURNISSEURS VALUES ( 0, 'FOU1', 5 );
insert into FOURNISSEURS VALUES ( 0, 'FOU2', 2 );
insert into FOURNISSEURS VALUES ( 0, 'FOU3', 0 );
insert into FOURNISSEURS VALUES ( 0, 'FOU4', 0 );
insert into FOURNISSEURS VALUES ( 0, 'FOU5', 0 );
insert into FOURNISSEURS VALUES ( 0, 'FOU6', 0 );
insert into FOURNISSEURS VALUES ( 0, 'FOU7', 0 );
insert into FOURNISSEURS VALUES ( 0, 'FOU8', 0 );
insert into FOURNISSEURS VALUES ( 0, 'FOU9', 0 );
insert into FOURNISSEURS VALUES ( 0, 'FOU0', 0 );

-- -------------
-- STOCK A ZERO
-- -------------
-- D1 : Depot par defaut
insert into STOCK values ('D1', 1, 0);
insert into STOCK values ('D1', 2, 0);
insert into STOCK values ('D1', 3, 0);
insert into STOCK values ('D1', 4, 0);
insert into STOCK values ('D1', 5, 0);
insert into STOCK values ('D1', 6, 0);
insert into STOCK values ('D1', 7, 0);
insert into STOCK values ('D1', 8, 0);
insert into STOCK values ('D1', 9, 0);
insert into STOCK values ('D1', 10, 0);

exit
