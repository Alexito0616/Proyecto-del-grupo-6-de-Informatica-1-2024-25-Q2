edad = [25,40,65,80]
kcal = [120,110,105,100,90]
edad = int(input("Escribe tu edad:"))

if edad < 25:
    print(kcal[0])

elif edad > 25 and edad < 40:
    print(kcal[1])

elif edad > 40 and edad < 65:
    print(kcal[2])

elif edad > 65 and edad < 80:
    print(kcal[3])

elif edad > 80:
    print(kcal[4])

else:
    print("error")
