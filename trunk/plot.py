#! /usr/bin/env python

import matplotlib.pyplot as plt

# one-curve-per-revision-plot
def time_vs_config_plot(x, y, e, cpg, l, dout, file):


	n = len(x)
	print "n: ", n

	i=1
	index=0
	index_max=cpg

	while index < n:
		while index < index_max:
			if index >= n:
				break
			#print "index: ", index
			print "time: ", y[index]
			print "error: ",  e[index]
			plt.errorbar([0,2,4,8], y[index], e[index], label=l+str(x[index]))
			index+=1
			
		#print "index max: ", index_max
		print "plot!"
		plt.grid('on')
		plt.margins(0.1, 0.1)
		plt.suptitle(file, fontsize=15)
		plt.xlabel('ntsm', fontsize=12)		
		plt.ylabel('t(s)', fontsize=12)		
		plt.legend(loc=4)
		#plt.savefig(dout + file + str(i) + ".png")
		#plt.close()
		plt.show()
		i = i + 1
		index_max = index_max + cpg

	
	return
