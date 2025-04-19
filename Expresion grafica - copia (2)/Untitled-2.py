valido = 0
nulo = 0 
fin = False

while not fin:
    numero = int(input(""))
    letra = input("")

    if (letra=="E"):
        fin = True
    elif (letra=="V"):
        valido = valido + numero
    elif (letra=="N"):
        nulo = nulo + numero
    else:
        numero = 0
    
print((valido*100)/(valido+nulo),"V",(nulo*100)/(valido+nulo),"N")

