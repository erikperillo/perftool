#! /usr/bin/env python

import re
import sys
import plot
import getopt
import shutil
import os.path
import subprocess
#import pdb; pdb.set_trace()
from collections import namedtuple

bar = namedtuple("bar", ["b","file"])
line = namedtuple("line", ["l","files"])
point = namedtuple("point", ["l","p","file"])

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
			cmd = "/local/julia/perftool/compd.py --cf " + df + " --cl " + str(c) + " --of '(ds-av) (ds-ci)' --ds " + f
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

# generates report file
# xvalues: list containing labels for x ticks
# yvalues: list containing y values
# yerror: list containig y error values
# filenme: string for the name of tha graph file
def gen_report(xvalues, yvalues, yerror, filename):
	DIR="/local/julia/performance_regression/perf_data/report/warning/"

	ymax=[(x+y) for x, y in zip(yvalues, yerror)]
	ymin=[(x-y) for x, y in zip(yvalues, yerror)]

	filename1=filename.rstrip('.png') + '.poi' 
	filename2=filename.rstrip('.png') + '.all' 

	pos=1
	while pos < len(ymax):
		if ymax[pos-1] < ymin[pos]:
			# report
			avincrease=(yvalues[pos]-yvalues[pos-1])*(100/yvalues[pos-1])
			minincrease=(ymin[pos]-ymax[pos-1])*(100/ymin[pos])		
			
			fileobj=open(filename1, 'a')
			reportstr = str(xvalues[pos-1]) + "," + str(yvalues[pos-1]) + "+-" + str(yerror[pos-1]) + "s," + str(xvalues[pos]) + "," + str(yvalues[pos]) + "+-" + str(yerror[pos]) + "s," + str(avincrease) + "%," + str(minincrease) + "%\n"
			print reportstr	
			fileobj.write(reportstr)
			fileobj.close()
		pos=pos+1
	
	fileobj=open(filename2, 'a')
	for i in range(len(xvalues)):
		reportstr = str(xvalues[i]) + ',' + str(yvalues[i]) + ',' + str(yerror[i]) + ',' + str(ymin[i]) + ',' + str(ymax[i]) + '\n'
		fileobj.write(reportstr)
 	fileobj.close()

# checar existencia do arquivo no diretorio de destino
	if os.path.exists(filename1) and not(os.path.exists(DIR+filename1)):
		shutil.move(filename1, DIR)
	if os.path.exists(filename2) and not(os.path.exists(DIR+filename1)):
		shutil.move(filename2, DIR)

	return


# ============
# Main
# ============

short_flags='B:b:L:l:o:h'
long_flags=['lp=', 'df=', 'cf=', 'title=', 'xlabel=', 'ylabel=', 'help']

opts, extra_args = getopt.getopt(sys.argv[1:], short_flags, long_flags)

output=field=conf=title=xlabel=ylabel=plot_type=legend=0
input=[]
	
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
		if plot_type == 'L' or plot_type == 'l' or plot_type == 'lp' or plot_type == 'b':
			fail("Cannot mix these plot types.", 1)
		plot_type='B'
		input = list_files(v)

	elif f == '-L':
		if plot_type == 'b' or plot_type == 'B' or plot_type == 'l' or plot_type == 'lp':
			fail("Cannot mix these plot types.", 1)
		plot_type='L'
		input = list_files(v)

	elif f == '-b':
		if plot_type == 'L' or plot_type == 'l' or plot_type == 'lp' or plot_type == 'B':
			fail("Cannot mix these plot types.", 1)
		plot_type='b'
		temp=v.split(' ')
		input.append(bar(b=int(temp[0]), file=temp[1]))

	elif f == '-l':
		if plot_type == 'b' or plot_type == 'B' or plot_type == 'L':
			fail("Cannot mix these plot types.", 1)
		plot_type='l'
		temp=v.split(' ')
		input.append(line(l=int(temp[0]), files=list_files(temp[1])))

	elif f == '--lp':
		if plot_type == 'b' or plot_type == 'B' or plot_type == 'L':
			fail("Cannot mix these plot types.", 1)
		plot_type='lp'
		temp=v.split(' ')
		input.append(point(l=int(temp[0]), p=int(temp[1]), file=temp[2]))


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
	if len(input):
		xlabel=get_fname(input)
else:
	xlabel=xlabel.split(',')

if not ylabel:
	warning("no label for the y axis. Data field will be used.")	
	ylabel = field


if plot_type == 'b' or plot_type == 'B':
	if plot_type == 'b':
		input.sort(key=lambda x:x.b)
		input = [bar.file for bar in input]
	ylist,error = generate_data(input, field, conf)
	plot.bars(ylist, error, output, title, xlabel, ylabel)

elif plot_type == 'L':
	ylist,error = generate_data(input, field, conf)
	plot.line(ylist, error, output, title, xlabel, ylabel)

elif plot_type == 'l' or plot_type == 'lp':
	
	ylist = []
	error = []
	aux = []
	flist = []

	input.sort(key=lambda x:x.l)

	if plot_type == 'l':
		i=1
		while True:
			aux = [line.files for line in input if line.l==i]
			if not len(aux):
				break
			flist.append(aux)
			i=i+1	
	elif plot_type == 'lp':
		i=1
		while True:
			aux = [point for point in input if point.l==i]
			if not len(aux):
				break
			aux.sort(key=lambda x:x.p)
			aux = [point.file for point in aux]
			flist.append(aux)
			i=i+1
	for l in flist:
		av,e = generate_data(l, field, conf)
		ylist.append(av)
		error.append(e)
		
		#	ylist,error=generate_data(input, field, conf)
		#	plot.line(ylist, error, output, title, xlabel, ylabel)
	#elif plot_type == 'lp':
	if not legend:
		warning("labels for lines not entered. Default labels will be used.")
	
	if len(ylist) == 1:
		plot.line(ylist[0], error[0], output, title, xlabel, ylabel)
	elif len(ylist) > 1:
		plot.lines(ylist, error, output, title, ylabel, legend)

else:
	fail(plot_type+"is not a valid plot type", 1)

#verificar se grafico foi gerado

if conf: 
	gen_report(xlabel, ylist[0], error[0], output)
