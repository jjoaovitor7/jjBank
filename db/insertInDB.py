import pymysql


def insertInDB(_name, _email, _password):
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    insertContaBancaria = f"""INSERT INTO CONTASBANCARIAS () VALUES ();"""
    insertUser = f"""INSERT INTO USERS (`NOME`, `EMAIL`, `FK_ID_BANCO`, SENHA) VALUES ("{_name}", "{_email}", LAST_INSERT_ID(), "{_password}");"""
    commit = f"""COMMIT;"""

    cursor.execute(insertContaBancaria)
    cursor.execute(insertUser)
    cursor.execute(commit)

    dbConnection.close()
