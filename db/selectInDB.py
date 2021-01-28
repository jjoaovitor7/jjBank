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


def selectEmailInDB(_email):
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    selectTableUsersEmail = f"""SELECT * FROM USERS WHERE EMAIL = "{_email}";"""

    cursor.execute(selectTableUsersEmail)
    print(cursor.fetchall())

    dbConnection.close()


def selectNameInDB(_email):
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    selectTableUsersName = f"""SELECT NOME FROM USERS WHERE EMAIL = "{_email}";"""

    cursor.execute(selectTableUsersName)
    fetch = cursor.fetchall()

    dbConnection.close()
    return fetch


def selectPasswordInDB(_email):
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    selectTableUsersEP = f"""SELECT SENHA FROM USERS WHERE EMAIL = "{_email}";"""

    cursor.execute(selectTableUsersEP)
    fetch = cursor.fetchall()

    dbConnection.close()
    return fetch