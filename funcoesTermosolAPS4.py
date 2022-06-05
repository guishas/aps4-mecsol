# -*- coding: utf-8 -*-
"""
A funcao 'plota' produz um gráfico da estrutura definida pela matriz de nos N 
e pela incidencia Inc.

Sugestao de uso:

from funcoesTermosol import plota
plota(N,Inc)
-------------------------------------------------------------------------------
A funcao 'importa' retorna o numero de nos [nn], a matriz dos nos [N], o numero
de membros [nm], a matriz de incidencia [Inc], o numero de cargas [nc], o vetor
carregamento [F], o numero de restricoes [nr] e o vetor de restricoes [R] 
contidos no arquivo de entrada.

Sugestao de uso:
    
from funcoesTermosol import importa
[nn,N,nm,Inc,nc,F,nr,R] = importa('entrada.xlsx')
-------------------------------------------------------------------------------
A funcao 'geraSaida' cria um arquivo nome.txt contendo as reacoes de apoio Ft, 
deslocamentos Ut, deformacoes Epsi, forcas Fi e tensoes Ti internas. 
As entradas devem ser vetores coluna.

Sugestao de uso:
    
from funcoesTermosol import geraSaida
geraSaida(nome,Ft,Ut,Epsi,Fi,Ti)
-------------------------------------------------------------------------------

"""
def plota(N,Inc):
    # Numero de membros
    nm = len(Inc[:,0])
    
    import matplotlib as mpl
    import matplotlib.pyplot as plt

#    plt.show()
    fig = plt.figure()
    # Passa por todos os membros
    for i in range(nm):
        
        # encontra no inicial [n1] e final [n2] 
        n1 = int(Inc[i,0])
        n2 = int(Inc[i,1])        

        plt.plot([N[0,n1-1],N[0,n2-1]],[N[1,n1-1],N[1,n2-1]],color='r',linewidth=3)


    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.grid(True)
    plt.axis('equal')
    plt.show()
    
def importa(entradaNome):
    
    import numpy as np
    import xlrd
    
    arquivo = xlrd.open_workbook(entradaNome)
    
    ################################################## Ler os nos
    nos = arquivo.sheet_by_name('Nos')
    
    # Numero de nos
    nn = int(nos.cell(1,3).value)
                 
    # Matriz dos nós
    N = np.zeros((2,nn))
    
    for c in range(nn):
        N[0,c] = nos.cell(c+1,0).value
        N[1,c] = nos.cell(c+1,1).value
    
    ################################################## Ler a incidencia
    incid = arquivo.sheet_by_name('Incidencia')
    
    # Numero de membros
    nm = int(incid.cell(1,5).value)
                 
    # Matriz de incidencia
    Inc = np.zeros((nm,4))
    
    for c in range(nm):
        Inc[c,0] = int(incid.cell(c+1,0).value)
        Inc[c,1] = int(incid.cell(c+1,1).value)
        Inc[c,2] = incid.cell(c+1,2).value
        Inc[c,3] = incid.cell(c+1,3).value
    
    ################################################## Ler as cargas
    carg = arquivo.sheet_by_name('Carregamento')
    
    # Numero de cargas
    nc = int(carg.cell(1,4).value)
                 
    # Vetor carregamento
    F = np.zeros((nn*2,1))
    
    for c in range(nc):
        no = carg.cell(c+1,0).value
        xouy = carg.cell(c+1,1).value
        GDL = int(no*2-(2-xouy)) 
        F[GDL-1,0] = carg.cell(c+1,2).value
         
    ################################################## Ler restricoes
    restr = arquivo.sheet_by_name('Restricao')
    
    # Numero de restricoes
    nr = int(restr.cell(1,3).value)
                 
    # Vetor com os graus de liberdade restritos
    R = np.zeros((nr,1))
    
    for c in range(nr):
        no = restr.cell(c+1,0).value
        xouy = restr.cell(c+1,1).value
        GDL = no*2-(2-xouy) 
        R[c,0] = GDL-1


    return nn, N, nm, Inc, nc, F, nr, R

def geraSaida(nome,Ft,Ut,Epsi,Fi,Ti):
    nome = nome + '.txt'
    f = open(nome,"w+")
    f.write('Reacoes de apoio [N]\n')
    f.write(str(Ft))
    f.write('\n\nDeslocamentos [m]\n')
    f.write(str(Ut))
    f.write('\n\nDeformacoes []\n')
    f.write(str(Epsi))
    f.write('\n\nForcas internas [N]\n')
    f.write(str(Fi))
    f.write('\n\nTensoes internas [Pa]\n')
    f.write(str(Ti))
    f.close()
    
