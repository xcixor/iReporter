"""Database related functionality."""

import psycopg2


def connect(db_config):
    """Create a db connection.

    args:
        db_config(dict): Database url variables

    returns:
        conn(connection): A connection to the database
    """
    conn = None
    try:
        print('Connecting to db...')
        url = "dbname={} user={} password={} host={} port={}".\
              format(db_config['dbname'], db_config['user'],
                     db_config['password'], db_config['host'],
                     db_config['port'])
        conn = psycopg2.connect(url)
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            print("Connected to db")
            return conn
        return None


def init_db(db_config):
    """Initialize db."""
    create_tables(db_config)


def create_tables(db_config):
    """Create tables."""
    tables = table_queries()
    try:
        conn = connect(db_config)
        cursor = conn.cursor()
        for table in tables:
            cursor.execute(table)
            conn.commit()
        print('***** db init complete *****')
    except Exception as e:
        print(e)


def table_queries():
    """Table queries."""
    tables = []
    user = "CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY,\
    Email VARCHAR, \
    User_Password TEXT, \
    FirstName TEXT,\
    LastName TEXT, \
    Is_Admin Boolean);"
    tables.append(user)

    incident = "CREATE TABLE IF NOT EXISTS incidents (id serial PRIMARY KEY,\
    Creator TEXT,\
    Location TEXT,\
    Type TEXT,\
    Comment TEXT,\
    user_id INTEGER REFERENCES users(id),\
    Title TEXT);"
    tables.append(incident)

    images = "CREATE TABLE IF NOT EXISTS images (id serial PRIMARY KEY,\
    url TEXT,\
    incident_id INTEGER REFERENCES incidents(id));"
    tables.append(images)

    videos = "CREATE TABLE IF NOT EXISTS videos (id serial PRIMARY KEY, \
    url TEXT,\
    incident_id INTEGER REFERENCES incidents(id));"
    tables.append(videos)

    return tables
