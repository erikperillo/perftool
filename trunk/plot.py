import math
import numpy as np
import matplotlib.pyplot as plt

# This function plots a bar graph and save it to a file.
# ARGUMENTS
# y: list containing the height of the bars
# yerror: list containing error value for y 
# file: file name for the graph file
# title: graph title 
# xticks: label for the x ticks
# ylabel: label for the y axis  
def bars(y, yerror=None, file=0, title=0, xticks=0, ylabel=0, display=0):

	N = len(y)
	x = np.arange(N)	# the x locations for the bars
	width = 0.25		# width of the bars
	xmargin = 0.2		# horizontal margin to graph

	plt.bar(x, y, width, yerr=yerror, ecolor='r')	# plotting bar graph
	
	plt.margins(xmargin,0)		# add horizontal margin
	if ylabel:	
		plt.ylabel(ylabel)	# add label to the y axis
	if xticks:
		# add labels to the x ticks
		plt.xticks(x+width/2., xticks, size=5, weight='black',  stretch='ultra-condensed', rotation=-20, ha='left')	
	if title:			
		plt.title(title)	# add title to graph

	if yerror == None:
		ub = y
	else:
		ub=[]	
		for a,b in zip(y,yerror):
			ub.append(a+b)

	ymax = max(ub)
	#print ymax
	e = math.log(ymax,10)
	#print e
	if e < 1:
		ticks = 1
	else:
		ticks = 10**int(e)
	#print ticks
	ymax = (((ymax/ticks)+1)*ticks)+1
	plt.yticks(np.arange(0,ymax,ticks))# set values to the y ticks
	
	if not(display) and file:
		plt.savefig(file, bbox_inches='tight')	# save graph to file
	else:
		plt.show()		# display graph 

	return

# This function plots a line graph and save it to a file.
# ARGUMENTS
# y: list containing y coordinates for each point of the line
# yerror: list containing error values for y 
# file: file name for the graph file
# title: graph title 
# xticks: label for the x ticks
# ylabel: label for the y axis 
def lines(y, yerror=None, file=0, title=0, xticks=0, ylabel=0, display=0):

	N = len(y)
	x = np.arange(N)	# the x locations of the points
	margin = 0.2		# margin to graph

	plt.errorbar(x, y, yerr=yerror, ecolor='r')	# plotting line graph

	plt.margins(margin,margin)	# add margins to graph	
	if ylabel:
		plt.ylabel(ylabel)	# add label to the y axis
	if xticks:
		plt.xticks(x, xticks)	# add labels to the x ticks
	if title:			
		plt.title(title)	# add title to graph

	if not(display) and file:
		plt.savefig(file)	# save graph to file
	else:
		plt.show()		# display graph 

	return
