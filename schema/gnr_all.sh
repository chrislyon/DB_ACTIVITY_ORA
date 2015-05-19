sqlplus system/manager <<!!
drop user ADV cascade;
@user.sql
!!

sqlplus adv/tiger <<!!
@ADV.sql
!!

sqlplus adv/tiger <<!!
@fixtures.sql
!!
