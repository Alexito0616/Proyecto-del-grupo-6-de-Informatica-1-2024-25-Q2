num = int(input("Dime un numero:"))
suma = 0
grande = False
while num !=-1 and not grande:
    if num%2 != 0:
      suma = suma + num

      if suma >= 100:
         grande = True
    if not (grande):
       num = int(input("Dime otro numero:"))
print(suma)

if grande:
   print("es mayor que 100")
else:
   print("no es mayor que 100")


