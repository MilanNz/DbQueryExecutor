#!/usr/bin/python
import xml.etree.ElementTree
import psycopg2


db_name = ''
db_host = ''
db_user = ''
db_password = ''


# gets queries from xml.
def parse_queries_xml():
    e = xml.etree.ElementTree.parse('query.xml').getroot()
    return e.find('QUERIES')


# gets configs from xml.
def parse_config_xml():
    e = xml.etree.ElementTree.parse('query.xml').getroot()
    return e.find('CONFIG')


# select database version.
def get_db_version(cursor):
    cursor.execute('SELECT version()')
    return cursor.fetchone()


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
def connect():
    try:
        conn = psycopg2.connect("dbname=%s host=%s user=%s password=%s" % (db_name, db_host, db_user, db_password))
        conn.autocommit = True
        return conn.cursor()
    except Exception, e:
        print 'connection problem', e.message
        return None


# executes queries.
def execute_queries(queries):
    for query in queries:
        print 'executed', query.text
        if query.tag == 'SELECT':
            cursor.execute(query.text)
            print cursor.fetchall()
        else:
            cursor.execute(query.text)


try:
    # set up configuration.
    set_config()

    # connect on db server.
    cursor = connect()

    print '*********** PSQL Version ***********'
    print get_db_version(cursor)

    print '*********** EXECUTE QUERIES ***********'
    queries = parse_queries_xml()
    execute_queries(queries)

    print '*********** COMPLETED ***********'
except Exception, e:
    print 'Whoops ', e