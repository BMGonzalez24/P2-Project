__author__ = 'Bruno Gonzalez, 56941; João Leal, 56922.'

import re
import argparse
import csv
import matplotlib.pyplot as plt
import numpy as np

chaves = {
    'game_id'       :  0,
    'pgn'           :  2,
    'time_control'  :  3,
    'end_time'      :  4,
    'time_class'    :  6,
    'white_username':  9,
    'white_result'  : 11,
    'black_username': 12,
    'black_result'  : 14,}

############################## FUNÇÕES AUXILIARES ##############################
def ler_csv_lista(ficheiro_csv, x):
    """Lê um ficheiro csv e transforma as linhas de uma coluna em elementos de uma lista. 

    Args:
        ficheiro_csv (str): Nome do ficheiro csv
        x (int): Número da coluna presente no dicionário "chaves"

    Returns:
        list: Lista dos elementos de uma coluna.
    """
    final = []
    with open(ficheiro_csv, 'r') as ficheiro:
        leitor = csv.reader(ficheiro, delimiter=',')
        for i in leitor:
            final.append(i[chaves[x]])
    return final[:]

def ler_csv_dicionario(ficheiro_csv, x, y, tamanhoX=None, tamanhoY=None):
    dic = { }
    with open(ficheiro_csv, 'r') as ficheiro:
        leitor = csv.reader(ficheiro, delimiter=',')
        next(leitor)
        for i in leitor:
            if i[chaves[x]][:tamanhoX].lower() in dic.keys():
                dic[ i[chaves[x]][:tamanhoX].lower() ].append( i[chaves[y]][:tamanhoY] )
            else:
                dic[ i[chaves[x]][:tamanhoX].lower() ] = [ i[chaves[y]][:tamanhoY] ]
    return dic

def adicionar_a_dic(ficheiro_csv, dic, x, y, tamanhoX=None, tamanhoY=None):
    with open(ficheiro_csv, 'r') as ficheiro:
        leitor = csv.reader(ficheiro, delimiter=',')
        next(leitor)
        for i in leitor:
            if i[chaves[x]][:tamanhoX].lower() not in dic.keys():
                dic[ i[chaves[x]][:tamanhoX].lower() ] = [ i[chaves[y]][:tamanhoY] ]
            else: 
                dic[ i[chaves[x]][:tamanhoX].lower() ].append( i[chaves[y]][:tamanhoY] )
    return dic

def remover_reptidos_dic(dic):
    for i in dic:
        filtrado = list(dict.fromkeys(dic[i]))
        dic[i] = filtrado
    return dic

def verificaMate(ficheiro_csv, dic, x, y):
    with open(ficheiro_csv, 'r') as ficheiro:
        leitor = csv.reader(ficheiro, delimiter=',')
        next(leitor)
        for i in leitor:
            if i[chaves[x]] == 'checkmated':
                if i[chaves[y]].lower() in dic.keys():
                    dic[ i[chaves[y]].lower() ] += 1
                else:
                    dic[ i[chaves[y]].lower() ] = 1
    return dic

def probabilidade(favoraveis, possiveis):
    """Calcula a robabilidade de um acontecimento

    Args:
        favoraveis (int): Número de casos favoráveis ao acontecimento
        possiveis (int): Número de casos possíveis

    Returns:
        float: Probabilidade de um acontecimento acontecer.
    """
    return (favoraveis/possiveis)

############################## ANOS #############################################
def anos(ficheiro_csv):
    """Faz o gráfico "anos", ou seja, para cada ano estão dois valores: número de jogos e número de jogadoras diferentes.

    Args:
        ficheiro_csv (str): Ficheiro csv com a informação

    Returns:
        graph: Gráfico desejado
    """
    anosNmrjogos  = ler_csv_dicionario(ficheiro_csv, 'end_time', 'game_id', 4)
    anosJogadores = ler_csv_dicionario(ficheiro_csv, 'end_time', 'white_username', 4)
    anosJogadores = adicionar_a_dic(ficheiro_csv, anosJogadores, 'end_time', 'black_username', 4)
    anosJogadores = remover_reptidos_dic(anosJogadores)

    anos = list(anosNmrjogos.keys())
    anos.sort()
    anosNmrjogos  = list(map(lambda x: len(anosNmrjogos[x]), anos))
    anosJogadores = list(map(lambda x: len(anosJogadores[x]), anos))

    pos = np.arange(len(anos))
    compBarra = 0.85

    fig, ax1 = plt.subplots()

    plt.xticks(rotation='vertical')
    plt.title('Jogos e jogadoras por ano')

    ax2 = ax1.twinx()
    ax1.bar(pos, anosNmrjogos, compBarra, color='green')
    ax1.legend(['#Jogos'], loc='center left')
    ax2.plot(anos, anosJogadores, color='blue')
    ax2.legend(['#Jogadoras diferentes'], loc='upper left')

    ax1.set_xlabel('Ano')
    ax1.set_ylabel('Jogos', color='green')
    ax2.set_ylabel('#Jogadoras diferentes', color='blue')
    return plt.show()

