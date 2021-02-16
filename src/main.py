import re
import requests
import bcrypt
import pymysql
from clear import clear


def context(strategy):
    return strategy


def registerStrategy():
    clear()
    print("-----CADASTRO-----")

    name = str(input("Nome: "))
    email = str(input("E-mail: "))
    password = str(input("Senha: "))

    regexEmailValidator = re.compile(".+@.+\..+")
    if (regexEmailValidator.match(email) == None):
        print("Email inválido!")
    else:
        aux = requests.get("http://127.0.0.1:5000/emailverify",
                           params={"email": email}).reason

        if (len(aux) == 2):
            requests.post("http://127.0.0.1:5000/register", params={"name": name, "email": email, "password": bcrypt.hashpw(
                str.encode(password), bcrypt.gensalt())})
            context(loginStrategy())
        else:
            clear()
            print("Esse e-mail já está cadastrado no sistema.\n")


def loginStrategy():
    from clear import clear
    import globals
    clear()
    print("-----LOGIN-----")

    try:
        email = str(input("E-mail: "))
        password = str(input("Senha: "))

        if (bcrypt.checkpw(str.encode(password), str.encode(str(requests.get("http://127.0.0.1:5000/gethashforverification", params={"email": email}).reason).replace(
                "((", "").replace(",),)", "").replace("\"", "").replace("\"", "").replace("b'", "").replace("'", "")))):
            globals.NAME = str(requests.get("http://127.0.0.1:5000/getname", params={"email": email}).reason).replace(
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
                    try:
                        options()
                    except KeyboardInterrupt:
                        print("Programa interrompido.")
            except Exception as e:
                print(e)

        else:
            print("Senha inválida ou e-mail inválido.")

    except Exception as e:
        print("Erro na conexão com o servidor.")


exec = True

while (exec):
    print("-----JJBANK-----"
          + "\n1-Cadastro"
          + "\n2-Login"
          + "\n3-Sair")

    try:
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
    except KeyboardInterrupt:
        print("\nPrograma interrompido.")
        break
