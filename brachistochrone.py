#!/usr/bin/env python
# encoding: utf-8

import random, math, sys, time, csv
from BrachFitness import calcBrachTime as fitness
from operator import itemgetter
from xturtle import *
from Tkinter import *

spamWriter = csv.writer(open('results.csv', 'wb'))
#spamWriter.writerow(('Title 1','Title 1','Title 1'))
#spamWriter.writerow(['Spam Spam', 'Lovely Spam', 'Wonderful Spam'])

FILE = open("results.txt",'w')
outputxt = open("output.txt",'w')
best = []
size_gen = 300
size_pop = 500
n_points = 8
representacao = 1
elite = 10
pgene = 0.01
prec = 0.5
rec_points = 3
seleccao = 2
tsize = 20
start = [1, 5]
finish = [10,2]

canvasWidth = 580
canvasHeight = 290

"""size_gen = input("Numero de geraçoes: ")
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
		break"""

def create_indiv(npoints):
	indiv = [0 for i in xrange(npoints*2)]
	step = float(finish[0]-start[0])/(npoints+2)
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


def brachistochrone( rTurtle):
	# create initial population
	population = create_population(size_pop)
	
	# evaluate population
	population = [[indiv[:], fitness(start+indiv[:]+finish)] for indiv in population]	
	population.sort(key=itemgetter(1))
	for generation in xrange(size_gen):
		parents = []
		# select parents
		if seleccao==2: # tournament
			parents = [tournament(population[:], tsize) for i in xrange(size_pop)]
		else: # roulette
			sumfitness = 0.0
			for i in population:
				sumfitness += 1/i[1]
			
			probability = [0 for i in xrange(size_pop)]
			sumprob = 0.0
			for i in xrange(size_pop):
				probability[i] = sumprob + ((1/population[i][1]) / sumfitness)
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
		for i in xrange(elite):
			population[size_pop-i-1] = offspring2[i][:]
		#population[size_pop-elite:] = offspring2[:elite]
		population2 = [[indiv[0][:], fitness(start+indiv[0][:]+finish)] for indiv in population]
		population = sorted(population2[:], key=itemgetter(1))
		#print population[0][0]
		#print 'fitness %lf'%(population[0][1])
		FILE.write("Generation: "+str(generation+1)+"\n\n")
		FILE.write("Best: "+str(population[0][1])+" seconds\n")
		FILE.write("Worst: "+str(population[-1][1])+" seconds\n")
		FILE.write("Average: "+str(average(population))+" seconds\n")
		FILE.write("Standard Deviation: "+str(stdev(population))+" seconds\n")
		FILE.write("-"*30+"\n")
		
		
		print str(generation)+"\n"
		
		
	points = []
	
	xScale = canvasWidth/(finish[0] - start[0])
	yScale = canvasHeight/(start[1] - finish[1])
	
	for i in xrange(0,len(population[0][0]),2):
		points.append([population[0][0][i]*xScale-(canvasWidth/2)-start[0]*xScale , population[0][0][i+1]*yScale-(canvasHeight/2)-finish[1]*yScale +50])
	points.append([finish[0]*xScale-(canvasWidth/2)-start[0]*xScale, finish[1]*yScale-(canvasHeight/2)-finish[1]*yScale + 50])

	
	drawCurve(rTurtle, points,xScale, yScale)
	
	print "Best took %f seconds " %population[0][1]
	best.append(population[0][1])
	return True

def drawCurve( rTurtle, points, xScale, yScale):
	#print points
	#rTurtle.clear()
	#rTurtle.pu()
	#rTurtle.setpos(start[0]*xScale-(canvasWidth/2)-start[0]*xScale, start[1] *yScale-(canvasHeight/2)-finish[1]*yScale)
	#rTurtle.pd();
	#rTurtle.goto(finish[0]*xScale-(canvasWidth/2)-start[0]*xScale, finish[1]*yScale-(canvasHeight/2)-finish[1]*yScale)
	
	rTurtle.clear()
	rTurtle.pu()
	rTurtle.setpos(start[0]*xScale-(canvasWidth/2)-start[0]*xScale, start[1] *yScale-(canvasHeight/2)-finish[1]*yScale+50)
	rTurtle.pd()
	for i in xrange(0,len(points)):
		rTurtle.goto(points[i])
	rTurtle.pu()
	rTurtle.setpos(start[0]*xScale-(canvasWidth/2)-start[0]*xScale, start[1] *yScale-(canvasHeight/2)-finish[1]*yScale+50)


