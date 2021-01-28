import pymysql


def selectInDB():
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    selectTableUsers = f"""SELECT * FROM USERS;"""
    selectTableContasBancarias = f"""SELECT * FROM CONTASBANCARIAS;"""

    cursor.execute(selectTableUsers)
    print(cursor.fetchall())

    cursor.execute(selectTableContasBancarias)
    print(cursor.fetchall())

    dbConnection.close()


def selectEmailInDB(email):
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    selectTableUsersEmail = f"""SELECT * FROM USERS WHERE EMAIL = "{email}";"""

    cursor.execute(selectTableUsersEmail)
    print(cursor.fetchall())

    dbConnection.close()
