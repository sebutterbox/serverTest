import sqlite3, csv
import pandas as pd
from sqlite3 import Error


# Establishes a connection to the sql database, prints error if failure to connect.
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(e)

    return connection

# Creates a table from SQL connection, and from a query
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# Creates a user inserting into the table, based off customer parameter
def create_user(conn, customer):
    sql = """INSERT INTO customers(FirstName, LastName, email)
             VALUES(?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql, customer)
    conn.commit()
    return cur.lastrowid



# Main function, path of database is database.db and creation table query for a customer ID, firstname, lastname and email. SQLite will then attempt to connect and add 2 users to the table.
def main():
    database = r"weatherbase.db"

    #sql_create_projects_table = """CREATE TABLE IF NOT EXISTS customers(customerID integer PRIMARY KEY, FirstName text NOT NULL, LastName text NOT NULL, email text NOT NULL);"""

    conn = create_connection(database)

    if conn is not None:
       # create_table(conn, sql_create_projects_table)
        #customer = ("John", "Doe", "butter@butter.com")
        #create_user(conn, customer)
        #customer = ("Jane", "Doe", "brew@brew.com")
        #create_user(conn, customer)
        pass
    else:
        print("error")

def csvconveter():

    weatherbase = r"weatherbase.db"
    conn = create_connection(weatherbase)
    cur = conn.cursor()
    cur.execute("CREATE TABLE t (col1, col2);") # use your column names here

    with open('Broadstairstoday.csv','r') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin) # comma is default delimiter
        # selects what columns you want from the csv file
        to_db = [(i['datetime'], i['winddir']) for i in dr]

    #
    cur.executemany("INSERT INTO t (col1, col2) VALUES (?, ?);", to_db)
    conn.commit()
    conn.close()   

def superiorcsvconverter():
    #creates a path to weatherbase
    weatherbase = r"weatherbase.db"

    #creates a connection to the database
    conn = create_connection(weatherbase)
    #uses pandas to read the csv file
    df = pd.read_csv("Broadstairstoday.csv")
    #turns it into a table named t
    df.to_sql("t", conn, if_exists='append', index=False)
    #pandas used again to read the table that was created 
    duf = pd.read_sql_query("SELECT * FROM t", conn)
    print(duf)
    
    
if __name__ == "__main__":
    #csvconveter()
    superiorcsvconverter()
    #main()