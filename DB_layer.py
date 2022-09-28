import json
import pyodbc
import pandas as pd


credsfilepath="sqlDBcreds.json"


def initialize_connection():
    jsonfile = open(credsfilepath)
    credsObj=json.load(jsonfile)
    
    conn = pyodbc.connect(
                        'Driver={0};Server={1};Database={2};UID={3};PWD={4};Trusted_Connection=no;'
                        .format(credsObj["driver"],credsObj["server"],credsObj["DB"],credsObj["user"],credsObj["pass"]))
    
    cursor = conn.cursor()
    jsonfile.close()
    return conn,cursor

def close_connection(conn):
    conn.close()

def select_from_table(query):
    con,cur=initialize_connection()    
    df = pd.read_sql(query,con)
    print(df)
    close_connection(con)

def insert_into_table(query):
    con,cur=initialize_connection()
    cur.execute(query)
    con.commit()

#insert_into_table("insert into LoginUsers values ('user2','password321','user')")
select_from_table("select * from LoginUsers")





