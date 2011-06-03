import csv,sys,numpy
import matplotlib, pylab

rows = [0 for i in xrange(9091)]
sizes_pop = [50,100,150,200,300,400,500]
output = csv.writer(open('results_pop.csv','wb'))

for size_pop in sizes_pop:
	data = csv.reader(open("results-size_pop_"+str(size_pop)+".csv", 'rb'))
	
	i=0
	for row in data:
		rows[i] = row
		i += 1
	gens = [[0.0,0.0,0.0,0.0] for i in xrange(300)] #best worst avg stddev

	i=4
	j=4
	for gen in xrange(300): #geracoes
		for rep in xrange(30): #repeticoes
			gens[gen][0] += float(rows[j][3])
			gens[gen][1] += float(rows[j][5])
			gens[gen][2] += float(rows[j][7])
			gens[gen][3] += float(rows[j][9])
			j += 303
		i += 1
		j=i

	for i in xrange(300):
		gens[i][0] /= 30.0
		gens[i][1] /= 30.0
		gens[i][2] /= 30.0
		gens[i][3] /= 30.0

	for row in gens:
		output.writerow(row)

	points_best = [0 for i in xrange(300)]
	points_worst = [0 for i in xrange(300)]
	points_avg = [0 for i in xrange(300)]
	points_stdev = [0 for i in xrange(300)]
	i=0
	for p in gens:
		points_best[i] = p[0]
		points_worst[i] = p[1]
		points_avg[i] = p[2]
		points_stdev[i] = p[3]
		i+=1
	
	pylab.subplot(221)
	pylab.plot(points_best, label=str(size_pop))
	pylab.title("BEST")
	pylab.legend(bbox_to_anchor=(1.05, 1), loc=0, borderaxespad=0.)
	pylab.subplot(222)
	pylab.plot(points_worst, label=str(size_pop))
	pylab.title("WORST")
	pylab.legend(bbox_to_anchor=(1.05, 1), loc=0, borderaxespad=0.)
	pylab.subplot(223)
	pylab.plot(points_avg, label=str(size_pop))
	pylab.title("AVG")
	pylab.legend(bbox_to_anchor=(1.05, 1), loc=0, borderaxespad=0.)
	pylab.subplot(224)
	pylab.plot(points_stdev, label=str(size_pop))
	pylab.title("STD DEV")
	pylab.legend(bbox_to_anchor=(1.05, 1), loc=0, borderaxespad=0.)
	
pylab.savefig("graficos.png")