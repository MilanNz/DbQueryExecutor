#!/usr/bin/python
import xml.etree.ElementTree
import psycopg2
import mysql.connector


db_name = ''
db_host = ''
db_user = ''
db_password = ''
db_cnx = None


# gets queries from xml.
def parse_queries_xml():
    e = xml.etree.ElementTree.parse('query.xml').getroot()
    return e.find('QUERIES')


# gets configs from xml.
def parse_config_xml():
    e = xml.etree.ElementTree.parse('query.xml').getroot()
    return e.find('CONFIG')


# select database version.
def psql_get_db_version(cursor):
    cursor.execute('SELECT version()')
    return cursor.fetchone()


# gets db type MySql or PSQL
def get_db_type():
    e = xml.etree.ElementTree.parse('query.xml').getroot()
    return e.get('DATABASE')


# sets configs.
def set_config():
    global db_name
    global db_host
    global db_user
    global db_password
    for item in parse_config_xml():
        print item.tag
        if item.tag == 'DB':
            db_name = item.text
        elif item.tag == 'USER':
            db_user = item.text
        elif item.tag == 'HOST':
            db_host = item.text
        elif item.tag == 'PASSWORD':
            db_password = item.text
    print 'db config', db_name, db_host, db_user, db_password


# connects on db server.
def psql_connect():
    try:
        conn = psycopg2.connect("dbname=%s host=%s user=%s password=%s" % (db_name, db_host, db_user, db_password))
        conn.autocommit = True
        return conn.cursor()
    except Exception, e:
        print 'connection problem', e.message
        return None


# connects on db server.
def mysql_connect():
    try:
        db_cnx = mysql.connector.connect(user=db_user, password=db_password, host=db_host, database=db_name)
        return db_cnx.cursor()
    except Exception, e:
        print 'connection problem', e.message
        return None


# executes queries.
def psql_execute_queries(queries):
    for query in queries:
        print 'executed', query.text
        if query.tag == 'SELECT':
            cursor.execute(query.text)
            print cursor.fetchall()
        else:
            cursor.execute(query.text)


# executes queries.
def mysql_execute_queries(queries):
    for query in queries:
        print 'executed', query.text
        if query.tag == 'SELECT':
            cursor.execute(query.text)
            db_cnx.commit()
            print cursor.fetchall()
        else:
            cursor.execute(query.text)
            db_cnx.commit()


try:
    # set up configuration.
    set_config()
    db_type = get_db_type()

    # connect on db server and get cursor.
    cursor = None
    if db_type == 'MYSQL':
        cursor = mysql_connect()
    elif db_type == 'PSQL':
        cursor = psql_connect()
    else:
        raise ValueError('DB type must be MYSQL or PSQL')

    print '*********** PSQL/MYSQL Version ***********'
    if db_type == 'PSQL':
        print psql_get_db_version(cursor)

    print '*********** EXECUTE QUERIES ***********'
    queries = parse_queries_xml()
    if db_type == 'MYSQL':
        mysql_execute_queries(queries)
    elif db_type == 'PSQL':
        psql_execute_queries(queries)

    print '*********** COMPLETED ***********'
    if db_type == 'MYSQL':
        cursor.close()
        db_cnx.close()

except Exception, e:
    print 'Whoops ', e