import http.server
import socketserver
# import json
import secrets
from urllib.parse import urlparse, parse_qs
import pymysql

HOST = "127.0.0.1"
PORT = 5000

usuarios_logados = []


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

    def do_POST(self):
        if (self.path.endswith("/")):
            token = secrets.token_hex(16)
            usuarios_logados.append(token)
            self.send_response(200, token)
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
