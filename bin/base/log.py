
## -----------------
## Librairie de log
## -----------------

import datetime

def log(msg="<vide>"):
	now=datetime.datetime.now()
	ts=now.strftime('%j %X')
	print "=== %s : %s " % (ts, msg)


def test():
	msg = "Test de message"
	log(msg)


if __name__ == '__main__':
	test()
