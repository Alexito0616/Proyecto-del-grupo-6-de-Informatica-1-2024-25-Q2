a = int(input("Dime un número:"))
b = int(input("Dime otro:"))
c = int(input("Dime el ultimo:"))

if a == b + c or b == a + c or c == a + b:
    print("Se cumple")

else:
    print("No se cumple")