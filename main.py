# from db.createTables import createTables
# createTables()

# from db.dropTables import dropTables
# dropTables()

# from db.showTables import showTables
# showTables()

name = str(input("Nome: "))
email = str(input("E-mail: "))

from db.insertInDB import insertInDB
insertInDB(name, email)

from db.selectInDB import selectInDB
selectInDB()