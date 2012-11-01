#! /usr/bin/env python

import matplotlib.pyplot as plt

# one-curve-per-revision-plot
def time_vs_config_plot(x, y, e, cpg, dout, file):


	n = len(x)
	print "n: ", n

	index=0
	index_max=cpg

	while index < n:
		while index < index_max:
			if index >= n:
				break
			print "index: ", index
			print "time: ", y[index]
			print "error: ",  e[index]
			plt.errorbar([0,2,4,8], y[index], e[index], label="r"+str(x[index]))
			index+=1
			
		print "index max: ", index_max
		print "plot!"
		plt.grid('on')
		plt.suptitle(file, fontsize=15)
		plt.xlabel('ntsm', fontsize=12)		
		plt.ylabel('t(s)', fontsize=12)		
		plt.legend(loc=4)
		plt.savefig(dout + file + ".png")
		#plt.show()
		index_max = index_max + cpg

	
	return