def gauss(ite, tol, K, F):

    size = len(K)

    xs = [0]*size
    lasts = [0]*size
    errors = [0]*size

    contador = 0

    for i in range(0, ite):
        contador+=1

        for k in range(0, size):
            soma = 0
            for j in range(0, size):
                if k != j:
                    soma += (K[k][j]*xs[j])
            
            if K[k][k] == 0:
                xs[k] = 0
            else:
                xs[k] = (F[k] - soma)/K[k][k]

        for g in range(0, size):
            if xs[g] == 0:
                errors[g] = 0
            else:
                errors[g] = (xs[g] - lasts[g])/xs[g]

        count = 0
        for l in range(0, size):
            if errors[l] < tol:
                count+=1

        if count == size:
            break

        for x in range(0, size):
            lasts[x] = xs[x]

    return xs, contador

def jacobi(ite, tol, K, F):

    size = len(K)

    xs = [0]*size
    lasts = [0]*size
    errors = [0]*size

    contador = 0

    for i in range(0, ite):
        contador+=1

        for k in range(0, size):
            soma = 0
            for j in range(0, size):
                if k != j:
                    soma += (K[k][j]*lasts[j])
            
            xs[k] = (F[k] - soma)/K[k][k]

        for g in range(0, size):
            if xs[g] == 0:
                errors[g] = 0
            else:
                errors[g] = (xs[g] - lasts[g])/xs[g]

        count = 0
        for l in range(0, size):
            if errors[l] < tol:
                count+=1

        if count == size:
            break

        for x in range(0, size):
            lasts[x] = xs[x]

    return xs, contador

def rigidez(nm, Inc, N, nn, R, F):
    import math
    import numpy as np

    elementos = {}

    for n in range(1, nm+1):
        elementos[str(n)] = {}

    for n in range(1, nm+1):
        elementos[str(n)]['INCIDENCIA'] = '{}-{}'.format(Inc[n-1][0], Inc[n-1][1])

    for elemento, valores in elementos.items():
        f = int(valores['INCIDENCIA'][0:1]) - 1
        t = int(valores['INCIDENCIA'][4:5]) - 1

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

    for n in range(0, nm):
        elementos[str(n+1)]['YOUNG'] = int(Inc[n][2])

    for n in range(0, nn):
        g = n+1
        g1 = (g*2)-1
        g2 = g*2
        elementos[str(n+1)]['LIBERDADE'] = [g1, g2]

    K_list = []
    K_indexes = []
    for n in range(0, nm):
        cos = elementos[str(n+1)]['COS']
        sen = elementos[str(n+1)]['SEN']
        youngs = elementos[str(n+1)]['YOUNG']
        area = elementos[str(n+1)]['AREA']
        tamanho = elementos[str(n+1)]['TAMANHO']

        inc1 = elementos[str(n+1)]['INCIDENCIA'][0:1]
        inc2 = elementos[str(n+1)]['INCIDENCIA'][4:5]
        
        g1 = elementos[inc1]['LIBERDADE']
        g2 = elementos[inc2]['LIBERDADE']

        idxs = [g1[0], g1[1], g2[0], g2[1]]
        K_indexes.append(idxs)

        K = [[cos**2, cos*sen, -1*(cos**2), -1*(cos*sen)],
             [cos*sen, sen**2, -1*(cos*sen), -1*(sen**2)],
             [-1*(cos**2), -1*(cos*sen), cos**2, cos*sen],
             [-1*(cos*sen), -1*(sen**2), cos*sen, sen**2]]

        c = int((youngs*area)/tamanho)


        kl = []
        kll = []
        for i in range(0, len(K)):
            for j in range(0, len(K)):
                kl.append(c*K[i][j])

            kll.append(kl)
            kl = []
        K_list.append(kll)

    gl = nn*2
    kg = np.zeros((gl, gl))

    for i in range(0, gl):
        for j in range(0, gl):
            
            soma = 0
            for k in range(0, nm):
                if ((i+1) in K_indexes[k] and (j+1) in K_indexes[k]):
                    idx1 = K_indexes[k].index(i+1)
                    idx2 = K_indexes[k].index(j+1)
                    soma += K_list[k][idx1][idx2]

            kg[i][j] = soma

    ## FORÇAS 

    mF = []

    for i in range(0, nn*2):
        mF.append(F[i][0])

    gauss_matrix = []
    gauss_forces = []
    for n in range(0, gl):
        if n not in R:
            gauss_forces.append(mF[n])

            l = []
            for i in range(0, gl):
                if i not in R:
                    l.append(kg[n][i])

            gauss_matrix.append(l)

    xs, contador = gauss(3000, 1e-7, gauss_matrix, gauss_forces)

    return xs, kg, gauss_matrix

def apoio(R, nr, nn, kg):
    import numpy as np

    apoios = R

    for a in range(nr):
        r = int(R[a][0])
        xs = np.insert(xs, r, 0, 0)

    for i in range(0, nr):
        a = int(R[i][0])
        for x in range(0, nn*2):
            apoios[i] += xs[x]*kg[a][x]