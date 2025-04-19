a = int(input("Dime un numero:"))
b = int(input("Dime otro numero:"))
letra = input("Dime una letra:")
suma = a + b

if letra == "a":
    print(suma%10)

elif letra == b:
    print(suma/2)

else:
    print("error")
