# this a module with statistics functions

import math
import re
import sys

def sum(x):
	s=0
        for n in x:
                s+=n
        return s

def sqsum(x):
	s2=0
#	print 'x:', x
	for n in x:
#		print "n:", n
		s2+=pow(float(n),2.0)
#		print "s2:", s2
#	print s2
	return s2

def prod(x):
	p=1
        for val in x:
                p *= val
#		print "=====",p
#	print "----------------->",p
	return p	

def nroot(val, n):
	return float(pow(val, 1/float(n)))
	
def average(ssum, ssize):
	return float(ssum)/float(ssize)

def gmean(x):
	n=len(x)
	y=[]
#	print n
	for val in x:
		y.append(nroot(val, n))
#		print x[i]
	return prod(y)

def var(sum1, sum2, size):
#	print "sum:", sum1
#	print "sqsum:",sum2
#	print "len:",size
	return (sum2-(pow(sum1,2)/float(size)))/float(size-1)

def stdv1(variance):
#	print variance
	return math.sqrt(variance)

def stdv2(sum1, sum2, size):
	return math.sqrt(var(sum1, sum2, size))

def conf(cl, stdev, df):

	table = open('students_t_table.txt', 'r')
	line1 = table.readline().strip().split(' ')
#	print line1
	pos=1
	list=[]
	while pos < len(line1):
		if float(line1[pos]) == cl: break
		pos+=1
#	print pos
	if pos == len(line1):
		print "WARNING: confidence level not supported"
		return -1
	while 1:
		line = table.readline().strip()
#		print line
		if len(line) == 0:
			 break
		if df<=30 and re.match(r'^'+str(df), line):
			list = line.split(" ")
			break
		elif re.match(r'^inf', line):
			list = line.split(" ")
			break
	if len(list) == 0:
		return -1
	
	tstar = float(list[pos])
#	print tstar

	table.close()

	return tstar*(float(stdev)/float(math.sqrt(df+1)))

def ratio(val1 , val2):
	return float(val1)/float(val2)

def diff(val1, val2):
	return val1-val2
