import pymysql


def connectDatabase():
    return pymysql.connect(host="localhost", user="root", password="123456789", database="test")


def createTables():
    cursor = connectDatabase().cursor()

    tableUsers = """CREATE TABLE IF NOT EXISTS USERS (
        ID int(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        NOME varchar(100) NOT NULL,
        EMAIL varchar(50) NOT NULL,
        SENHA varchar(65) NOT NULL,
        FK_ID_BANCO int(5) DEFAULT NULL,
        CONSTRAINT FK_1 FOREIGN KEY (`FK_ID_BANCO`) REFERENCES `CONTASBANCARIAS`(`ID`) ON UPDATE CASCADE
    );
    """

    tableContasBancarias = """CREATE TABLE IF NOT EXISTS CONTASBANCARIAS (
        ID int NOT NULL AUTO_INCREMENT,
        SALDO int(15) DEFAULT "0",
        PRIMARY KEY (ID)
    );
    """

    cursor.execute(tableContasBancarias)
    cursor.execute(tableUsers)

    connectDatabase().close()


def showTables():
    cursor = connectDatabase().cursor()

    tables = """SHOW TABLES;"""

    cursor.execute(tables)
    print(cursor.fetchall())

    connectDatabase().close()


def dropTables():
    cursor = connectDatabase().cursor()

    tableUsers = """DROP TABLE USERS;"""
    tableContasBancarias = """DROP TABLE CONTASBANCARIAS;"""

    cursor.execute(tableUsers)
    cursor.execute(tableContasBancarias)

    connectDatabase().close()
