from funcoesTermosolAPS4 import importa, plota, geraSaida, rigidez
import math
import numpy as np

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

    xs, kg, gauss_matrix = rigidez(nm, Inc, N, nn, R, F)
    
    apoios = R

    for a in range(nr):
        r = int(R[a][0])
        xs = np.insert(xs, r, 0, 0)

    for i in range(0, nr):
        a = int(R[i][0])
        for x in range(0, nn*2):
            apoios[i] += xs[x]*kg[a][x]

    print(apoios)

    print(xs)

    

    #plota(N, Inc)

solver()