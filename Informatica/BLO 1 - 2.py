a = int(input("Dime un numero:"))
b = int(input("Dime otro:"))
c = int(input("Dime el último:"))
producto = a*b*c

if producto%2 == 0:
    print("El producto es un número par")

else:
    print("El producto es un número impar")