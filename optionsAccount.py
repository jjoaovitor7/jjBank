def options():
    import globals
    import pymysql
    exec = True
    while (exec):
        print("-----OPÇÕES-----"
              + "\n1-Visualizar Perfil"
              + "\n2-Realizar Depósito"
              + "\n3-Visualizar Saldo"
              + "\n4-Sair")

        try:
            condicao2 = int(input(":"))

            if (condicao2 == 1):
                print(f"NOME: {globals.NAME}\nE-MAIL: {globals.EMAIL}")

            elif(condicao2 == 2):
                dbConnection = pymysql.connect(
                    host="localhost", user="root", password="123456789", database="test")
                cursor = dbConnection.cursor()

                selectID = f"""SELECT ID FROM USERS WHERE EMAIL = "{globals.EMAIL}";"""
                cursor.execute(selectID)
                fetch = cursor.fetchall()
                fetch = int(str(fetch).replace("((", "").replace(",),)", ""))

                depositValue = float(input("Depósitar (R$): "))

                insertContaBancaria = f"""UPDATE CONTASBANCARIAS SET SALDO="{depositValue}" WHERE ID = {fetch};"""
                commit = f"""COMMIT;"""

                cursor.execute(insertContaBancaria)
                cursor.execute(commit)

                dbConnection.close()

            elif (condicao2 == 3):
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

            elif (condicao2 == 4):
                exec = False
                globals.NAME = None
                globals.EMAIL = None
                return None

            else:
                print("Opção inválida.")
        except ValueError:
            print("Opção inválida.")


if __name__ == "__main__":
    options()
