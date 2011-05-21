#!/usr/bin/env python
# encoding: utf-8

import random, math, sys, time
from BrachFitness import calcBrachTime as fitness
from operator import itemgetter
from xturtle import *

FILE = open("results.txt",'w')

best = []
size_gen = input("Numero de geraçoes: ")
size_pop = input("Tamanho da populaçao: ")
n_points = input("Numero de pontos: ")

while 1:
	representacao = raw_input("Representação:\n  1-Pontos com espaçamento bem definido\n  2-Pontos espaçados aleatoriamente\n")
	if representacao=='1' or representacao=='2':
		representacao = int(representacao)
		break

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

if seleccao==2:
	tsize = input("Tamanho do torneio: ")

start = [int(s) for s in raw_input("Coordenadas do ponto de partida (x y): ").split()]

while 1:
	finish = [int(s) for s in raw_input("Coordenadas do ponto de chegada (x y): ").split()]
	if start[1]>finish[1] and start[0]<finish[0]:
		break


def create_indiv(npoints):
	indiv = [0 for i in xrange(npoints*2)]
	step = float(finish[0]-start[0])/(npoints+2)
	j=1
	for i in xrange(0,npoints*2,2):
		indiv[i] = start[0]+ j*step
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


def tournament(individuos, tsize):
	elements = random.sample(individuos, tsize)
	elements.sort(key=itemgetter(1)) # minimization
	
	return elements[0]


def roulette(individuos):
	sumfitness = 0.0
	for i in individuos:
		sumfitness += 1/i[1]
	
	probability = [0 for i in xrange(len(individuos))]
	sumprob = 0.0
	for i in xrange(len(individuos)):
		probability[i] = sumprob + ((1/individuos[i][1]) / sumfitness)
		sumprob += probability[i]
	
	for i in xrange(len(individuos)):
		if random.random() <= probability[i]:
			return individuos[i]	


def mutation(individuo):
	if seleccao==1:
		for i in xrange(1,len(individuo),2):
			if random.random() < pgene:
				individuo[i] = random.random()*start[1]
	else:
		pass
	return individuo

def recnpoints(individuo1, individuo2):
	size_i = len(individuo1[0])
	
	chosen = [0 for i in xrange(rec_points)]
	num = 0
	for i in xrange(rec_points):
		while num in chosen:
			num = random.randint(0, n_points-1)
		chosen[i] = num
	
	chosen.sort()
	
	prev = 0
	for i in xrange(0,rec_points,2):
		individuo1[0][prev:2*chosen[i]], individuo2[0][prev:2*chosen[i]] = individuo2[0][prev:2*chosen[i]], individuo1[0][prev:2*chosen[i]]
		prev = 2*chosen[i]
	
	if seleccao == 2:
		pass
	
	return [individuo1, individuo2]

def average(population):
	soma = 0.0
	for i in xrange(size_pop):
		soma += population[i][1]
	
	return soma/size_pop

def stdev(population):
	avg = average(population)
	soma = 0.0
	for i in population:
		soma += ((i[1]-avg)**2)
	
	stdev = math.sqrt(1/(size_pop-1.0)*soma)
	
	return stdev


def brachistochrone():
	# create initial population
	population = create_population(size_pop)
	
	# evaluate population
	population = [[indiv, fitness(start+indiv+finish)] for indiv in population]	
	population.sort(key=itemgetter(1))
	for generation in xrange(size_gen):
		parents = []
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
			offspring[i] = mutation(offspring[i])
		
		# evaluate offspring
		offspring2 = [[indiv[0], fitness(start+indiv[0]+finish)] for indiv in offspring]
		offspring2.sort(key=itemgetter(1))

		# select survivors
		population[size_pop-elite:] = offspring2[:elite]
		population.sort(key=itemgetter(1))
		FILE.write("Generation: "+str(generation+1)+"\n\n")
		FILE.write("Best: "+str(population[0][1])+" seconds\n")
		FILE.write("Worst: "+str(population[size_pop-1][1])+" seconds\n")
		FILE.write("Average: "+str(average(population))+" seconds\n")
		FILE.write("Standard Deviation: "+str(stdev(population))+" seconds\n")
		FILE.write("-"*30+"\n")
		
		print str(generation)+"\n"
		print population[0][0], population[0][1]
		print population[1][0], population[1][1]
		print population[2][0], population[2][1]
		
		points = []
		points.append([start[0]*50,start[1]*50])
		for i in xrange(0,len(population[0][0]),2):
			points.append([ population[0][0][i]*50, population[0][0][i+1]*50 ])
		points.append([finish[0]*50, finish[1]*50 ])
		#print points
		clear()
		pd()
		for i in xrange(0,len(points)):
			goto(points[i])
		pu()
		setpos(start[0]*50,start[1]*50)
		time.sleep(0.5)
	
	print "Best took %f seconds " %population[0][1]
	best.append(population[0][1])
	return True

"""
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
"""
winsize(1500,700,100,100)
pd()
setpos(start[0]*50,start[1]*50)
pu()
brachistochrone()
FILE.close()
