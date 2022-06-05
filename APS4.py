from funcoesTermosolAPS4 import importa, internas, plota, geraSaida, rigidez, apoio, deformacao, tensao, internas, novos_nos
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

    plota(N, Inc)

    xs, kg, elementos = rigidez(nm, Inc, N, nn, R, F, nr)
    
    apoios, u = apoio(R, nr, nn, kg, xs)

    deform = deformacao(u, elementos)

    tens = tensao(deform, elementos)

    interns = internas(tens, elementos)

    novos = novos_nos(N, u)

    plota(novos, Inc)

    new_xs = np.zeros((len(xs), 1))
    for i in range(len(xs)):
        new_xs[i][0] = xs[i]

    geraSaida("saida", apoios, new_xs, deform, interns, tens)

solver()