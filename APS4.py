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

    xs = rigidez(nm, Inc, N, nn, R, F)
    print(xs)

    

    #plota(N, Inc)

solver()