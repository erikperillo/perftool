# this a module with statistics functions

import math
import re

def sum(x):
	s=0
        for n in x:
                s+=n
        return s

def sqsum(x):
	s2=0
	for n in x:
		s2+=pow(n, 2)
	return s2

def prod(x):
	p=long(1)
        for val in x:
                p *= long(val)
#		print "=====",p
#	print "----------------->",p
	return p	

def nroot(val, n):
	if val == 1:
		return 1
	elif n == 2:
		return math.sqrt(val)
	else:
		x0 = 0
		xk = math.sqrt(val)
	
		while (xk != x0):
			x0 = xk
#			print x0,n,val
			a = pow(x0, n) - val
			b = pow(x0, n-1) * n
			xk = x0 - (long(a)/long(b))
	return xk
	
def average(ssum, ssize):
	return float(ssum)/float(ssize)

def gmean(x):
	return nroot(prod(x),len(x))

def var(sum1, sum2, size):
	return (sum2-(sum1**2/size))/(size-1)

def stdv1(variance):
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

def diff(x, y):

        dif=[]

        if len(x) > len(y):
                n = len(y)
                d = len(x) - len(y)
        elif len(x) < len(y):
                n = len(x)
                d = len(y) - len(x)
        else:
                n = len(x)
                d = 0

        for i in range(n):
                dif.append(x[i]-y[i])

        return dif, d

