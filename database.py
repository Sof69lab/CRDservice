import psycopg2
conn = psycopg2.connect(dbname="form_db", user="", password="", host="127.0.0.1", port="5432")
cursor = conn.cursor()
conn.autocommit = True
sql = '''CREATE DATABASE form_db
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;'''
cursor.execute(sql)
cursor.close()
conn.close()
