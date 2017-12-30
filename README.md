# DbQueryExecutor
Mysql and PostgreSql query executor written in python.

# How to use?
Firstly install dependencies, create or use existing query.xml file located in root together with py scripts.
All queries written in query.xml will be executed, also it is very important to configure db in this file.

#### Configure db:
Open query.xml,
```
<SQL DATABASE="PSQL"> <!-- MYSQL or PSQL -->
  <DB>db name</DB>
  <HOST>localhost</HOST>
  <USER>user</USER>
  <PASSWORD>password</PASSWORD>
```

#### Write sql queries:
Open query.xml,

in <QUERIES> tag write sql queries. For example:
  ```
<INSERT>INSERT INTO role (name, description) VALUES ('user_user', 'User')</INSERT>
<SELECT>SELECT * FROM role</SELECT>
<DELETE>DELETE FROM role</DELETE>
  ```
and etc.
  
  
## Run executor
Once you have query.xml populated, all you need is to run <b>db_query_executor.py</b> script or <b>mysql_executor.py</b> for mysql db and <b>psql_executor.py</b> for postgressql. But i suggest to use <b>db_query_executor.py</b>.

# Issue
Feel free to open issue if you have problem i'll take a look.

# Copyright
Do what every you want.

# Buy me a drink:
Bitcoin: 1JVQnkuKTWA6i4AMXFsksdJgt4B3o1yfgA
