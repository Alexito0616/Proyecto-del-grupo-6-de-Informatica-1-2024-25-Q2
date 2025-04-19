F = open("products.txt","r")
linea = F.readline()
while linea != "":
    trozos = linea.rstrip().split("")
    pAnt = float(trozos[2])
    pAct = float(trozos[1])
    if pAct > pAnt * 1.1:
        print (trozos[0])
    linea = F.readline()
F.close()