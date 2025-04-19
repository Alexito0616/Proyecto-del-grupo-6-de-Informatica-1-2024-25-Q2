x = int(input("Escribe la base:"))
y = int(input("Escribe el radical:"))
i = 1
if (y<0):
    print("error")

else:
    resultado = 1
    while (i <= y):
        i = i + 1
        resultado = resultado * x
    print(resultado)


