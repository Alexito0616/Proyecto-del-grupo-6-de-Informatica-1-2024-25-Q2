num = int(input("Dime un numero"))
i = 1

if i == 1:
    maximo = num
    minimo = num

while i<3:
    num = int(input("Dime un numero:"))
    i = i + 1
    if num > maximo:
        maximo = num
    if num < minimo:
        minimo = num
print ("El numero maximo es:",maximo,"El minimo es:",minimo)

