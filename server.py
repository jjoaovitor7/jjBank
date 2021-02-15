import http.server
import socketserver
# import json
import secrets
from urllib.parse import urlparse, parse_qs
import pymysql

HOST = "127.0.0.1"
PORT = 5000

usuarios_logados = []


def connectDatabase():
    return pymysql.connect(host="localhost", user="root", password="123456789", database="test")


def selectNameInDB(_email):
    cursor = connectDatabase().cursor()
    cursor.execute(f"""SELECT NOME FROM USERS WHERE EMAIL = "{_email}";""")
    fetch = cursor.fetchall()
    connectDatabase().close()
    return fetch


def selectPasswordInDB(_email):
    cursor = connectDatabase().cursor()
    cursor.execute(f"""SELECT SENHA FROM USERS WHERE EMAIL = "{_email}";""")
    fetch = cursor.fetchall()
    connectDatabase().close()
    return fetch


def selectEmailInDB(_email):
    cursor = connectDatabase().cursor()
    cursor.execute(f"""SELECT * FROM USERS WHERE EMAIL = "{_email}";""")
    fetch = cursor.fetchall()
    connectDatabase().close()
    return fetch


def register(_name, _email, _password):
    cursor = connectDatabase().cursor()
    cursor.execute("INSERT INTO CONTASBANCARIAS () VALUES ();")
    cursor.execute(
        f"""INSERT INTO USERS (`NOME`, `EMAIL`, `FK_ID_BANCO`, `SENHA`) VALUES ("{_name}", "{_email}", LAST_INSERT_ID(), "{_password}");""")
    cursor.execute("COMMIT;")
    connectDatabase().close()


def doDepositStrategy(email, depositValue):
    cursor = connectDatabase().cursor()

    cursor.execute(f"""SELECT ID FROM USERS WHERE EMAIL = "{email}";""")
    fetch = cursor.fetchall()
    fetchID = int(fetch[0][0])

    cursor.execute(
        f"""SELECT SALDO FROM CONTASBANCARIAS WHERE ID = {fetchID};""")
    fetchSaldo = cursor.fetchall()
    deposit = float(fetchSaldo[0][0]) + float(depositValue)

    cursor.execute(
        f"""UPDATE CONTASBANCARIAS SET SALDO="{deposit}" WHERE ID = {fetchID};""")
    cursor.execute("COMMIT;")
    connectDatabase().close()


def viewBalanceStrategy(email):
    cursor = connectDatabase().cursor()
    cursor.execute(f"""SELECT ID FROM USERS WHERE EMAIL = "{email}";""")
    fetch = cursor.fetchall()
    fetchID = int(fetch[0][0])

    cursor.execute(
        f"""SELECT SALDO FROM CONTASBANCARIAS WHERE ID = {fetchID};""")
    fetchSelectCB = cursor.fetchall()

    connectDatabase().close()
    return "Saldo:", float(fetchSelectCB[0][0])


def doWithdrawStrategy(email, withdrawValue):
    cursor = connectDatabase().cursor()

    cursor.execute(f"""SELECT ID FROM USERS WHERE EMAIL = "{email}";""")
    fetch = cursor.fetchall()
    fetchID = int(fetch[0][0])

    cursor.execute(
        f"""SELECT SALDO FROM CONTASBANCARIAS WHERE ID = {fetchID};""")
    fetchSaldo = cursor.fetchall()
    withdraw = float(fetchSaldo[0][0]) - float(withdrawValue)

    cursor.execute(
        f"""UPDATE CONTASBANCARIAS SET SALDO={withdraw} WHERE ID = {fetchID};""")
    cursor.execute("COMMIT;")
    connectDatabase().close()


def doTransferStrategy(emailOrigin, transferValue, emailTransfer):
    cursor = connectDatabase().cursor()

    # retirando o dinheiro a ser transferido
    # TODO: verificar se a conta existe
    cursor.execute(
        f"""SELECT FK_ID_BANCO FROM USERS WHERE EMAIL = "{emailOrigin}";""")
    fetch = cursor.fetchall()
    fetchContaBancaria = int(fetch[0][0])

    cursor.execute(
        f"""SELECT SALDO FROM CONTASBANCARIAS WHERE ID = {fetchContaBancaria};""")
    fetchSaldo = cursor.fetchall()
    transfer = float(fetchSaldo[0][0]) - float(transferValue)

    cursor.execute(
        f"""UPDATE CONTASBANCARIAS SET SALDO={transfer} WHERE ID = {fetchContaBancaria};""")
    cursor.execute("COMMIT;")

    # adicionando na conta
    # TODO: verificar se a conta existe
    cursor.execute(
        f"""SELECT FK_ID_BANCO FROM USERS WHERE EMAIL = "{emailTransfer}";""")
    fetch = cursor.fetchall()
    fetchContaBancariaTransfer = int(fetch[0][0])

    cursor.execute(
        f"""SELECT SALDO FROM CONTASBANCARIAS WHERE ID = {fetchContaBancariaTransfer};""")
    fetchSaldoTransfer = cursor.fetchall()
    transfer_ = float(fetchSaldoTransfer[0][0]) + float(transferValue)

    cursor.execute(
        f"""UPDATE CONTASBANCARIAS SET SALDO={transfer_} WHERE ID = {fetchContaBancariaTransfer};""")
    cursor.execute("COMMIT;")
    connectDatabase().close()


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

        elif (self.path.startswith("/gethashforverification")):
            query = parse_qs(urlparse(self.path).query)
            self.send_response(200, selectPasswordInDB(query['email'][0]))
            self.end_headers()

        elif (self.path.startswith("/getname")):
            query = parse_qs(urlparse(self.path).query)
            self.send_response(200, selectNameInDB(query['email'][0]))
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

        elif (self.path.startswith("/register")):
            query = parse_qs(urlparse(self.path).query)
            register(query['name'][0], query['email'][0], query['password'][0])
            self.send_response(200)
            self.end_headers()

        elif (self.path.startswith("/verify")):
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

        elif (self.path.startswith("/transfer")):
            query = parse_qs(urlparse(self.path).query)
            doTransferStrategy(query['emailOrigin'][0], query['transferValue'][0],  query['emailTransfer'][0])
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
