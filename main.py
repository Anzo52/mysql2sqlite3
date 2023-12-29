# Python script for transfering data from mysql to sqlite

import sqlite3
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from simple_term_menu import TerminalMenu
from rich import print
import os

load_dotenv()


def mysql_con():
    # Connect to mysql db and return db, cursor
    db = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        passwd=os.getenv("MYSQL_PASSWD"),
        database=os.getenv("MYSQL_DB"),
    )
    cursor = db.cursor()
    return db, cursor


def get_mysql_tables():
    # Get all tables from mysql db
    db, cursor = mysql_con()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    db.close()
    return tables


def select_mysql_table():
    # Select mysql table from list
    tables = get_mysql_tables()
    table_names = [table[0] for table in tables]
    terminal_menu = TerminalMenu(table_names)
    table_index = terminal_menu.show()
    return tables[table_index][0]


def get_mysql_table_columns(table):
    # Get all columns from mysql table
    db, cursor = mysql_con()
    cursor.execute(f"SHOW COLUMNS FROM {table}")
    columns = cursor.fetchall()
    db.close()
    return [column[0] for column in columns]


def get_mysql_table_column_types(table):
    # Get all column types from mysql table
    db, cursor = mysql_con()
    cursor.execute(f"SHOW COLUMNS FROM {table}")
    columns = cursor.fetchall()
    db.close()
    return [column[1] for column in columns]


def get_mysql_table_data(table):
    # Get all data from mysql table
    db, cursor = mysql_con()
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    db.close()
    return data


def get_mysql_table_schema(table):
    # Get table schema from mysql table
    db, cursor = mysql_con()
    cursor.execute(f"SHOW CREATE TABLE {table}")
    schema = cursor.fetchall()
    db.close()
    return schema


def mysql_schema_to_sqlite(schema):
    # Convert mysql schema to sqlite schema
    table_name = schema[0][0]
    columns = get_mysql_table_columns(table_name)
    column_types = get_mysql_table_column_types(table_name)
    sqlite_types = {
        "int": "INTEGER",
        "varchar": "TEXT",
        "datetime": "TEXT",
        "timestamp": "TEXT",
        "date": "TEXT",
        "tinyint": "INTEGER",
        "decimal": "REAL",
    }
    new_types = mysql_to_sqlite_types(column_types, sqlite_types)
    return f"CREATE TABLE {table_name} ({','.join([f'{columns[i]} {new_types[i]}' for i in range(len(columns))])})"


def mysql_to_sqlite_types(column_types, sqlite_types):
    # Convert mysql types to sqlite types
    new_types = []
    for column_type in column_types:
        if column_type in sqlite_types:
            new_types.append(sqlite_types[column_type])
        else:
            new_types.append("TEXT")
    return new_types


def sqlite_con():
    # Connect to sqlite db and return db, cursor
    db = sqlite3.connect("data.db")
    cursor = db.cursor()
    return db, cursor


def create_sqlite_table(table, schema):
    # Create sqlite table
    db, cursor = sqlite_con()
    cursor.execute(schema)
    db.commit()
    db.close()


def insert_sqlite_data(table, columns, data):
    # Insert data into sqlite table
    db, cursor = sqlite_con()
    for row in data:
        row_data = []
        for i in range(len(row)):
            if columns[i][1] == "int":
                row_data.append(str(row[i]))
            else:
                row_data.append(f"'{row[i]}'")
        cursor.execute(f"INSERT INTO {table} VALUES ({','.join(row_data)})")
    db.commit()
    db.close()


def main():
    # Main function
    table = select_mysql_table()
    print(table)
    columns = get_mysql_table_columns(table)
    print(columns)
    data = get_mysql_table_data(table)
    print(data)
    schema = get_mysql_table_schema(table)
    print(schema)
    sqlite_schema = mysql_schema_to_sqlite(schema)
    print(sqlite_schema)
    create_sqlite_table(table, sqlite_schema)
    insert_sqlite_data(table, columns, data)
    print(f"Data from {table} table has been transfered to sqlite database.")


if __name__ == "__main__":
    main()
