import pymysql


def insertInDB(name, email):
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    insertContaBancaria = f"""INSERT INTO CONTASBANCARIAS () VALUES ();"""
    insertUser = f"""INSERT INTO USERS (`NOME`, `EMAIL`, `FK_ID_BANCO`) VALUES ("{name}", "{email}", LAST_INSERT_ID());"""
    commit = f"""COMMIT;"""

    cursor.execute(insertContaBancaria)
    cursor.execute(insertUser)
    cursor.execute(commit)

    dbConnection.close()
