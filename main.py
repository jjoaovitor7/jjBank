# from db.createTables import createTables
# createTables()

# from db.dropTables import dropTables
# dropTables()

# from db.showTables import showTables
# showTables()

from db.selectInDB import selectInDB, selectEmailInDB, selectNameInDB, selectPasswordInDB
import bcrypt
print("----JJBANK----")
print("1-Cadastro")
print("2-Login")
condicao1 = int(input(":"))

if (condicao1 == 1):
    from clear import clear
    clear()
    print("----CADASTRO----")

    name = str(input("Nome: "))
    email = str(input("E-mail: "))
    password = str(input("Senha: "))

    from db.insertInDB import insertInDB
    insertInDB(name, email, bcrypt.hashpw(
        str.encode(password), bcrypt.gensalt()))

elif (condicao1 == 2):
    from clear import clear
    import globals
    clear()
    print("----LOGIN----")

    email = str(input("E-mail: "))
    password = str(input("Senha: "))

    if (bcrypt.checkpw(str.encode(password), str.encode(str(selectPasswordInDB(email)).replace(
            "((", "").replace(",),)", "").replace("\"", "").replace("\"", "").replace("b'", "").replace("'", "")))):
        globals.NAME = str(selectNameInDB(email)).replace(
            "(('", "").replace("',),)", "")
        globals.EMAIL = email

        print(f"Usuário {globals.NAME} logado com o e-mail \"{globals.EMAIL}\".")
# selectInDB()
