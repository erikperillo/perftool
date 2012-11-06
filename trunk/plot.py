#! /usr/bin/env python

import matplotlib.pyplot as plt

# one-curve-per-revision-plot
def time_vs_config_plot(x, y, e, leg, cpg, l1, l2, dout, file):


	n = len(x)
	print "n: ", n

	index=0
	index_max=cpg

	while index < n:
		i=-1
		while index < index_max:
			if index >= n:
				break
			print "index: ", index
			print "time: ", len(y[index])
			print "error: ",  len(e[index])
			if l1 == 'r':
				i = index
			else:
				i = i + 1
				print "funfou!"
			print 'i: ', i
			print "leg: ", leg[i]
			plt.errorbar(x, y[index], e[index], label=l1+str(leg[i]))
			index+=1
			
		#print "index max: ", index_max
		plt.grid('on')
		plt.margins(0.2, 0.2)
		plt.suptitle(file, fontsize=15)
		plt.xlabel(l2, fontsize=12)		
		plt.ylabel('t(s)', fontsize=12)		
		plt.legend(loc=8, ncol=cpg, mode="expand")
		#plt.savefig(dout + file + str(i) + ".png")
		#plt.close()
		print "plot!"
		plt.show()
		index_max = index_max + cpg

	
	return
