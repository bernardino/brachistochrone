#!/usr/bin/env python
# encoding: utf-8

import random
from BrachFitness import calcBrachTime as fitness
from operator import itemgetter

size_gen = input("Número de gerações: ")
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
		seleccao = int(seleccao)
		break
tsize = input("Tamanho do torneio: ")
start = [int(s) for s in raw_input("Coordenadas do ponto de partida (x y): ").split()]

while 1:
	finish = [int(s) for s in raw_input("Coordenadas do ponto de chegada (x y): ").split()]
	if start[1]>finish[1] and start[0]<finish[0]:
		break

elite = input("Elitismo: ")

def create_indiv(npoints):
	indiv = [0 for i in xrange(npoints*2)]
	step = float(finish[0]-start[0])/(npoints+2)
	j=0
	for i in xrange(0,npoints*2,2):
		indiv[i] = start[0]+(j+1)*step
		indiv[i+1] = random.random()*start[1] # menor que o Y inicial
		j+=1
	return indiv

def create_population(size_pop):
	pop = [0 for i in xrange(size_pop)]
	
	for i in xrange(size_pop):
		pop[i] = create_indiv(n_points)
	
	return pop

def recnpoints(npoints, individuos):
	size = len(individuos)
	
	size_i = len(individuos[0][0])
	
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
		individuos[ind1][0][prev:chosen[i]], individuos[ind2][0][prev:chosen[i]] = individuos[ind2][0][prev:chosen[i]], individuos[ind1][0][prev:chosen[i]]
		prev = chosen[i]


def tournament(individuos, tsize):
	elements = random.sample(individuos, tsize)
	elements.sort(key=itemgetter(1)) # minimization
	return elements[0]


def roulette(individuos):
	element = random.randint(0,size_pop-1)
	return individuos[element]	


def mutation(individuo):
	point = random.randint(0,n_points)
	
	individuo[0][point*2+1] = random.random()*start[1] # menor que o Y inicial


def brachistochrone():
	# create initial population
	population = create_population(size_pop)
	# evaluate population
	population = [[indiv, fitness(start+indiv+finish)] for indiv in population]	
	population.sort(key=itemgetter(1))
	
	for generation in xrange(size_gen):
		# select parents
		if seleccao==1: # tournament
			parents = [tournament_selection(population, tsize) for i in xrange(size_pop)]
		else: # roulette
			parents = [roulette(population) for i in xrange(size_pop)]
		
		# produce offspring
		offspring = []
		
		# crossover
		for i in xrange(size_pop):
			if random.random() < prec:
				offspring.append(recnpoints(parents[i]))
			else:
				offspring.append(parents[i])
		
		# mutation
		for i in xrange(size_pop):
			if random.random() < pgene:
				offspring[i] = mutation(parents[i])
			else:
				offspring[i] = parents[i]
		
		# evaluate offspring
		offspring = [[indiv[0], fitness(start+indiv[0]+finish)] for indiv in offspring]
		offspring.sort(key=itemgetter(1))
		# select survivors
		population[size_pop-elite:] = offspring[:elite]
		population.sort(key=itemgetter(1))
	print "Best took %f seconds " %population[0][1]

print "\nRoleta"
for i in xrange(10):
	brachistochrone()
seleccao = 2
print "\nTorneio"
for i in xrange(10):
	brachistochrone()