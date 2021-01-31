import globals
from clear import clear
import requests


def context(strategy):
    return strategy


def viewProfileStrategy():
    print(f"NOME: {globals.NAME}\nE-MAIL: {globals.EMAIL}")


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
                depositValue = float(input("Depósitar (R$): "))
                requests.post("http://127.0.0.1:5000/deposit",
                              params={"email": globals.EMAIL, "depositValue": depositValue})
                print("\n")

            elif (condicao2 == 3):
                clear()
                print(requests.get("http://127.0.0.1:5000/viewbalance",
                                   params={"email": globals.EMAIL}).reason)
                print("\n")

            elif (condicao2 == 4):
                clear()
                withdrawValue = float(input("Saque (R$): "))
                requests.post("http://127.0.0.1:5000/withdraw",
                             params={"email": globals.EMAIL, "withdrawValue": withdrawValue})
                print("\n")

            elif (condicao2 == 5):
                exec = False

                try:
                    requests.delete(
                        "http://127.0.0.1:5000/", data=globals.TOKEN)
                except Exception as e:
                    # print(e)
                    print("Deslogado.")

                globals.NAME = None
                globals.TOKEN = None
                globals.EMAIL = None

                print("\n")
                return None

            else:
                print("Opção inválida.")
        except ValueError:
            print("Opção inválida.")
