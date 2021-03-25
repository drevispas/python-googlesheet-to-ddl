# Steps
## 1. Generate DDLs.
`python googlesheet-to-ddl.py > finance_ddl.sql`
## 2. Load the DDL into `connect` database.
`mysql -udeveloper -p -h$MYSQL_LOCAL_CONNECT -P3306 -Dconnect < finance_ddl.sql`
