def clear():
    import os
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