############################## CLASSES ##############################
def classes(ficheiro_csv, c=5):
    """Função que encaminha para outra de acordo com a classe escolhida

    Args:
        ficheiro_csv (str): Nome do ficheiro csv
        abc (int, optional): Número de abcissas que se pretende estudar. Defaults to 5.
        classes (str, optional): Classe que se pretende. Defaults to 'time_class'.
    """
    graficos = ['rapid','daily','bullet','blitz']
    for i in graficos:
        graficos_classes(ficheiro_csv, c, i)
    time_class(ficheiro_csv)

def time_class(ficheiro_csv):
    """Faz o grafico do time_class com as classes de jogos e o número de jogos para cada uma.

    Args:
        ficheiro_csv (str): Nome do ficheiro de xadrez
        classes (str, optional): Nome da coluna do ficheiro csv. Defaults to 'time_class'.
    """
    i = 0
    yJogos = []
    plt.title('time_class')
    plt.xlabel("Formato de jogo")
    plt.xticks(rotation='vertical')
    plt.ylabel("#Jogos")
    Tipos = ler_csv_lista(ficheiro_csv, 'time_class')
    xTipos = sorted(list(dict.fromkeys(Tipos)))
    while len(yJogos) < len(xTipos):
        yJogos.append(Tipos.count(xTipos[i]))
        i = i + 1
    plt.bar(xTipos, yJogos)
    plt.show()

def graficos_classes(ficheiro_csv, c, classes):
    """Faz o grafico para classes que não são o time_class.

    Args:
        ficheiro_csv (str): Nome do ficheiro csv
        c (int): Número de abcissas que se pretende
        classes (str): Classe de jogo que se pretende estudar
    """
    
    Tipos = ler_csv_lista(ficheiro_csv, 'time_class')
    Tempo = ler_csv_lista(ficheiro_csv, 'time_control')
    indices = [i for i in range(len(Tipos)) if Tipos[i]==classes]

    xTipos = []
    for x in indices:
        xTipos.append(Tempo[x])
    xTipos = list(dict.fromkeys(xTipos))
    print(xTipos)

    i = 0
    yJogos = []
    while len(yJogos) < len(xTipos):
        yJogos.append(Tempo.count(xTipos[i]))
        i = i + 1

    res = dict(zip(xTipos, yJogos))
    marklist = sorted(res.items(), key=lambda x:x[1], reverse=True)
    sortdict = dict(marklist)

    while len(sortdict) > c:
        sortdict.popitem()

    plt.title(classes)
    plt.xlabel("Formato de jogo")
    plt.xticks(rotation='vertical')
    plt.ylabel("#Jogos")
    plt.bar(*zip(*sortdict.items()))
    plt.show()

graficos_classes('xadrez.csv', 5, 'blitz')

############################## VITORIAS ##############################
def vitorias(ficheiro_csv, c=5, u=[]):
    """Mostra um gráfico que estuda as vitórias mostrando, para cada jogadora a percentagem de vezes que usa peças brancas ou pretas.

    Args:
        ficheiro_csv (str): Ficheiro com a informação
        c (int): Quantidade de colunas pretendidas
        u (str): Quantidade de utilizadores pretendida

    Returns:
        Graph: Gráfico pretendido
    """
    statsBranco = ler_csv_dicionario(ficheiro_csv, 'white_username', 'white_result')
    statsPreto  = ler_csv_dicionario(ficheiro_csv,'black_username', 'black_result')

    if u == []:
        organizar = adicionar_a_dic(ficheiro_csv, statsBranco, 'black_username', 'black_result')
        topJogadores = list(organizar.items())
        topJogadores = list( map( lambda x: (len(topJogadores[x][1]), topJogadores[x][0]) , range(0,len(topJogadores))))
        topJogadores.sort(reverse=True)
        nomes = list(map(lambda x: topJogadores[x][1].lower(), range(c)))
    
    if u != []:
        nomes = u

    jogosBrancos = list(map(lambda x: statsBranco[x], nomes))
    jogosBrancos = list(map(lambda x: x.count('win') / len(x), jogosBrancos))
    jogosPretos  = list(map(lambda x: statsPreto[x], nomes))
    jogosPretos  = list(map(lambda x: x.count('win') / len(x), jogosPretos))

    legenda = ['peças brancas','peças pretas']
    pos = np.arange(len(nomes))
    compBarra = 0.35
    plt.bar(pos-compBarra/2, jogosBrancos, compBarra, color='#cacaca')
    plt.bar(pos+compBarra/2, jogosPretos, compBarra, color='black')
    plt.xlabel('Jogadoras', fontsize=10)
    plt.xticks(np.arange(len(nomes)), nomes, rotation='vertical')
    plt.ylabel('Percentagem', fontsize=10)
    plt.title('Percentagem de vitórias jogando com\npeças brancas / pretas',fontsize=15)
    plt.legend(legenda,loc=1)
    return 



