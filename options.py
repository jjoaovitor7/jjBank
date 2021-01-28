def options():
    import globals
    exec = True
    while (exec):
        print("-----OPÇÕES-----"
        + "\n1-PERFIL"
        + "\n2-SAIR")

        condicao2 = int(input())

        if (condicao2 == 1):
            print(f"NOME: {globals.NAME}\nE-MAIL: {globals.EMAIL}")

        elif(condicao2 == 2):
            exec = False
            break