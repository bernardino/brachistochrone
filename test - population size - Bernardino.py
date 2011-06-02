#!/usr/bin/env python
# encoding: utf-8

import random, math, sys, time, csv
from BrachFitness import calcBrachTime as fitness
from operator import itemgetter

from math import sin, cos, pi

size_gen = 300
size_pop = 200
n_points = 10
representacao = 1
elite = 20
pgene = 0.05
prec = 0.3
rec_points = 3
seleccao = 2
tsize = 20
start = [0, 5]
finish = [10,2]

def create_indiv(npoints):
	indiv = [0 for i in xrange(npoints*2)]
	step = float(finish[0]-start[0])/(npoints+1)
	deltaX = float(finish[0]-start[0])/2
	j=1
	for i in xrange(0,npoints*2,2):
		indiv[i] = start[0]+ j*step
		indiv[i+1] = random.uniform(finish[1]-deltaX/2, start[1]) # menor que o Y inicial
		j+=1
	return indiv



def create_indiv_2(npoints):
	indiv = [0 for i in xrange(npoints*2)]
	num = 0.0
	dist = float(finish[0]-start[0])
	x = [0.0 for i in xrange(npoints)]
	for i in xrange(npoints):
		while num in x:
			num = random.random()*dist
		x[i] = num
	
	x.sort()
	
	j=0
	for i in xrange(0,npoints*2,2):
		indiv[i+1] = random.uniform(finish[1]-dist/2, start[1]) # menor que o Y inicial
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
	#print id(individuos)
	elements = random.sample(individuos, tsize)[:]
	for i in xrange(tsize):
		elements[i] = elements[i][:]
	elements.sort(key=itemgetter(1)) # minimization
	aux = [[],0]
	aux[0].extend(elements[0][0])
	aux[1] = elements[0][1]
	return aux


def roulette(individuos, probability):
	for i in xrange(len(individuos)):
		if random.random() <= probability[i]:
			aux = [[],0]
			aux[0].extend(individuos[0][0])
			aux[1] = individuos[0][1]
			return aux


def mutation(individuo):
	dist = float(finish[0]-start[0])
	if representacao==1:
		for i in xrange(1,len(individuo[0]),2):
			if random.random() < pgene:
				individuo[0][i] = random.uniform(finish[1]-dist/2, start[1])
	else:
		prev = start[0]
		dif=0
		for i in xrange(0,len(individuo[0]),2):
			if random.random() < pgene:
				if i+2>=len(individuo[0])-1:
					dif = finish[0]-prev
				else:
					dif = individuo[0][i+2]-prev
				
				individuo[0][i] = prev+random.random()*dif/2+dif/5
				individuo[0][i+1] = random.uniform(finish[1]-dist/2, start[1])
			prev = individuo[0][i]
	
	return individuo[:]

def recnpoints(individuo1, individuo2):
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
		if i+1<len(chosen):
			prev = 2*chosen[i+1]
	
	if representacao == 2:
		points = [[0,0] for i in xrange(n_points)]
		points2 = [[0,0] for i in xrange(n_points)]
		j=0
		prev = 0
		prev2 = 0
		for i in xrange(0,n_points*2,2):
			points[j][0] = individuo1[0][i]
			points[j][1] = individuo1[0][i+1]
			points2[j][0] = individuo2[0][i]
			points2[j][1] = individuo2[0][i+1]
			
			if prev == points[j][0]:
				points[j][0] += 0.0000001
			if prev2 == points2[j][0]:
				points2[j][0] += 0.0000001
			
			prev = points[j][0]
			prev2 = points2[j][0]
			j += 1
		
		points.sort(key=itemgetter(0))
		points2.sort(key=itemgetter(0))
		
		j=0
		prev = 0
		prev2 = 0
		for i in xrange(0,n_points*2,2):
			individuo1[0][i] = points[j][0]
			individuo1[0][i+1] = points[j][1]
			individuo2[0][i] = points2[j][0]
			individuo2[0][i+1] = points2[j][1]
			if prev == points[j][0]:
				individuo1[0][i] += 0.0000001
			if prev2 == points2[j][0]:
				individuo2[0][i] += 0.0000001
			prev = individuo1[0][i]
			prev2 = individuo2[0][i]
			j += 1
	
	return [individuo1[:], individuo2[:]]

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

def brachistochroneReal(x0, y0, x1, y1, n):
	dy = y0 - y1
	prec=10.0**-12
	
	t1=0.0
	t2=2*pi
	
	xm=x0
	while abs(xm-x1) > prec:
		tm = (t1+t2)/2
		
		if (1-cos(tm)==0):
			continue
		
		rm = dy / (1 - cos(tm))
		xm = x0 + rm * (tm - sin(tm))
		
		if (xm > x1):
			#pag 258
			t2 = tm
		else:
			t1 = tm
	
	L = []
	L2 = []
	r=rm
	for i in xrange(n+1):
		t=tm*i/n
		L.append ( [(x0+r*(t-sin(t))), (y0-r*(1-cos(t)))] )
		L2.extend ( [(x0+r*(t-sin(t))), (y0-r*(1-cos(t)))] )
	
	return L, L2

