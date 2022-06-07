import array
import sqlite3 as sqlite
import os
import sys
import numpy as np

path = os.path.dirname(__file__) + "/database.db"
con = sqlite.connect(path)


def create_database(name_table):
    """
    function: Create Table contain Information of Employee
    with: Id, FullName, Position, Embed, Active, IsAdmin
    Args:
        name_table: name_table

    Returns:

    """
    with con:

        cur = con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {name_table}")
        cur.execute(f"CREATE TABLE {name_table}(id TEXT PRIMARY KEY, fullname TEXT, sex INT, position TEXT,"
                    f" office TEXT, embed BLOB)")
        cur.close()


def add_employee(data_tuple, name_table='employees'):
    """
    Function: add new employee
    Args:
        data_tuple: tuple
        name_table:name of table

    Returns:

    """

    try:
        con = sqlite.connect(path)
        cursor = con.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = f""" INSERT INTO {name_table}
        (id, fullname, sex, position, office, embed) VALUES (?, ?, ?, ?, ?, ?)"""
        print(data_tuple)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        con.commit()
        print("Data inserted successfully into a table")
        cursor.close()

    except sqlite.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if con:
            con.close()
            print("the sqlite connection is closed")


def get_all_employee(name_table='employees'):
    """
    Function: Get information of name_table
    Args:
        name_table: name of table
    Returns:

    """
    con = sqlite.connect(path)
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {name_table}")
        # get data
        rows = cur.fetchall()
        data = []
        for id, row in enumerate(rows):
            row = list(row)
            for i in [len(row)-1]:
                # convert binary to array
                arr = np.frombuffer(row[i], dtype='float')
                # convert array 1D to nD
                row[i] = arr.reshape(len(arr)//512, 512).tolist()
            data.append(row)
        return data


def update_info(data_change: tuple, name_table='employees'):
    """
    Function: Again update information of employee
    Args:
        name_rows: name of change rows
        value_replace: change value or name
        id: id of employee
        full_name: full name of employee
        name_table: name of table

    Returns:

    """
    try:
        con = sqlite.connect(path)
        cursor = con.cursor()
        print("Connected to SQLite")
        sql_update_query = f"""UPDATE {name_table} SET fullname = ?, sex = ?, position = ?, office = ? 
        Where id = {data_change[0]}"""
        cursor.execute(sql_update_query, (data_change[1:5]))
        con.commit()
        print("Record update successfully")
        cursor.close()

    except sqlite.Error as error:
        print("Failed to update reocord from a sqlite table", error)
    finally:
        if con:
            con.close()
            print("sqlite connection is closed")


def delete_employee(code_id: str, name_table='employees'):
    """
    function: Remove a object with id and full_name at name_table
    Args:
        id: data id
        name_table: name of table

    Returns:

    """
    try:
        con = sqlite.connect(path)
        cursor = con.cursor()
        print("Connected to SQLite")
        sql_update_query = f"""DELETE FROM {name_table} Where id = {code_id}"""
        cursor.execute(sql_update_query)
        con.commit()
        print("Record deleted successfully")
        cursor.close()

    except sqlite.Error as error:
        print("Failed to delete reocord from a sqlite table", error)
    finally:
        if con:
            con.close()
            print("sqlite connection is closed")


def insert_timekeeping(id: str, fullname: str):
    """
    insert timekeepings row
    Args:
        id:
        fullname:

    Returns:

    """
    try:
        con = sqlite.connect(path)
        cursor = con.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = f""" INSERT INTO timekeepings (id, fullname) VALUES (?, ?)"""
        cursor.execute(sqlite_insert_blob_query, (id, fullname))
        con.commit()
        print("Data inserted successfully into a table")
        cursor.close()

    except sqlite.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if con:
            con.close()
            print("the sqlite connection is closed")


if __name__ == '__main__':
    # create database for tab employee
    create_database('employee')
    # add info
    embed = []
    a = np.ones((1, 512))[0].tolist()
    b = np.zeros((1, 512))[0].tolist()
    embed.append(a)
    embed.append(b)
    embed = np.array(embed, dtype='float')
    add_employee(('DEV01', 'Dao Duy Ngu', 1, 'Dev', 'AI',embed,), 'employee')
    add_employee(('DEV02', 'Nguyen Vu Hoai Duy', 1, 'Dev', 'AI', embed), 'employee')
    add_employee(('DEV03', 'Tran Chi Cuong', 0, 'Dev', 'AI', embed), 'employee')
    # delete employee
    delete_employee('DEV01')
    # get employee
    data = get_all_employee('employee')
    print(data)
    # change info
    update_info(('106190023', 'Nguyen Van C', 1, 'DEV', 'AI'))
    data = get_all_employee('employee')
    print(data)
    insert_timekeeping('DEV02', 'Dao Duy Ngu')
