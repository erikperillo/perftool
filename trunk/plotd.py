#! /usr/bin/env python

import re
import sys
import plot
import getopt
import subprocess

# prints the module info
def usage():
	sys.stderr.write("\nHelp on plotd tool\nNAME\n\tplotd\nDESCRIPTION\n\tPlotd generates bar or line graph from given rdt files\n")
	sys.stderr.write("ARGUMENTS\n")
	sys.stderr.write("\t-o str: Name for the output file including extension. It must be entered.\n")
	sys.stderr.write("\t--df fieldname: Data field from rdt file to be plotted. It must be entered.\n")
	sys.stderr.write("\t--cf conf: Confidence level of confidence. If none is entered error bars will not be displayed.\n")
	sys.stderr.write("\t--title str: Graph title. If none is entered the graph will not have a title.\n")
	sys.stderr.write("\t--xlabel \"str1,str2,...,strn\": Label to each bar or dot in the graph. If not entered filenames will be used.\n")
	sys.stderr.write("\t--ylabel str: Label for the y axis. If not entered data field will be used.\n")
	sys.stderr.write("BAR PLOT\n")
	sys.stderr.write("\t-B \"filename\": rdt file range. One bar will be plotted for each file.\n")
	sys.stderr.write("\t-b \"n filename\": The rdt file containing data for the nth bar of the graph.\n")
	sys.stderr.write("LINE PLOT\n")
	sys.stderr.write("\t-L \"filename\": rdt files range. A single line will be plotted.\n")
	sys.stderr.write("\t-l \"n filename\": The rdt file range containing data for the nth line of the graph\n")
	sys.stderr.write("\t--lp \"n m filename\": The rdt file containig data for the mth point of the nth line of graph.\n")
	sys.stderr.write("\t--lines \"str1,str2,...,strn\": Label to each line in a multiple line plot. If not entered, default labels will be used(l1,l2,...,ln).\n")

# prints an error message and the module info
# exits if required
# message: string
# status: int
def fail(message, status=0):
        sys.stderr.write("ERROR: " + message+'\n')
        usage()
        if status:
                sys.exit(status)

# prints a warning message and returns
# message: string
def warning(message):
	sys.stderr.write("WARNING: " + message + '\n')

# cuts off the filename of complete path
# paths: list of strings
# returns a list of strings
def get_fname(paths):
	flist=[]	
	for path in paths:	
		fname = path.split('/')
		pos = len(fname) - 1
		flist.append(fname[pos])
	return flist

# executes the ls command 
# filename: string
# returns a list of strings
def list_files(filename):
	list=[]
	cmd = "ls -1 " + filename
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	while True:
		file = p.stdout.readline().strip()
		if len(file):
			list.append(file)
		else:
			break	# reached end of file						
	return list

# executes the compd tool 
# files: list of strings
# df: string
# c: string
# returns a list containing averages and another containing errors, if c is given
def generate_data(files, df, c):

	av=[]
	error=[]

	if c:
		for f in files:
			cmd = "/local/julia/perftool/compd.py --cf " + df + " --cl " + c + " --of '(ds-av) (ds-ci)' --ds " + f
			p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
			values = p.stdout.readline().strip().split(' ')
			av.append(float(values[0]))
			error.append(float(values[1]))	
	else:
		for f in files:
			cmd = "/local/julia/perftool/compd.py --cf " + df + " --of '(ds-av)' --ds " + f
			p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
			value = p.stdout.readline().strip()
			av.append(float(value))
		error=None
		
	return av, error

# makes a list out of a dictionary
# dict: dictionary containing the input files
# returns a list
def dict_to_list(dict):
	d={}
	l=[]
	temp=-1
	for key in dict:
		if type(key) is int:
			d[key]=dict[key]
		else:
			if temp == key[0]:
				l.append(dict[key])
			else:
				if len(l):
					d[temp]=l
					del l[:]
				temp=key[0]
			
	list = d.values()		
	return list	


# ============
# Main
# ============

short_flags='B:b:L:l:o:h'
long_flags=['lp=', 'df=', 'cf=', 'title=', 'xlabel=', 'ylabel=', 'help']

opts, extra_args = getopt.getopt(sys.argv[1:], short_flags, long_flags)

output=field=conf=title=xlabel=ylabel=plot_type=legend=0
input=[]
input2={}
	
for f,v in opts:

	if f == '-o':
		output = v

	elif f == '-h':
		usage()
		sys.exit()

	elif f == '--df':
		field = v

	elif f == '--cf': 
		conf = v

	elif f == '--title':
		title = v
		
	elif f == '--xlabel':
		xlabel = v

	elif f == '--ylabel':
		ylabel = v

	elif f == '--lines':
		legend = v.split(',')

	elif f == '-B':
		if plot_type == 'L' or plot_type == 'l':
			fail("Cannot mix plot types.", 1)
		else:
			plot_type='b'
		input = list_files(v)

	elif f == '-L':
		if plot_type == 'b':
			fail("Cannot mix plot types.", 1)
		else:
			plot_type='l'
		input = list_files(v)

	elif f == '-b':
		if plot_type == 'L' or plot_type == 'l':
			fail("Cannot mix plot types.", 1)
		else:
			plot_type='b'
		temp=v.split(' ')
		input2[int(temp[0])]=temp[1]

	elif f == '-l':
		if plot_type == 'b':
			fail("Cannot mix plot types.", 1)
		else:
			plot_type='L'
		temp=v.split(' ')
		input2[int(temp[0])]=list_files(temp[1])

	elif f == '--lp':
		if plot_type == 'b':
			fail("Cannot mix plot types.", 1)
		else:
			plot_type='L'
		temp=v.split(' ')
		input2[(int(temp[0]),int(temp[1]))]=temp[2]


if not plot_type:
	fail("Input file(s) must be entered.", 1)

if not field:
	fail("A data field must be entered.", 1)

if not output:
	fail("A name is required for the output file.", 1)

if not conf:
	warning("no value entered for the confidence level. Erros bars will not be displayed.")
	error=None
	
if not title:
	warning("no title entered. None will be displayed.")

if not xlabel:
	warning("no label for x values. File names will be used.")
	xlabel=get_fname(input)
else:
	xlabel=xlabel.split(',')

if not ylabel:
	warning("no label for the y axis. Data field will be used.")	
	ylabel = field
	
if plot_type == 'b':
	if len(input2):
		input=input2.values()
	ylist,error = generate_data(input, field, conf)
	plot.bars(ylist, error, output, title, xlabel, ylabel)

elif plot_type == 'l':
	ylist,error = generate_data(input, field, conf)
	plot.line(ylist, error, output, title, xlabel, ylabel)

else:
	if not legend:
		warning("labels for lines not entered. Default labels will be used.")
	input=dict_to_list(input2)
	ylist = error = []
	for list in input:
		av,e = generate_data(list, field, conf)
		ylist.append(av)
		error.append(e)
	plot.lines(ylist, error, output, title, ylabel, legend)
