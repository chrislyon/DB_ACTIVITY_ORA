export ORACLE_BASE=/ado/app/oracle
export ORACLE_HOME=$ORACLE_BASE/product/11.2.0/dbhome_1

export PATH=$ORACLE_HOME/bin:$PATH
export LD_LIBRARY_PATH=/ado/app/oracle/product/11.2.0/dbhome_1/lib
export ORACLE_SID=X3TEST

MODE=test
DIR_BASE=/home/worker/$MODE
DIR_BIN=$DIR_BASE/bin
DIR_LOG=$DIR_BASE/log

TS=$(date "+%j_%H%M")

FONCTION=client
FIC_LOG=$DIR_LOG/${TS}_${FONCTION}.log

exec 1>$FIC_LOG
exec 2>&1

PYTHON=/usr/local/bin/python2.7

( cd $DIR_BIN ; $PYTHON $FONCTION.py )
