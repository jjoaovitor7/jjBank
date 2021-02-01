# import db.tables as tables
# tables.createTables
# tables.dropTables
# tables.showTables

import bcrypt
import requests


def context(strategy):
    return strategy


def registerStrategy():
    from clear import clear
    from db.selectInDB import selectEmailInDB
    clear()
    print("-----CADASTRO-----")

    name = str(input("Nome: "))
    email = str(input("E-mail: "))
    password = str(input("Senha: "))

    aux = selectEmailInDB(email)

    if (len(aux) == 0):
        requests.post("http://127.0.0.1:5000/register", params={"name": name, "email": email, "password": bcrypt.hashpw(
            str.encode(password), bcrypt.gensalt())})
        context(loginStrategy())
    else:
        clear()
        print("Esse e-mail já está cadastrado no sistema.\n")


def loginStrategy():
    from db.selectInDB import selectPasswordInDB, selectNameInDB
    from clear import clear
    import globals
    clear()
    print("-----LOGIN-----")

    email = str(input("E-mail: "))
    password = str(input("Senha: "))

    if (bcrypt.checkpw(str.encode(password), str.encode(str(selectPasswordInDB(email)).replace(
            "((", "").replace(",),)", "").replace("\"", "").replace("\"", "").replace("b'", "").replace("'", "")))):
        globals.NAME = str(selectNameInDB(email)).replace(
            "(('", "").replace("',),)", "")
        globals.EMAIL = email

        try:
            PORT = 5000
            token = requests.post(f"http://127.0.0.1:{PORT}/").reason
            globals.TOKEN = token

            verify = requests.post(
                f"http://127.0.0.1:{PORT}/verify", globals.TOKEN).reason

            if (verify):
                clear()
                print(
                    f"Usuário {globals.NAME} logado com o e-mail \"{globals.EMAIL}\".")

                from optionsAccount import options
                options()
        except Exception as e:
            print(e)

    else:
        print("Senha inválida ou e-mail inválido.")


exec = True

while (exec):
    print("-----JJBANK-----"
          + "\n1-Cadastro"
          + "\n2-Login"
          + "\n3-Sair")

    try:
        condicao1 = int(input(":"))

        if (condicao1 == 1):
            context(registerStrategy())
        elif (condicao1 == 2):
            context(loginStrategy())
        elif (condicao1 == 3):
            exec = False
            break
        else:
            print("Opção inválida.")
    except ValueError as error:
        if (str(error) == "Invalid salt"):
            print("Senha inválida ou e-mail inválido.\n")
        else:
            print("Opção inválida.\n")
