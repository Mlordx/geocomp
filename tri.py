#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from geocomp.common.polygon import Polygon
from geocomp.common import prim
from geocomp.common import control
from geocomp.common.segment import Segment
from geocomp.common.guiprim import *
from geocomp import config
from geocomp.common.point import Point
"""
Implementação do algoritmo de triangulação de polígonos monótonos(Para posteriormente ser usado com o algoritmo de Lee e Preparata, mas por enquanto deixo ele aqui
para ser usado sozinho no programa)
"""

def triangulaMonotono(l):#Os pontos devem vir em ordem anti-horária
    pontos = [] #lista com os pontos,juntamente com seus indices
    verts = [] #lista com os pontos ordenados
    pilha = [] #pilha usada no algoritmo
    diagonais = [] #lista de diagonais da triangulação
    lado = []

    for x in range(len(l)):#desenha poligono
        if(x != len(l)-1): l[x].lineto(l[(x+1)],'red')
        else: l[x].lineto(l[0],'red')
                                        
    N = len(l)

    for i in range(N): 
        pontos.append((l[i],i)) #transforma cada ponto numa dupla (ponto,indice)
        lado.append(True)
    
    ########################################### 
    #Esse pedaço acha o vertice mais alto e o mais baixo e realiza o merge
    yMax = -20000000
    yMin = 2000000
    vMax = pontos[0]
    vMin = pontos[N-1]

    for i in range(N):
        if(pontos[i][0].y == yMax and pontos[i][0].x < vMax[0].x): vMax = pontos[i]
        if(pontos[i][0].y == yMin and pontos[i][0].x > vMin[0].x): vMin = pontos[i]
        if(pontos[i][0].y > yMax):
            vMax = pontos[i]
            yMax = vMax[0].y
        if(pontos[i][0].y < yMin):
            vMin = pontos[i]
            yMin = vMin[0].y
            
    if(vMax[1] != N-1):v = pontos[vMax[1]+1]
    else: v = pontos[0]
            
    if(vMax[1]!= 0): i = vMax[1]-1
    else: i = N-1

    if(vMax[1]!= N-1):j = vMax[1]+1
    else: j = 0

    lado[vMin[1]] = False

    if(vMax[1]!= 0): i = vMax[1]-1
    else: i = N-1

    if(vMax[1]!= N-1):j = vMax[1]+1
    else: j = 0            

    verts.append(vMax);
    while(len(verts) < N): #Merge
        if(pontos[j] == vMin):
            while(pontos[i] != vMin):
                verts.append(pontos[i])
                if(i!=0):i -= 1
                else: i = N-1
        elif(pontos[i] == vMin):
            while(pontos[j] != vMin):
                lado[pontos[j][1]] = False
                verts.append(pontos[j])
                if(j != N-1):j += 1
                else: j = 0

        if((pontos[j][0].y >= pontos[i][0].y)):
            lado[pontos[j][1]] = False
            verts.append(pontos[j])
            if(j != N-1): j+= 1
            else: j = 0
        else:
            verts.append(pontos[i])
            if(i!=0):i -= 1
            else: i = N-1

    ########################################

    #verts = sorted(pontos,key=lambda x: (x[0].y,-x[0].x), reverse=True)	 
    for i in range(N):
        if(lado[i] == True): pontos[i][0].hilight("blue")
        else: pontos[i][0].hilight("green")

    print verts

    pilha.append(verts[0])
    pilha.append(verts[1])

    for i in range(2,N):
        t = len(pilha)
        print "____________________"
        print pilha
        verts[i][0].hilight("yellow")
        control.sleep()
        if(verts[i][1] == 0): ant = len(l)-1
        else: ant = verts[i][1]-1

        if(verts[i][1] == len(l)-1): prox = 0
        else: prox = verts[i][1]+1

        #aqui pilha[t-1][1] é o St e pilha[0][1] o S1, de acordo com os slides

   #Caso A ########################
        if((ant == pilha[t-1][1] and prox != pilha[0][1]) or (ant != pilha[0][1] and prox == pilha[t-1][1])): #adjacente a St mas nao a S1   
            print "Entrei no caso A" , "no vertice ",verts[i][0]
            if(lado[pilha[t-1][1]] == True):   
                while(t>1 and left_on(pilha[t-1][0],pilha[t-2][0],verts[i][0]) ):                
                    pilha.pop()
                    t -= 1
                    diagonais.append(Segment(verts[i][0],pilha[t-1][0]))
                    d = Segment(verts[i][0],pilha[t-1][0])
                    d.hilight("blue")
                    control.sleep()
                    print "Adicionei a diagonal ", d
            elif(t>1):
                while(t>1 and right_on(pilha[t-1][0],pilha[t-2][0],verts[i][0])):
                    
                    pilha.pop()
                    t -= 1
                    diagonais.append(Segment(verts[i][0],pilha[t-1][0]))
                    d = Segment(verts[i][0],pilha[t-1][0])
                    d.hilight("blue")
                    control.sleep()
                    print "Adicionei a diagonal ", d
                    
            pilha.append(verts[i])

   #Caso B ########################
        if((ant != pilha[t-1][1] and prox == pilha[0][1]) or (ant == pilha[0][1] and prox != pilha[t-1][1])): #adjacente a S1 mas nao a St
            print "Entrei no caso B"  , "no vertice ",verts[i][0]
            aux = pilha[t-1]
            while(t>1):
                diagonais.append(Segment(verts[i][0],pilha[t-1][0]))
                d = Segment(verts[i][0],pilha[t-1][0])
                d.hilight("blue")
                control.sleep()
                print "Adicionei a diagonal ", d
                pilha.pop()
                t -= 1
            pilha.pop()
            pilha.append(aux)
            pilha.append(verts[i])
   #Caso C ########################
        if((ant == pilha[t-1][1] and prox == pilha[0][1]) or (ant == pilha[0][1] and prox == pilha[t-1][1])): #adjacente a St e S1
            print "Entrei no caso C", "no vertice ",verts[i][0]
            pilha.pop()
            while(t>2):
                t -= 1
                diagonais.append(Segment(verts[i][0],pilha[t-1][0]))
                d = Segment(verts[i][0],pilha[t-1][0])
                d.hilight("blue")
                control.sleep()
                print "Adicionei a diagonal ", d
                pilha.pop()
        verts[i][0].hilight("red")
        print "--------------------"
