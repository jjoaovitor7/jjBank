# from db.createTables import createTables
# createTables()

# from db.dropTables import dropTables
# dropTables()

# from db.showTables import showTables
# showTables()

from db.selectInDB import selectInDB
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

    from db.insertInDB import insertInDB
    insertInDB(name, email)

selectInDB()