def brachistochrone():
	# create initial population
	population = create_population(size_pop)
	
	# evaluate population
	population = [[indiv[:], fitness(start+indiv[:]+finish)] for indiv in population]	
	population.sort(key=itemgetter(1))
	for generation in xrange(size_gen):
		parents = []
		# select parents
		if seleccao==2: # tournament
			for i in xrange(size_pop):
				parents.extend([tournament(population[:],tsize)])
			parents = [tournament(population[:], tsize) for i in xrange(size_pop)]
		else: # roulette
			sumfitness = 0.0
			for i in population:
				sumfitness += 1/i[1]
			
			probability = [0 for i in xrange(size_pop)]
			sumprob = 0.0
			for i in xrange(size_pop):
				probability[i] = sumprob + float((1.0/population[i][1]) / sumfitness)
				sumprob += probability[i]
			parents = [roulette(population[:], probability) for i in xrange(size_pop)]
		
		# produce offspring
		offspring = []
		
		# crossover
		for i in xrange(0, size_pop,2):
			if random.random() < prec:
				offspring.extend(recnpoints(parents[i][:],parents[i+1][:]))
			else:
				offspring.extend([parents[i][:],parents[i+1][:]])
				
		# mutation
		for i in xrange(size_pop):
			offspring[i] = mutation(offspring[i][:])
		
		# evaluate offspring
		offspring2 = [[indiv[0][:], fitness(start+indiv[0][:]+finish)] for indiv in offspring]
		offspring2.sort(key=itemgetter(1))
		
		# select survivors
		for i in xrange(size_pop - elite):
			population[size_pop-i-1] = offspring2[i][:]
		
		population2 = [[indiv[0][:], fitness(start+indiv[0][:]+finish)] for indiv in population]
		population = sorted(population2[:], key=itemgetter(1))
		
		excelWriter.writerow(("Generation: ",str(generation+1), "Best: ",str(population[0][1]), "Worst: ", str(population[-1][1]), "Average: ", str(average(population)), "Desvio: ", str(stdev(population)) ))
		
		if not generation%10:
			print str(generation)+"\n"
	FILE.write("Best Curve in Repetition "+str(repetition+1)+":\n"+str(population[0])+"\n\n")
	return True

points, bestpoints = brachistochroneReal(start[0], start[1], finish[0], finish[1], n_points+2)
bestRealFitness = fitness(bestpoints)

if representacao:
	representacaoStr = "X fixos"
else:
	representacaoStr = "S/ X fixos"
if seleccao == 2:
	seleccaoStr = "Torneio"
else:
	seleccaoStr = "Roleta"

sizes_pop = [50,100,150,200,300,400,500]

for size_pop in sizes_pop:
	
	FILE = open("results-size_pop_"+str(size_pop)+"-best.txt",'w')
	filename = "results-size_pop_"+str(size_pop)+".csv"
	excelWriter = csv.writer(open(filename, 'wb'))
	excelWriter.writerow(('Melhor tempo real: ', str(bestRealFitness) ))
	FILE.write("Real Curve points:\n"+str(points)+"\nFitness: "+str(bestRealFitness)+"\n\n")
	
	for repetition in xrange(30):
		#alterar seed
		random.seed(random.randint(0,10000))
		
		excelWriter.writerow(("PARAMS"," "))
		excelWriter.writerow(('Start','Finish','Geracoes','NPopulacao','NPontos','Representacao','Tam Torneio','Elitismo','Selecao','P. Mutacao','P. Recombinacao','Pontos Rec.'))
		excelWriter.writerow((str(start[0])+" "+str(start[1]),str(finish[0])+" "+str(finish[1]), size_gen, size_pop, n_points, representacaoStr, tsize, elite, seleccaoStr, pgene, prec, rec_points))
		brachistochrone()
	
	FILE.close()

"""representacao = 2
for size_pop in sizes_pop:
	
	FILE = open("results-size_pop_"+str(size_pop)+"-best.txt",'w')
	filename = "results-size_pop_"+str(size_pop)+".csv"
	excelWriter = csv.writer(open(filename, 'wb'))
	excelWriter.writerow(('Melhor tempo real: ', str(bestRealFitness) ))
	FILE.write("Real Curve points:\n"+str(points)+"\nFitness: "+str(bestRealFitness)+"\n\n")
	
	for repetition in xrange(30):
		#alterar seed
		random.seed(random.randint(0,10000))
		
		excelWriter.writerow(("PARAMS"," "))
		excelWriter.writerow(('Start','Finish','Geracoes','NPopulacao','NPontos','Representacao','Tam Torneio','Elitismo','Selecao','P. Mutacao','P. Recombinacao','Pontos Rec.'))
		excelWriter.writerow((str(start[0])+" "+str(start[1]),str(finish[0])+" "+str(finish[1]), size_gen, size_pop, n_points, representacaoStr, tsize, elite, seleccaoStr, pgene, prec, rec_points))
		brachistochrone()
	
	FILE.close()"""
#FILE.close()
