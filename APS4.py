from funcoesTermosolAPS4 import importa, plota, geraSaida, gauss, jacobi
import math

def solver():
    # nn = Número de nós
    # N = Matriz com a posição dos nós em metros
    # nm = Número de membros
    # Inc = Matriz com os membros, módulos de elasticidade (Pa) e áreas (m2)
    # nc = Número de cargas (forças)
    # F = Matriz com a posição das forças e os módulos
    # nr = Número de restrições
    # R = Matriz com a posição de cada restrição
    nn, N, nm, Inc, nc, F, nr, R = importa('entrada.xls')

    elementos = {}

    for n in range(1, nn+1):
        elementos[str(n)] = {}

    for n in range(1, nn):
        elementos[str(n)]['INCIDENCIA'] = '{}-{}'.format(n, n+1)
    
    elementos[str(nn)]['INCIDENCIA'] = '{}-{}'.format(nn, 1)

    for elemento, valores in elementos.items():
        f = int(valores['INCIDENCIA'][0:1]) - 1
        t = int(valores['INCIDENCIA'][2:3]) - 1

        x1 = N[0][f]
        y1 = N[1][f]
        x2 = N[0][t]
        y2 = N[1][t]

        L = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        elementos[elemento]['TAMANHO'] = L
        elementos[elemento]['SEN'] = (y2-y1)/L
        elementos[elemento]['COS'] = (x2-x1)/L
        
    for n in range(0, nm):
        elementos[str(n+1)]['AREA'] = Inc[n][3]

    print(elementos)

    #print(Inc)

    #plota(N, Inc)

solver()