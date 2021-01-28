def options():
    import globals
    exec = True
    while (exec):
        print("-----OPÇÕES-----"
              + "\n1-PERFIL"
              + "\n2-SAIR")

        try:
            condicao2 = int(input(":"))

            if (condicao2 == 1):
                print(f"NOME: {globals.NAME}\nE-MAIL: {globals.EMAIL}")

            elif(condicao2 == 2):
                exec = False
                globals.NAME = None
                globals.EMAIL = None
                return None
        except ValueError:
            print("Opção inválida.")