class App:

	def start(self):
		self.startButton.configure(state=DISABLED)
		global size_gen, size_pop, n_points, representacao, elite, pgene, prec, rec_points, seleccao, tsize, start, finish
		rt = RawTurtle(self.canvas)
		self.canvas.delete(ALL)
		try:
			size_gen = int(self.gen.get())
			size_pop = int(self.pop.get())
			n_points = int(self.points.get())
			representacao = self.representation.get()
			elite = int(self.elitism.get())
			pgene = float(self.mutation.get())
			prec = float(self.recombination.get())
			rec_points = int(self.recombinationPoints.get())
			seleccao = self.sel.get()
			tsize = int(self.tournamentSize.get())
			start[0] = float(self.startPointX.get())
			start[1] = float(self.startPointY.get())
			finish[0] = float(self.finishPointX.get())
			finish[1] = float(self.finishPointY.get())
			random.seed(random.randint(0,10000))
			brachistochrone(rt)
			self.startButton.configure(state=NORMAL)
		except ValueError:
			self.startButton.configure(state=NORMAL)
			print "Incorrect values, please check your parameters"
		
		
		
		
	def __init__(self, root):
		frame = Frame(root, width=800, height=600)
		frame.pack()
		root.geometry("800x600+100+100")

		self.button = Button(frame, text="Quit", command=frame.quit)
		self.button.place(w=80,h=30,x=100,y=10)
		self.startButton = Button(frame, text="Start", command=self.start)
		self.startButton.place(w=80,h=30,x=10,y=10)

		self.genLabel = Label(frame, text="Generations:")
		self.genLabel.place(w=100,h=30,x=55,y=50)

		self.gen = StringVar()
		self.genEntry = Entry(frame,width=20, textvariable = self.gen)
		self.genEntry.place(w=40,h=25,x=140,y=50)
		self.gen.set("300")       


		self.popLabel = Label(frame, text="Population:")
		self.popLabel.place(w=100,h=30,x=55,y=80)

		self.pop = StringVar()
		self.popEntry = Entry(frame,width=20, textvariable = self.pop)
		self.popEntry.place(w=40,h=25,x=140,y=80)
		self.pop.set("500")

		self.pointLabel = Label(frame, text="Points:")
		self.pointLabel.place(w=100,h=30,x=65,y=110)

		self.points = StringVar()
		self.pointEntry = Entry(frame,width=20, textvariable = self.points)
		self.pointEntry.place(w=40,h=25,x=140,y=110)
		self.points.set("8")


		self.elitismLabel = Label(frame, text="Elitism:")
		self.elitismLabel.place(w=100,h=30,x=65,y=140)

		self.elitism = StringVar()
		self.elitism.set("10")
		self.elitismEntry = Entry(frame,width = 20, textvariable = self.elitism)
		self.elitismEntry.place(w=40,h=25,x=140,y=140)

		self.mutationLabel = Label(frame, text ="% of Mutation:")
		self.mutationLabel.place(w=150,h=30,x=20,y=170)

		self.mutation = StringVar()
		self.mutation.set("0.01")

		self.mutationEntry = Entry(frame,width=20, textvariable = self.mutation)
		self.mutationEntry.place(w=40,h=25,x=140,y=170)

		self.recombinationLabel = Label(frame, text ="% of Recombination:")
		self.recombinationLabel.place(w=120,h=30,x=20,y=200)

		self.recombination = StringVar()
		self.recombination.set("0.5")

		self.recombinationEntry = Entry(frame,width=20, textvariable = self.recombination)
		self.recombinationEntry.place(w=40,h=25,x=140,y=200)

		self.recombinationPointsLabel = Label(frame, text ="Points of Recombination:")
		self.recombinationPointsLabel.place(w=140,h=30,x=0,y=230)

		self.recombinationPoints = StringVar()
		self.recombinationPoints.set("3")

		self.recombinationPointsEntry = Entry(frame,width=20, textvariable = self.recombinationPoints)
		self.recombinationPointsEntry.place(w=40,h=25,x=140,y=230)


		self.startPointLabel = Label(frame, text = "Start Point")
		self.startPointLabel.place(w=100,h=30,x=0,y=260)

		self.startPointXLabel = Label(frame, text = "x:")
		self.startPointXLabel.place(w=20,h=30,x=40,y= 280)

		self.startPointX = StringVar()
		self.startPointX.set("1")
		self.startPointXEntry = Entry(frame,width=20, textvariable = self.startPointX)
		self.startPointXEntry.place(w= 30, h=20, x=60, y=285)

		self.startPointYLabel = Label(frame, text = "y:")
		self.startPointYLabel.place(w=20,h=30,x=90,y= 280)

		self.startPointY = StringVar()
		self.startPointY.set("5")
		self.startPointYEntry = Entry(frame,width=20, textvariable = self.startPointY)
		self.startPointYEntry.place(w= 30, h=20, x=110, y=285)

		self.finishPointLabel = Label(frame, text = "End Point")
		self.finishPointLabel.place(w=100,h=30,x=0,y=310)

		self.finishPointXLabel = Label(frame, text = "x:")
		self.finishPointXLabel.place(w=20,h=30,x=40,y= 330)

		self.finishPointX = StringVar()
		self.finishPointX.set("10")
		self.finishPointXEntry = Entry(frame,width=20, textvariable = self.finishPointX)
		self.finishPointXEntry.place(w= 30, h=20, x=60, y=335)

		self.finishPointYLabel = Label(frame, text = "y:")
		self.finishPointYLabel.place(w=20,h=30,x=90,y= 330)

		self.finishPointY = StringVar()
		self.finishPointY.set("2")
		self.finishPointYEntry = Entry(frame,width=20, textvariable = self.finishPointY)
		self.finishPointYEntry.place(w= 30, h=20, x=110, y=335)


		self.representationLabel = Label(frame, text="Representation:")
		self.representationLabel.place(w=120,h=30,x=0,y=350)

		representation = [("Defined points",1), ("Random points",2)]
		self.representation = IntVar()
		for name,value in representation:
			Radiobutton(frame,text = name, variable = self.representation, value = value, indicatoron = 0).place(w=100,h=20,x=40,y=380+25*(value-1))
		self.representation.set(1)

		self.selectionLabel = Label(frame, text="Selection:")
		self.selectionLabel.place(w=100,h=30,x=0,y=440)

		selection = [ ("Tournament", 2), ("Roulette",1)]
		self.sel = IntVar()
		for name,value in selection:
			Radiobutton(frame, text=name, variable=self.sel, value=value, indicatoron=0).place(w=100,h=20,x=40, y=470+25*(value-1))
		self.sel.set(2)
		
		self.tournamentSize = StringVar()
		self.tournamentSize.set("20")
		self.tsizeLabel = Label(frame, text="Tournament Size:")
		self.tsizeLabel.place(w=140, h=30, x = 20,y = 530)
		
		self.tsizeEntry = Entry (frame, width = 20, textvariable = self.tournamentSize)
		self.tsizeEntry.place(w=40, h=25,x=140,y=530)
			 
		self.canvas = Canvas(root,width=canvasWidth+30,height=canvasHeight+150,bg="white")
		self.canvas.place(w=canvasWidth+30,h=canvasHeight+150,x=200,y=10)	
		
		
	
root = Tk()
root.title("Brachistochrone")
app = App(root)
root.mainloop()

#brachistochrone()
#FILE.close()
