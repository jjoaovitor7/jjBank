import bcrypt
import requests
import pymysql

def selectNameInDB(_email):
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    selectTableUsersName = f"""SELECT NOME FROM USERS WHERE EMAIL = "{_email}";"""

    cursor.execute(selectTableUsersName)
    fetch = cursor.fetchall()

    dbConnection.close()
    return fetch


def selectPasswordInDB(_email):
    dbConnection = pymysql.connect(
        host="localhost", user="root", password="123456789", database="test")
    cursor = dbConnection.cursor()

    selectTableUsersEP = f"""SELECT SENHA FROM USERS WHERE EMAIL = "{_email}";"""

    cursor.execute(selectTableUsersEP)
    fetch = cursor.fetchall()

    dbConnection.close()
    return fetch


def context(strategy):
    return strategy


def registerStrategy():
    from clear import clear
    clear()
    print("-----CADASTRO-----")

    name = str(input("Nome: "))
    email = str(input("E-mail: "))
    password = str(input("Senha: "))

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
