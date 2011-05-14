#!/usr/bin/env python
# encoding: utf-8

import random
from BrachFitness import calcBrachTime as fitness

size_pop = input("Tamanho da população: ")
n_points = input("Numero de pontos: ")
while 1:
	pgene = input("Probabilidade de mutação (0-1): ")
	if pgene >= 0 and pgene <= 1:
		break
	
while 1:
	prec = input("Probabilidade de recombinação (0-1): ")
	if prec >= 0 and prec <= 1:
		break

while 1:
	seleccao = raw_input("Seleccao:\n  1-Roleta\n  2-Torneio\n")
	if seleccao == '1' or seleccao == '2':
		break
tsize = input("Tamanho do torneio: ")
start = [int(s) for s in raw_input("Coordenadas do ponto de partida (x y): ").split()]

while 1:
	finish = [int(s) for s in raw_input("Coordenadas do ponto de chegada (x y): ").split()]
	if start[1]>finish[1] and start[0]<finish[0]:
		break

elite = input("Elitismo: ")

def create_indiv(npoints):
	indiv = [0 for i in xrange(npoints)]
	step = (finish[0]-start[0])/npoints
	
	for i in xrange(0,npoints*2,2):
		indiv[i] = (i+1)*step
		indiv[i+1] = random.random()*start[1] # menor que o Y inicial
	
	return indiv

def create_population(size_pop):
	pop = [0 for i in xrange(size_pop*2)]
	
	for i in xrange(size_pop):
		pop[i] = create_indiv()
	
	return pop

def recnpoints(npoints, individuos):
	size = len(individuos)
	
	size_i = len(individuos[0])
	
	chosen = [-1 for i in xrange(npoints)]
	num = 0
	for i in xrange(npoints):
		while num not in chosen:
			num = random.randint(0, size_i)
		chosen[i] = num
	
	ind1 = random.randint(0, size)
	while 1:
		ind2 = random.randint(0, size)
		if ind1 != ind2:
			break
	
	chosen.sort()
	
	prev = 0
	for i in xrange(npoints):
		individuos[ind1][prev:chosen[i]], individuos[ind2][prev:chosen[i]] = individuos[ind2][prev:chosen[i]], individuos[ind1][prev:chosen[i]]
		prev = chosen[i]


def tournament(individuos, tsize):
	elements = random.sample(xrange(len(individuos)),tsize)
	
	values = [[0,0] for i in xrange(elements)]
	j = 0
	for i in elements:
		values[j] = [fitness(individuos[i]),i]
		j += 1
	best = min(values) #minimization
	return best[1]


def roulette():
	elements = random.sample(xrange(len(individuos)),tsize)
	


def mutation(individuo):
	point = random.randint(0,n_points)
	
	individuo[point*2+1] = random.random()*start[1] # menor que o Y inicial

