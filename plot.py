#! /usr/bin/env python

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
def bars(y, yerror, file, title, xticks, ylabel):

	N = len(y)
	x = np.arange(N)	# the x locations for the bars
	width = 0.25		# width of the bars

	plt.bar(x, y, width, yerr=yerror, ecolor='r')	# plotting bar graph
	
	plt.ylabel(ylabel)		# add label to the y axis
	plt.xticks(x+width/2., xticks)	# add labels to the x ticks
	plt.margins(0.2,0)		# add horizontal margin	
	if title:			# if a title was parsed
		plt.title(title)	# add title to graph

	#plt.yticks(0,int(max(y+yerror))+1,10)	# set values to the y ticks
	
	#plt.savefig(file)		# save graph to file
	plt.show()
		
	return

# This function plots a line graph and save it to a file.
# ARGUMENTS
# y: list containing y coordinates for each point of the line
# yerror: list containing error values for y 
# file: file name for the graph file
# title: graph title 
# xticks: label for the x ticks
# ylabel: label for the y axis 
def lines(y, yerror, file, title, xticks, ylabel):

	N = len(y)
	x = np.arange(N)	# the x locations of the points
	margin = 0.2

	plt.errorbar(x, y, yerr=yerror, ecolor='r')	# plotting line graph

	plt.ylabel(ylabel)		# add label to the y axis
	plt.xticks(x, xticks)		# add labels to the x ticks
	plt.margins(margin,margin)		# add horizontal margin	
	if title:			# if a title was parsed
		plt.title(title)	# add title to graph

	#plt.savefig(file)		# save graph to file
	plt.show()

