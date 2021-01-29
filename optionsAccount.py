import globals
import pymysql
from clear import clear


def context(strategy):
    return strategy


def viewProfileStrategy():
    print(f"NOME: {globals.NAME}\nE-MAIL: {globals.EMAIL}")


def doDepositStrategy():
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    selectID = f"""SELECT ID FROM USERS WHERE EMAIL = "{globals.EMAIL}";"""
    cursor.execute(selectID)
    fetch = cursor.fetchall()
    fetchID = int(str(fetch).replace("((", "").replace(",),)", ""))

    depositValue = float(input("Depósitar (R$): "))

    selectSaldo = f"""SELECT SALDO FROM CONTASBANCARIAS WHERE ID = {fetchID};"""
    cursor.execute(selectSaldo)
    fetchSaldo = cursor.fetchall()
    deposit = float(str(fetchSaldo).replace(
        "((", "").replace(",),)", "")) + depositValue

    insertContaBancaria = f"""UPDATE CONTASBANCARIAS SET SALDO="{deposit}" WHERE ID = {fetchID};"""
    commit = f"""COMMIT;"""

    cursor.execute(insertContaBancaria)
    cursor.execute(commit)

    dbConnection.close()


def viewBalanceStrategy():
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    selectID = f"""SELECT ID FROM USERS WHERE EMAIL = "{globals.EMAIL}";"""
    cursor.execute(selectID)
    fetch = cursor.fetchall()
    fetch = int(str(fetch).replace("((", "").replace(",),)", ""))

    selectContaBancaria = f"""SELECT SALDO FROM CONTASBANCARIAS WHERE ID = {fetch};"""

    cursor.execute(selectContaBancaria)
    print("Saldo:", float(str(cursor.fetchall()).replace(
        "((", "").replace(",),)", "")))
    dbConnection.close()


def doWithdrawStrategy():
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    selectID = f"""SELECT ID FROM USERS WHERE EMAIL = "{globals.EMAIL}";"""
    cursor.execute(selectID)
    fetch = cursor.fetchall()
    fetchID = int(str(fetch).replace("((", "").replace(",),)", ""))

    withdrawValue = float(input("Saque (R$): "))

    selectSaldo = f"""SELECT SALDO FROM CONTASBANCARIAS WHERE ID = {fetchID};"""
    cursor.execute(selectSaldo)
    fetchSaldo = cursor.fetchall()
    withdraw = float(str(fetchSaldo).replace(
        "((", "").replace(",),)", "")) - withdrawValue

    insertContaBancaria = f"""UPDATE CONTASBANCARIAS SET SALDO={withdraw} WHERE ID = {fetchID};"""
    commit = f"""COMMIT;"""

    cursor.execute(insertContaBancaria)
    cursor.execute(commit)

    dbConnection.close()


def options():
    exec = True
    while (exec):
        print("-----OPÇÕES-----"
              + "\n1-Visualizar Perfil"
              + "\n2-Realizar Depósito"
              + "\n3-Visualizar Saldo"
              + "\n4-Realizar Saque"
              + "\n5-Sair")

        try:
            condicao2 = int(input(":"))

            if (condicao2 == 1):
                clear()
                context(viewProfileStrategy())
                print("\n")

            elif(condicao2 == 2):
                clear()
                context(doDepositStrategy())
                print("\n")

            elif (condicao2 == 3):
                clear()
                context(viewBalanceStrategy())
                print("\n")

            elif (condicao2 == 4):
                clear()
                context(doWithdrawStrategy())
                print("\n")

            elif (condicao2 == 5):
                exec = False
                globals.NAME = None
                globals.EMAIL = None
                print("\n")
                return None

            else:
                print("Opção inválida.")
        except ValueError:
            print("Opção inválida.")
