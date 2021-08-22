arq_um = open("arq_1", "r")
arq_dois = open("arq_2", "w")
arq_tres = open("arq_3", "w")
arq_lido = arq_um.read()
contador = 0
dicionario = {}
compressao = []

for letra in arq_lido:
    if not letra in dicionario:
        if not contador > 9:
            dicionario[letra] = contador
            compressao.append(contador)
            contador += 1
        else:
            dicionario[letra] = "#" + str(contador)
            resultado = "#" + str(contador)
            compressao.append(resultado)
            contador += 1

    else:
        for teste_letra in dicionario:
            if teste_letra == letra:
                compressao.append(dicionario[letra])

for i in compressao:
    arq_dois.write(str(i))
print(dicionario)

arq_dois = open("arq_2", "r")
arq_lido_dois = arq_dois.read()

cont = 0
contador_flag = 0

for letra_dois in arq_lido_dois:
    cont += 1
    if contador_flag == 0:
        for teste_letra in dicionario:
            if not letra_dois == "#":
                if int(letra_dois) == dicionario[teste_letra]:
                    arq_tres.write(teste_letra)
            else:
                contador_flag = 2
                if "#" + arq_lido_dois[cont] + arq_lido_dois[cont+1] == dicionario[teste_letra]:
                    arq_tres.write(teste_letra)
    else:
        contador_flag -= 1