############################## SEGUINTE ##############################
def seguinte(ficheiro_csv, jogada='e4'):
    plt.title("Jogadas mais prováveis depois de " + jogada)
    plt.xlabel("Jogadas")
    plt.ylabel("Probabilidade")
    movimentos = moves(ficheiro_csv)
    indices = [i for i, val in enumerate(movimentos) if val==jogada]
    xJogadas = []
    yProb = []
    sem_jogada = xJogadas.remove(jogada)
    sem_rep = list(dict.fromkeys(sem_jogada))
    for x in xJogadas:
        yProb.append(probabilidade(sem_rep.count(x), len(sem_rep)))
    plt.bar(xJogadas, yProb)

def moves(ficheiro_csv):
    coluna_pgn = ler_csv_lista(ficheiro_csv, 'pgn')
    regex = re.compile(r'[BRQNK][a-h][1-8]| [a-h][1-8]|[BRQNK][a-h][a-h][1-8]|O-O|0-0-0|[BRQNK]x[a-h][1-8]|[a-h]x[a-h][1-8]|1\/2-1\/2|1\/-O|O-\/1')
    va_la = []
    for x in coluna_pgn:
        va_la.append(x.split(" "))
    strings = [item for sublist in va_la for item in sublist]
    filtrada = list(filter(lambda i : regex.search(i), strings))
    return filtrada

############################## MATE ##############################
def mate(ficheiro_csv, c=5):
    """Gráfico que mostra a percentagem de xeque-mate, jogos ganhos e jogos ganhos por xeque-mate

    Args:
        ficheiro_csv (str): Ficheiro com a informação
        c (int, optional): Número de colunas pretendidas. Defaults to 5.

    Returns:
        graph: Gráfico pretendido
    """
    jogadorasEJogos = adicionar_a_dic(ficheiro_csv, ler_csv_dicionario(ficheiro_csv, 'white_username', 'white_result'), 'black_username', 'black_result')
    topJogadores = list(jogadorasEJogos.items())
    topJogadores = list( map( lambda x: (len(topJogadores[x][1]), topJogadores[x][0]) , range(0,len(topJogadores))))
    topJogadores.sort(reverse=True)
    nrCheckmated   = {  }
    nrCheckmated   = verificaMate(ficheiro_csv, nrCheckmated, 'white_result', 'black_username')
    nrCheckmated   = verificaMate(ficheiro_csv, nrCheckmated, 'black_result', 'white_username')

    nomes          = list(map(lambda x: topJogadores[x][1].lower(), range(c)))
    nrJogosVitoria = list(map(lambda x: jogadorasEJogos[x].count('win'), nomes))
    nrCheckmated   = list(map(lambda x: nrCheckmated[x], nomes))
    nrPercentCheck = list(map(lambda x,y: int(x)/int(y), nrCheckmated, nrJogosVitoria))

    pos = np.arange(len(nomes))
    compBarra = 0.35

    fig, ax1 = plt.subplots()
    
    plt.xticks(rotation='vertical')
    plt.title('Percentagem de xeque-mate,\njogos ganhos, e jogos ganhos por xeque-mate')

    ax2 = ax1.twinx()
    ax1.bar(pos-compBarra/2, nrCheckmated, compBarra, color='#cacaca')
    ax1.bar(pos+compBarra/2, nrJogosVitoria, compBarra, color='blue')
    ax1.legend(['jogos ganhos por xeque-mate','jogos ganhos'], loc='upper right')
    ax2.plot(nomes, nrPercentCheck, color='red')
    ax2.legend(['percentagem\nde xeque-mate'], loc='center left')

    ax1.set_ylabel('#Jogos')
    ax2.set_ylabel('Percentagem de xeque-mate', color='red')
    return plt.show()

############################## ARGPARSE ##############################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('path', help='Caminho do ficheiro')
    parser.add_argument('function', type=str, help='Caminho do ficheiro')
    parser.add_argument('-c', '--c', type=int, required=False, default=5, help='Quantidade de jogadoras.')
    parser.add_argument('-u', '--u', required=False, nargs='+', default=[], help='Nomes de jogadoras')

    args = parser.parse_args()

    if args.function == 'anos':
        anos(args.path)

    elif args.function == 'classes':
        classes(args.path, args.c)

    elif args.function == 'vitorias':
        vitorias(args.path, args.c, args.u)

    elif args.function == 'seguinte':
        seguinte(args.path)

    elif args.function == 'mate':
        mate(args.path, args.c)