import getopt
import sys
import stats

flags = ['ds1=', 'ds2=', 'cf=', 'cl=', 'of1', 'of2', 'of=']

opts, args = getopt.getopt(sys.argv[1:], 'd', flags)

dataset1=dataset2=field=output=0
conf = 95

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

file1 = open(dataset1, 'r')
file2 = open(dataset2, 'r')

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

check1=check2=0
x=[]
y=[]

lineno=1
while 1 :
	temp=file1.readline()
	if not(temp) : break
	list1 = temp.strip().split(",")
	if pos1<len(list1) :
		x.append(list1[pos1])
	else: 
		print "WARNING: could not read field %i from line %i, it has only %i fields" %(pos1,lineno,len(list1)) 
	lineno+=1


print "Lista: "
print x

sum1 = sum(x)
sum2 = sum(y)

av1 = average(sum1, len(x))
av2 = average(sum2, len(y))

gm1 = gmean(x)
gm2 = gmean(y)

v1 = var(sum1, sqsum(x), len(x))
v2 = var(sum1, sqsum(y), len(y))

sd1 = stdev(v1)
sd2 = stdev(v2)

#c1 = conf(confidence, sd1, len(x))
#c2 = conf(confidence, sd2, len(y))

r = ratio(av1, av2)

d, r = diff(x, y)	

print "Data set 1: av:%i geomean:%i var:%i stdev:%i"  % (av1, gm1, v1, sd1)
print "Data set 2: av:%i geomean:%i var:%i stdev:%i"  % (av2, gm2, v2, sd2) 
