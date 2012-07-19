#!/usr/bin/env python

import sys
import stats
import getopt

def usage():
	print "Help on script compd"
	print "NAME"
	print "\tcompd"
	print "DESCRIPTION"
	print "\tThe compd script analyzes a determined feature of an application"
	print "ARGUMENTS"
	print "\t--ds1 file1name --ds2 file2name: The rdt files to be compared. The complete path is needed if the files are not in the same directory as the script"
	print "\t--ds filename: The rdt file to be analyzed. The complete path is needed if the file are not in the same directory as the script"
	print "\t--cf column: The feature to be anlyzed or/and compared. It corresponds to one of the columns of the rdt file(s). You must enter this argument."
	print "\t--cl number: The confidence level for the confidence interval. The values supported are 20%, 50%, 80%, 90%, 95%, 98%, 99%, 99.9%. In case no confidence level is set, the confidence interval will be calculated with a confidence value of 95%"
	print "\t--of1: Primary output format. There will be one line for each data set plus one line per each comparison result if there are two data sets. If no format is selected, the results will be displayed in this format."  
	print "\t--of2: Seconday output format. there will be a new line for each statistical result and comparison result if there are two data sets."
	print "\t--of string: User-defined output format. This format can be definded by a string one or more of the following:" 
	print "\t\t(ds1-av), (ds1-gm), (ds1-ci), (ds1-std), (ds1-var), (ds2-av), (ds2-gm), (ds2-ci), (ds2-std), (ds2-var), (av-ratio), (gm-ratio), (diff)"

flags = ['ds1=', 'ds2=', 'ds=', 'cf=', 'cl=', 'of1', 'of2', 'of=']

opts, args = getopt.getopt(sys.argv[1:], 'h', flags)

dataset1=dataset2=dataset=field=0
confidence = 95 # Default confidence level
output = 1 # Default output

for p,v in opts:
        if p == '--ds1':
                dataset1 = v
        elif p == '--ds2':
                dataset2 = v
        elif p == '--ds':
                dataset = v
        elif p == '--cf':
                field = v
        elif p == '--cl':
                confidence = v
        elif p == '--of1':
                output = 1
	elif p == '--of2':
		output = 2
	elif p == '--of':
		output = v
	elif h == '-h':
		usage();

if not field:
        print "Field to be analyzed missing."
        sys.exit(1)

if not dataset:
        if not dataset1 or not dataset2:
                print "One or more data sets missing."
                sys.exit(1)
	try:
        	file1 = open(dataset1, 'r')
	except IOError:
        	print "WARNING: could not read file ", dataset1
        	sys.exit(2)
	try:
        	file2 = open(dataset2, 'r')
	except IOError:
        	print "WARNING: could not read file ", dataset2
        	sys.exit(2)

	temp1 = file1.readline().strip() 
	temp2 = file2.readline().strip()

	list1 = temp1.split(",")
	list2 = temp2.split(",")

else
        if dataset1 or dataset2:
                print "Use either --ds or --ds1 and --ds2."
#                usage();
                sys.exit(1)
	try:
		file = open(dataset, 'r')
	except IOError:
		print "WARNING: could not read file", dataset
		sys.exit(2)

	temp = file.readline().strip()
	list = temp.split(',')

pos1=pos2=0	

#print "Comparing metric: (%s)" %(field)

for word in list1:
#	print "Comparing (%s) with (%s)" %(word,field)
	if word == field:
#		print "File ds1: Found %s at column %i" %(field,pos1) 
		break
	pos1+=1

for word in list2:
	if word == field:
#		print "File ds2: Found %s at column %i" %(field,pos2) 
		break
	pos2+=1

#check1=check2=0
x=[]
y=[]

lineno=1
while 1 :
	temp=file1.readline()
	if not(temp) : break
	list1 = temp.strip().split(",")
	if pos1<len(list1) :
		x.append(float(list1[pos1]))
	else: 
		print "WARNING: could not read field %i from line %i (ds1), it has only %i fields" %(pos1,lineno,len(list1)) 
	lineno+=1

lineno=1
while 1 :
	temp=file2.readline()
	if not(temp) : break
	list2 = temp.strip().split(",")
	if pos2<len(list2) :
		y.append(float(list2[pos2]))
	else: 
		print "WARNING: could not read field %i from line %i (ds2), it has only %i fields" %(pos2,lineno,len(list2)) 
	lineno+=1

file1.close()
file2.close()

# print "List 1: "
# print x
# print "List 2: "
# print y

sum1 = stats.sum(x)
sum2 = stats.sum(y)

av1 = stats.average(sum1, len(x))
av2 = stats.average(sum2, len(y))

# TODO: debug gmean
# done
#gm1 = gm2 = 0.0
gm1 = stats.gmean(x)
gm2 = stats.gmean(y)

v1 = stats.var(sum1, stats.sqsum(x), len(x))
v2 = stats.var(sum1, stats.sqsum(y), len(y))

# TODO: implement stdev
# already exists
#sd1 = sd2 = 0.0
sd1 = stats.stdv1(v1)
sd2 = stats.stdv1(v2)

# TODO: implement conf
# done
c1 = stats.conf(confidence, sd1, len(x))
c2 = stats.conf(confidence, sd2, len(y))

avr = stats.ratio(av1, av2)
gmr = stats.ratio(gm1, gm2)

d, r = stats.diff(x, y)	

if output == 1:
	print "Data set 1: av:%f geomean:%f var:%f stdev:%f conf:%f"  % (av1, gm1, v1, sd1, c1)
	print "Data set 2: av:%f geomean:%f var:%f stdev:%f conf:%f"  % (av2, gm2, v2, sd2, c2)
	print "Ratio: average:%f geometric mean:%f" % (avr, gmr) 
#	print "Diff: ",  d
#	if r:
#		print "%i values were disregarded for one of the data sets being larger than the other" %i

elif output == 2:
	print "DATA SET 1"
	print "average: ", av1
	print "geometric mean: ", gm1
	print "variance: ", v1
	print "standard deviation: ", sd1
	print "confidence interval: ", c1
	print "\nDATA SET 2"
	print "average: ", av2  
        print "geometric mean: ", gm2
        print "variance: ", v2  
        print "standard deviation: ", sd2
        print "confidence interval: ", c2
	print "\nAverage ratio: ", avr
	print "Geometric mean ratio: ", gmr
	print "Diff: ", d
	if r:
		print "%i values were disregarded for one of the data sets being larger than the other"	%i		

else:
	format = {'ds1-av':av1, 'ds1-gm':gm1, 'ds1-ci':c1, 'ds1-std':sd1, 'ds1-var':v1, 'ds2-av':av2, 'ds2-gm':gm2, 'ds2-ci':c2, 'ds2-std':sd2, 'ds2-var':v2, 'av-ratio':avr, 'gm-ratio':gmr, 'diff':d}
	output = output.replace('(', '%(')
	output = output.replace(')', ')s')
	print output % format
	





