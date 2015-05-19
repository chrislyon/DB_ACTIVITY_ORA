
# Commande Client : 8h-11h / 13h-16h      */10 minutes
*/10 8-11,13-16 * * 1-5	/home/worker/test/bin/client.sh
# Reception Fou   : 9h + 11h / 16h30
0 9,11 * * 1-5 /home/worker/test/bin/recept_fou.sh
30 16 * * 1-5 /home/worker/test/bin/recept_fou.sh
# Livraison Client: 11h30 / 17h
30 11 * * 1-5 /home/worker/test/bin/livraison.sh
# Cde Fou         : 12h00 + 18h
00 12,18 * * 1-5 /home/worker/test/bin/cde_fou.sh
