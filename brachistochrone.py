#!/usr/bin/env python
# encoding: utf-8

import random
from BrachFitness import calcBrachTime as fitness
from operator import itemgetter

best = []
size_gen = input("Número de gerações: ")
size_pop = input("Tamanho da população: ")
n_points = input("Numero de pontos: ")
representacao = input("Representação (1-2):")
elite = input("Elitismo: ")

while 1:
	pgene = input("Probabilidade de mutação (0-1): ")
	if pgene >= 0 and pgene <= 1:
		break
	
while 1:
	prec = input("Probabilidade de recombinação (0-1): ")
	if prec >= 0 and prec <= 1:
		if prec>0:
			rec_points = input("Numero de pontos para recombinação: ")
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

def create_indiv(npoints):
	indiv = [0 for i in xrange(npoints*2)]
	step = float(finish[0]-start[0])/(npoints+2)
	j=0
	for i in xrange(0,npoints*2,2):
		indiv[i] = start[0]+(j+1)*step
		indiv[i+1] = random.random()*start[1] # menor que o Y inicial
		j+=1
	return indiv


def create_indiv_2(npoints):
	indiv = [0 for i in xrange(npoints*2)]
	num = 0.0
	dist = finish[0]-start[0]
	x = [0.0 for i in xrange(npoints)]
	for i in xrange(npoints):
		while num in x:
			num = random.random()*float(dist)
		x[i] = num
	
	x.sort()
	
	j=0
	for i in xrange(0,npoints*2,2):
		indiv[i+1] = random.random()*start[1] # menor que o Y inicial
		indiv[i] = x[j]+start[0]
		j += 1
	
	return indiv

def create_population(size_pop):
	pop = [0 for i in xrange(size_pop)]
	
	if representacao == 1:
		for i in xrange(size_pop):
			pop[i] = create_indiv(n_points)
	else:
		for i in xrange(size_pop):
			pop[i] = create_indiv_2(n_points)
	
	return pop

def recnpoints(individuo1, individuo2):
	size_i = len(individuo1[0])
	
	chosen = [-1 for i in xrange(rec_points)]
	num = 0
	for i in xrange(rec_points):
		while num in chosen:
			num = random.randint(0, size_i-1)
		chosen[i] = num
	
	chosen.sort()
	
	prev = 0
	for i in xrange(rec_points):
		individuo1[0][prev:chosen[i]], individuo2[0][prev:chosen[i]] = individuo2[0][prev:chosen[i]], individuo1[0][prev:chosen[i]]
		prev = chosen[i]
	
	return [individuo1, individuo2]


def tournament(individuos, tsize):
	elements = random.sample(individuos, tsize)
	elements.sort(key=itemgetter(1)) # minimization
	
	return elements[0]


def roulette(individuos):
	element = random.randint(0,size_pop-1)
	return individuos[element]	


def mutation(individuo):
	point = random.randint(0,n_points-1)
	
	individuo[0][point*2+1] = random.random()*start[1] # menor que o Y inicial
	return individuo


def brachistochrone():
	# create initial population
	population = create_population(size_pop)
	
	# evaluate population
	population = [[indiv, fitness(start+indiv+finish)] for indiv in population]	
	population.sort(key=itemgetter(1))
	
	for generation in xrange(size_gen):
		# select parents
		if seleccao==2: # tournament
			parents = [tournament(population, tsize) for i in xrange(size_pop)]
		else: # roulette
			parents = [roulette(population) for i in xrange(size_pop)]
		
		# produce offspring
		offspring = []
		
		# crossover
		for i in xrange(0, size_pop,2):
			if random.random() < prec:
				offspring.extend(recnpoints(parents[i],parents[i+1]))
			else:
				offspring.extend([parents[i],parents[i+1]])
		
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
	best.append(population[0][1])
	return True

seleccao = 1
print "\nRoleta"
seed = random.random()*10000
random.seed(seed)
for i in xrange(10):
	brachistochrone()
print "AVERAGE: %f" %(sum(best)/10)
seleccao = 2
best = []
seed = random.random()*10000
random.seed(seed)
print "\nTorneio"
for i in xrange(10):
	brachistochrone()
print "AVERAGE: %f" %(sum(best)/10)