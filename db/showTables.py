import pymysql


def showTables():
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    tables = """SHOW TABLES;"""

    cursor.execute(tables)
    print(cursor.fetchall())

    dbConnection.close()
