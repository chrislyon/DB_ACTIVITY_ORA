--
-- User ADV 
--

drop user ADV cascade;

create user ADV identified by tiger
quota unlimited on USERS
temporary tablespace TEMP;

grant CONNECT to ADV;
grant RESOURCE to ADV;
grant create view to ADV;

exit
