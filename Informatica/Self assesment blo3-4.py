numero = int(input("Code:"))
ultimo = numero%10
total = 0 
while numero != 0:
    d = numero%10
    total = total + d 
    numero = numero//10
if total%ultimo == 0:
    print("ok")
else:
    print("no")