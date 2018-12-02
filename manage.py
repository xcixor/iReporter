"""Database related functionality."""
import psycopg2

development_url = "dbname='ireporter' host='localhost' port='5432' user='developer' password='developer'"
test_url = "dbname='test_ireporter' host='localhost' port='5432' user='developer' password='developer'"


def connect(url):
    conn = None
    try:
        print('Connecting to db...')
        conn = psycopg2.connect(url)
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            print("Connected to db")
            return conn


def init_db():
    """Initialize db."""
    tables()


def tables():
    """Create tables."""
    conn = connect(development_url)
    cursor = conn.cursor()
    user = "CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY,\
                                         Email VARCHAR, \
                                         User_Password TEXT, \
                                         FirstName TEXT,\
                                         LastName TEXT, \
                                         Is_Admin Boolean);"
    incident = "CREATE TABLE IF NOT EXISTS incidents (id serial PRIMARY KEY,\
                                            Creator TEXT,\
                                            Location TEXT,\
                                            Type TEXT,
                                            Comment TEXT);"
    try:
        cursor.execute(user)
        conn.commit()
        print('**********tables created successfuly*************')
    except Exception as e:
        print(e)
