num1 = int(input("Dime un numero"))
letra = input("Dime que operacion deseas realizar")
num2 = int(input("Dime otro numero"))

while not (num1 == 0 and num2 ==0 and letra == "+"):
    num1 = int(input("Dime un numero"))
    letra = input("Dime que operacion deseas realizar")
    num2 = int(input("Dime otro numero"))
    
    if letra == "+":
        print(num1 + num2)

    elif letra == "-":
        print(num1 - num2)

    elif letra == "*":
        print(num1*num2)

    elif letra == "/":
        print(num1/num2)
    
    else:
        print("error")