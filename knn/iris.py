import csv
import random
import math
import operator
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from Tkinter import *
import numpy as np

from interface_iris import Interface

#Ler o arquivo csv com os dados e o divide em duas variaves: treino e treste, na proporcao
def loadDados(arquivo, split, treino=[] , teste=[]):
    with open(arquivo, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dados = list(lines)
        for x in range(len(dados)-1):
            for y in range(4):
                dados[x][y] = float(dados[x][y])
            if random.random() < split:
                treino.append(dados[x])
            else:
                teste.append(dados[x])


#Calcular a distancia euclidiana
def euclideana(elemento, alvo, dim):
	distancia = 0
	for i in range(dim):
		distancia += pow((elemento[i] - alvo[i]), 2)
	return math.sqrt(distancia)

def amplitudes(treino, dim):
    tuplas = {}
    amplitudes = {'maximos':[], 'minimos':[]}
    #cria um dicionario com cada caracteristica sendo uma key
    for i in range(dim):
        tuplas[i] = []
    #Adiciona todas os valores de todos os dados a key de sua caracteristica correspondente
    for x in range(len(treino)):
        for y in range(dim):
             tuplas[y].append(treino[x][y])

    #Encontra o valor maximo e minimo de cada caracteristica
    for i in range(dim):
        maximo = max(tuplas[i])
        minimo = min(tuplas[i])
        amplitudes['maximos'].append(maximo)
        amplitudes['minimos'].append(minimo)

    return amplitudes
def gerarGraficos(conjunto, tipo):
    if tipo == "treino":
        for x in range(len(conjunto)):
            if(conjunto[x][-1]=="Iris-virginica"):
                plt.plot(conjunto[x][0], conjunto[x][1], 'bo')
            if(conjunto[x][-1]=="Iris-versicolor"):
                plt.plot(conjunto[x][0], conjunto[x][1], 'ro')
            elif(conjunto[x][-1]=="Iris-setosa"):
                plt.plot(conjunto[x][0], conjunto[x][1], 'go')
    elif tipo == "vizinhos":
        valoresx = [0] * len(conjunto)
        valoresy = [0] * len(conjunto)
        for i in range(len(conjunto)):
            valoresx[i] = conjunto[i][0]
            valoresy[i] = conjunto[i][1]
        plt.plot(valoresx, valoresy, linestyle='-', color='magenta',  linewidth=1.0)
    elif tipo == "centroides":
        for classe in conjunto.keys():
            if(classe=="Iris-virginica"):
                plt.plot(conjunto[classe][0], conjunto[classe][1], 'bo', markersize=15,  markerfacecolor = 'none')
            if(classe=="Iris-versicolor"):
                plt.plot(conjunto[classe][0], conjunto[classe][1], 'ro', markersize=15, markerfacecolor = 'none')
            elif(classe=="Iris-setosa"):
                plt.plot(conjunto[classe][0], conjunto[classe][1], 'go', markersize=15, markerfacecolor = 'none')
    elif tipo == "alvo":
        plt.plot(conjunto[0], conjunto[1], marker='s', color='yellow')


def normalizar(conjunto,amplitudes):
    if len(conjunto) > 6:
        dim = len(conjunto[0])-1
        #normaliza com base na formula v' =  v - min / max - min, onde v e o valor atual e v' o valor normalizado
        for x in range(len(conjunto)):
            for y in range(dim):
                conjunto[x][y] = (conjunto[x][y] - amplitudes['minimos'][y])/(amplitudes['maximos'][y] - amplitudes['minimos'][y])
    else:
        dim = len(conjunto)-1
        for y in range(dim):
            conjunto[y] = (conjunto[y] - amplitudes['minimos'][y])/(amplitudes['maximos'][y] - amplitudes['minimos'][y])
    return conjunto

def desnormalizar(conjunto,amplitudes,tipo):
    if tipo == "alvo":
        dim = len(conjunto)-1
        print dim
        for y in range(dim):
            conjunto[y] = (conjunto[y] * (amplitudes['maximos'][y] - amplitudes['minimos'][y]) + amplitudes['minimos'][y])
    else:
        dim = len(conjunto[0])-1
        #normaliza com base na formula v=   v'*(max - min)  + min, onde v e o valor atual e v' o valor normalizado
        for x in range(len(conjunto)):
            for y in range(dim):
                conjunto[x][y] = (conjunto[x][y] * (amplitudes['maximos'][y] - amplitudes['minimos'][y])) + amplitudes['minimos'][y]
    return conjunto

def acharVizinhos(treino, alvo, quantidade_vizinhos):
    distancias = []
    dimensao = len(alvo)-1
    #cria uma lista com todos os dados do treino e suas respectivas distancias
    for x in range(len(treino)):
        dist = euclideana(alvo, treino[x], dimensao)
        distancias.append((treino[x], dist))
    #ordena a lista pela distancia de cada dado
    distancias.sort(key=operator.itemgetter(1))
    vizinhos = []
    #Insere os vizinhos mais proximos de acordo com a quantidade passada
    for y in range(quantidade_vizinhos):
        vizinhos.append(distancias[y][0])
    return vizinhos

def acharResposta(vizinhos):
    #dicionarios com as respostas
    respostas = {}
    for x in range(len(vizinhos)):
        resposta = vizinhos[x][-1]
        if resposta in respostas:
            respostas[resposta] += 1
        else:
            respostas[resposta] = 1
    #respostas ordenadas de acordo com as que mais sao usadas
    respostas = sorted(respostas.iteritems(), key=operator.itemgetter(1), reverse=True)
    resposta = respostas[0][0]
    if len(respostas)>1:
        resposta_alternativa = respostas[1][0]
    return resposta

def medirPrecisao(teste, respostas):
    correto = 0
    for i in range(len(teste)):
        if teste[i][-1] == respostas[i]:
            correto += 1
    precisao = (correto/float(len(teste)))*100.0
    return precisao

def centroide(treino, alvo):
    classes = {}
    for x in range(len(treino)-1):
        classe = treino[x][-1]
        if classe not in classes:
            classes[classe] = []
            for atributo in range(len(treino[x])-1):
                classes[classe] += [treino[x][atributo]]
            classes[classe] += [1]
        else:
            for atributo in range(len(treino[x])-1):
                classes[classe][atributo] += treino[x][atributo]
            classes[classe][-1] += 1

    distancias = []
    for classe in classes.keys():
        for atributo in range(len(classes[classe])-1):
            classes[classe][atributo] = classes[classe][atributo]/classes[classe][-1]
        dist = euclideana(alvo, classes[classe], len(alvo)-1)
        distancias.append((dist, classe))
    gerarGraficos(classes,"centroides")
    distancias.sort()
    return distancias[0][1]


def main(valores_alvo, quantidade_vizinhos):
    response = ['','']
    treino = []
    teste = []
    split = 0.67
    respostas_teste = []
    loadDados('IRIS.csv', split, treino, teste)
    porCentroide = centroide(treino, valores_alvo)
    dimensao = 4
    gerarGraficos(treino, "treino")
    print len(teste)
    print len(treino)
    amplitudesTuplas = amplitudes(treino,dimensao)
    treino = normalizar(treino, amplitudesTuplas)
    teste = normalizar(teste, amplitudesTuplas)

    # valor a ser descoberto com grafico de seus vizinhos
    valores_alvo = normalizar(valores_alvo, amplitudesTuplas)
    vizinhos = acharVizinhos(treino, valores_alvo, quantidade_vizinhos)
    vizinhos = desnormalizar(vizinhos, amplitudesTuplas, "vizinhos")
    gerarGraficos(vizinhos, "vizinhos")
    gerarGraficos(desnormalizar(valores_alvo, amplitudesTuplas, "alvo"), "alvo")


    response[0] = acharResposta(vizinhos)


    for i in range(len(teste)):
        vizinhos_teste = acharVizinhos(treino, teste[i], quantidade_vizinhos)
        resposta_teste = acharResposta(vizinhos_teste)
        respostas_teste.append(resposta_teste)

    precisao = medirPrecisao(teste, respostas_teste)
    response[1] = precisao
    response += [porCentroide]

    return response



root = Tk()

Interface(root)
root.mainloop()
