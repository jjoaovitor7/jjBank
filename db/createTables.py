import pymysql


def createTables():
    # pymsql.connect("host", "user", "password", "db")
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    tableUsers = """CREATE TABLE IF NOT EXISTS USERS (
        ID int(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        NOME varchar(100) NOT NULL,
        EMAIL varchar(50) NOT NULL,
        FK_ID_BANCO int(5) DEFAULT NULL,
        CONSTRAINT FK_1 FOREIGN KEY (`FK_ID_BANCO`) REFERENCES `CONTASBANCARIAS`(`ID`) ON UPDATE CASCADE
    );
    """

    tableContasBancarias = """CREATE TABLE IF NOT EXISTS CONTASBANCARIAS (
        ID int NOT NULL AUTO_INCREMENT,
        PRIMARY KEY (ID)
    );
    """

    cursor.execute(tableContasBancarias)
    cursor.execute(tableUsers)

    dbConnection.close()
