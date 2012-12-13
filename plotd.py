#! /usr/bin/env python

import re
import sys
import plot
import getopt
import subprocess

# print the module info
def usage():
	sys.stderr.write("\nHelp on plotd tool\nNAME\n\tplotd\nDESCRIPTION\n\tPlotd generates bar or line graphs from given rdt files\n")
	sys.stderr.write("ARGUMENTS\n")
	sys.stderr.write("\t-o str: Name for the output file including extension. It must be entered.\n")
	sys.stderr.write("\t--df fieldname: Data field from rdt file to be plotted. It must be entered.\n")
	sys.stderr.write("\t--cf conf: Confidence level of confidence. If none is entered error bars will not be displayed.\n")
	sys.stderr.write("\t--title str: Graph title. If none is entered the graph will not have a title.\n")
	sys.stderr.write("\t--xlabel: Label to each bar or x value in the graph. If not entered filenames will be used.\n")
	sys.stderr.write("\t--ylabel: Label for the y axis. If not entered data field will be used.\n")
	sys.stderr.write("BAR PLOT\n")
	sys.stderr.write("\t--bar: selects bar plot\n")
	sys.stderr.write("\t--b{n} filename: The rdt file containing data for the nth bar of the graph.\n")
	sys.stderr.write("\t-b filenames: rdt file range. One bar will be plotted for each file.\n")
	sys.stderr.write("LINE PLOT\n")
	sys.stderr.write("\t--lines: selects line plot\n")
	sys.stderr.write("\t--l{n} filename: The rdt file containing data for the nth line of the graph\n")
	sys.stderr.write("\t--l{n}.{m} filename: The rdt file containig data for the mth point of the nth line of graph.\n")
	sys.stderr.write("\t-l filenames: rdt files range. One line will be plotted fo each file\n")

# print an error message and the module info
# exit if required
# mesage: string
# status: int
def fail(message, status=0):
        sys.stderr.write(message+'\n')
        usage()
        if status:
                sys.exit(status)

# print a warning message
# message: string
def warning(message):
	sys.stderr.write("WARNING: " + message + '\n')

def list(filename):
	list=[]
	cmd = "ls -1 " + filename
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	#a=p.stdout.readlines()
	#print a
	#sys.exit()
	while True:
		file = p.stdout.readline().strip()
		if len(file):
			list.append(file)
		else:
			break	# reached end of file						
	return list

def generate_data(files, df, c):
	av=[]
	error=[]
	if c:
		#print "cmd: ", cmd	
		for f in files:
			cmd = "/local/julia/perftool/compd.py --cf " + df + " --cl " + c + " --of '(ds-av) (ds-ci)' --ds " + f
			p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
			values = p.stdout.readline().strip().split(' ')
			#print values
			av.append(float(values[0]))
			error.append(float(values[1]))	
	else:
		for f in files:
			cmd = "/local/julia/perftool/compd.py --cf " + df + " --of '(ds-av)' --ds " + f
			
			#print "cmd: ", cmd	
			p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
			value = p.stdout.readline().strip()
			#print value
			av.append(float(value))
	
	return av, error
	

# ============
# Main
# ============

	
short_flags='o:b:l:h'
long_flags=['df=', 'cf=', 'title=', 'xlabel=', 'ylabel=', 'bar', 'lines', 'help']
extra_flags=['b1=', 'b2=', 'b3=', 'b4=', 'b5=', 'b6=', 'b7=', 'b8=', 'b9=', 'b10=', 'l1=', 'l2=', 'l3=', 'l4=', 'l5=', 'l6=', 'l7=', 'l8=', 'l9=', 'l10=']

opts, extra_args = getopt.getopt(sys.argv[1:], short_flags, long_flags+extra_flags)
	
output=field=conf=title=xlabel=ylabel=plot_type=0
input=[]
	
for f,v in opts:

	if f == '-o':
		output = v

	elif f == '-b' or f == '-l':
		input = list(v)

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

	elif f == '--bar':
		plot_type = 'b'
	
	elif f == '--lines':	
		plot_type = 'l'

	elif re.match(r'--b\d', f) != None:
		input.append(v)

	elif re.match(r'--l\d', f) != None:
		if re.search(r'\*', v) == None:
			input.append(v)
 		else:
			temp = list(v)
			input.append(temp)

print input
sys.exit()		

	
if not plot_type:
	fail("A plot type must be chosen.", 1)

if not field:
	fail("A data field must be entered.", 1)

if not output:
	fail("A name is required for the output file.", 1)

if not len(input):
	fail("Input files must be entered.", 1)
	
ylist,error = generate_data(input, field, conf)

if not conf:
	warning("no value entered for the confidence level. Erros bars will not be displayed.")
	error=None
	
if not title:
	warning("no title entered. None will be displayed.")

if not xlabel:
	warning("no label for x values. File names will be used.")
	xlabel=input
else:
	xlabel=xlabel.split(' ')

if not ylabel:
	warning("no label for the y axis. Data field will be used.")	
	ylabel = field
	
if plot_type == 'b':
	plot.bars(ylist, error, output, title, xlabel, ylabel)
else:
	plot.lines(ylist, error, output, title, xlabel, ylabel)

