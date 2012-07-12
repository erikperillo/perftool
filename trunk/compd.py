import getopt
import sys
import stats

flags = ['ds1=', 'ds2=', 'cf=', 'cl=', 'of1', 'of2', 'of=']

opts, args = getopt.getopt(sys.argv[1:], 'd', flags)

dataset1=dataset2=field=output=0
confidence = 95 # 95 eh o valor default do intervalo de confianca

for p,v in opts:
        if p == '--ds1':
                dataset1 = v
        elif p == '--ds2':
                dataset2 = v
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

if not dataset1 or not dataset2:
	print "One or more data sets missing"
	sys.exit(1)
if not field:
	print "Field to be compared missing."
	sys.exit(2)
if not output:
	print "Output format missing."
	sys.exit(3)

try:
file1 = open(dataset1, 'r')
except IOError:
	print "WARNING: could not read file ", dataset1
	sys.exit(4)
try:
file2 = open(dataset2, 'r')
except IOError:
	print "WARNING: could not read file ", dataset2
	sys.exit(5)

temp1 = file1.readline().strip() 
temp2 = file2.readline().strip()

list1 = temp1.split(",")
list2 = temp2.split(",")

pos1=pos2=0

print "Comparing metric: (%s)" %(field)

for word in list1:
#	print "Comparing (%s) with (%s)" %(word,field)
	if word == field:
		print "File ds1: Found %s at column %i" %(field,pos1) 
		break
	pos1+=1

for word in list2:
	if word == field:
		print "File ds2: Found %s at column %i" %(field,pos2) 
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
#gmr = stats.ratio(gm1, gm2)

d, r = stats.diff(x, y)	

if output == 1:
	print "Data set 1: av:%f geomean:%f var:%f stdev:%f"  % (av1, gm1, v1, sd1)
	print "Data set 2: av:%f geomean:%f var:%f stdev:%f"  % (av2, gm2, v2, sd2)
	print "Ratio: average:%f geometric mean:%f" % (avr, gmr) 
	print "Diff: ",  d
	if not r:
		print "%i values were disregarded for one of the data sets being larger than the other"

elif output == 2:
	print "DATA SET 1"
	print "average: ", av1
#	print "geometric mean: ", gm1
	print "variance: ", v1
	print "standard deviation: ", sd1
	print "confidence interval: ", c1
	print "\nDATA SET 2"
	print "average: ", av2  
#       print "geometric mean: ", gm2
        print "variance: ", v2  
        print "standard deviation: ", sd2
        print "confidence interval: ", c2
	print "\nAverage ratio: ", avr
#	print "Geometric mean ratio: ", gmr
	print "Diff: ", d
	if not r:
		print "%i values were disregarded for one of the data sets being larger than the other"			

else:
	format = {'ds1-av':av1, 'ds1-ci':c1, 'ds1-std':sd1, 'ds1-var':v1, 'ds2-av':av2, 'ds2-ci':c2, 'ds2-std':sd2, 'ds2-var':v2, 'av-ratio':avr}
	output = output.replace(')', ')s')
	print output % format
	





