# DB_ACTIVITY_ORA
Base Oracle avec Activité de gestion en python


Base oracle standard sans option particuliere

Schema simple et classique de Gestion :

Tables maitres : CLIENTS PRODUITS FOURNISSEURS
Tables Stock   : STOCK
Tables Ventes  : COMCLI LIGCLI
Tables Achats  : LIGFOU

Chaque cron execute plusieurs procedures :

```
----------------------------------------------------------------
# Commande Client : 8h-11h / 13h-16h      */10 minutes
*/5 8-11,13-16 * * 1-6  /home/worker/test/bin/cmd.sh client

# Reception Fou   : 9h + 11h / 16h30
0 9,11 * * 1-6 /home/worker/test/bin/cmd.sh recept_fou
30 16 * * 1-6 /home/worker/test/bin/cmd.sh recept_fou

# Livraison Client: 11h30 / 17h
30 11 * * 1-6 /home/worker/test/bin/cmd.sh livraison

# Cde Fou         : 12h00 + 18h
00 12,18 * * 1-6 /home/worker/test/bin/cmd.sh cde_fou
--------------------------------------------------------------
```

Ainsi chaque jour la base se rempli avec des données aléatoires
