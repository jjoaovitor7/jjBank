# from db.createTables import createTables
# createTables()

# from db.dropTables import dropTables
# dropTables()

# from db.showTables import showTables
# showTables()

import bcrypt


def context(strategy):
    return strategy


def registerStrategy():
    from clear import clear
    clear()
    print("-----CADASTRO-----")

    name = str(input("Nome: "))
    email = str(input("E-mail: "))
    password = str(input("Senha: "))

    from db.insertInDB import insertInDB
    insertInDB(name, email, bcrypt.hashpw(
        str.encode(password), bcrypt.gensalt()))


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

        clear()
        print(
            f"Usuário {globals.NAME} logado com o e-mail \"{globals.EMAIL}\".")

        from optionsAccount import options
        options()
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
            context(loginStrategy())
        elif (condicao1 == 2):
            context(loginStrategy())
        elif (condicao1 == 3):
            exec = False
            break
        else:
            print("Opção inválida.")
    except ValueError:
        print("Opção inválida.")
