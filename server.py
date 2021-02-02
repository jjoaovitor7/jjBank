import http.server
import socketserver
# import json
import secrets
from urllib.parse import urlparse, parse_qs
import pymysql

HOST = "127.0.0.1"
PORT = 5000

usuarios_logados = []


def createTables():
    # pymsql.connect("host", "user", "password", "db")
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

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

    # tableUsers = """DROP TABLE USERS;"""
    # tableContasBancarias = """DROP TABLE CONTASBANCARIAS;"""

    cursor.execute(tableContasBancarias)
    cursor.execute(tableUsers)

    dbConnection.close()


def showTables():
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    tables = """SHOW TABLES;"""

    cursor.execute(tables)
    print(cursor.fetchall())

    dbConnection.close()


def dropTables():
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    tableUsers = """DROP TABLE USERS;"""
    tableContasBancarias = """DROP TABLE CONTASBANCARIAS;"""

    cursor.execute(tableUsers)
    cursor.execute(tableContasBancarias)

    dbConnection.close()


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
    fetch = cursor.fetchall()

    dbConnection.close()
    return fetch


def register(_name, _email, _password):
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


def doDepositStrategy(email, depositValue):
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    selectID = f"""SELECT ID FROM USERS WHERE EMAIL = "{email}";"""
    cursor.execute(selectID)
    fetch = cursor.fetchall()
    fetchID = int(str(fetch).replace("((", "").replace(",),)", ""))

    selectSaldo = f"""SELECT SALDO FROM CONTASBANCARIAS WHERE ID = {fetchID};"""
    cursor.execute(selectSaldo)
    fetchSaldo = cursor.fetchall()
    deposit = float(str(fetchSaldo).replace(
        "((", "").replace(",),)", "")) + float(depositValue)

    insertContaBancaria = f"""UPDATE CONTASBANCARIAS SET SALDO="{deposit}" WHERE ID = {fetchID};"""
    commit = f"""COMMIT;"""

    cursor.execute(insertContaBancaria)
    cursor.execute(commit)

    dbConnection.close()


def viewBalanceStrategy(email):
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    selectID = f"""SELECT ID FROM USERS WHERE EMAIL = "{email}";"""
    cursor.execute(selectID)
    fetch = cursor.fetchall()
    fetchID = int(str(fetch).replace("((", "").replace(",),)", ""))

    selectContaBancaria = f"""SELECT SALDO FROM CONTASBANCARIAS WHERE ID = {fetchID};"""

    cursor.execute(selectContaBancaria)
    fetchSelectCB = cursor.fetchall()

    dbConnection.close()

    return "Saldo:", float(str(fetchSelectCB).replace(
        "((", "").replace(",),)", ""))


def doWithdrawStrategy(email, withdrawValue):
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    selectID = f"""SELECT ID FROM USERS WHERE EMAIL = "{email}";"""
    cursor.execute(selectID)
    fetch = cursor.fetchall()
    fetchID = int(str(fetch).replace("((", "").replace(",),)", ""))

    selectSaldo = f"""SELECT SALDO FROM CONTASBANCARIAS WHERE ID = {fetchID};"""
    cursor.execute(selectSaldo)
    fetchSaldo = cursor.fetchall()
    withdraw = float(str(fetchSaldo).replace(
        "((", "").replace(",),)", "")) - float(withdrawValue)

    insertContaBancaria = f"""UPDATE CONTASBANCARIAS SET SALDO={withdraw} WHERE ID = {fetchID};"""
    commit = f"""COMMIT;"""

    cursor.execute(insertContaBancaria)
    cursor.execute(commit)

    dbConnection.close()


class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path.startswith("/viewbalance")):
            query = parse_qs(urlparse(self.path).query)
            self.send_response(200, viewBalanceStrategy(query['email'][0]))
            self.end_headers()

        elif (self.path.startswith("/emailverify")):
            query = parse_qs(urlparse(self.path).query)
            self.send_response(200, selectEmailInDB(query['email'][0]))
            self.end_headers()

    def do_POST(self):
        if (self.path.endswith("/")):
            token = secrets.token_hex(16)
            usuarios_logados.append(token)
            self.send_response(200, token)
            self.end_headers()

        elif (self.path.startswith("/register")):
            query = parse_qs(urlparse(self.path).query)
            register(query['name'][0], query['email'][0], query['password'][0])
            self.send_response(200)
            self.end_headers()

        elif (self.path.endswith("/verify")):
            self.data_string = self.rfile.read(
                int(self.headers['Content-Length']))

            if (str(self.data_string).replace("b'", "").replace("'", "") in usuarios_logados):
                self.send_response(200, True)
                self.end_headers()

            else:
                self.send_response(404, False)
                self.end_headers()

        elif (self.path.startswith("/deposit")):
            query = parse_qs(urlparse(self.path).query)
            doDepositStrategy(query['email'][0], query['depositValue'][0])
            self.send_response(200)
            self.end_headers()

        elif (self.path.startswith("/withdraw")):
            query = parse_qs(urlparse(self.path).query)
            doWithdrawStrategy(query['email'][0], query['withdrawValue'][0])
            self.send_response(200)
            self.end_headers()

    def do_DELETE(self):
        self.data_string = self.rfile.read(
            int(self.headers['Content-Length']))

        usuarios_logados.remove(
            str(self.data_string).replace("b'", "").replace("'", ""))


httpd = socketserver.TCPServer((HOST, PORT), SimpleHTTPRequestHandler)
print(f"Servindo em {HOST} na porta: {PORT}.")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("\nServidor parado.")
