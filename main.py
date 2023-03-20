import sqlite3
import pandas as pd
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(e)

    return connection


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_user(conn, project):
    sql = """INSERT INTO customers(FirstName, LastName, email)
             VALUES(?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid


def main():
    database = r"database.db"

    sql_create_projects_table = """CREATE TABLE IF NOT EXISTS customers(customerID integer PRIMARY KEY, FirstName text NOT NULL, LastName text NOT NULL, email text NOT NULL);"""

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_projects_table)
        customer = ("John", "Doe", "butter@butter.com")
        create_user(conn, customer)
        customer = ("Jane", "Doe", "brew@brew.com")
        create_user(conn, customer)
        df = pd.read_sql_query("SELECT * FROM customers", conn)
        print(df)
    else:
        print("error")


if __name__ == "__main__":
    main()