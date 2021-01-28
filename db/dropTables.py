import pymysql


def dropTables():
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    tableUsers = """DROP TABLE USERS;"""
    tableContasBancarias = """DROP TABLE CONTASBANCARIAS;"""

    cursor.execute(tableUsers)
    cursor.execute(tableContasBancarias)

    dbConnection.close()
