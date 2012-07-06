# this a module with statistics functions

import math

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
	p=1.
        for val in x:
                p *= float(val)
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
			xk = x0 - ((pow(x0, n)-val)/n*pow(x0, n-1))
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

def conf(cl, stdev, size):
	#tstar attribution yet to be coded
	return tstar*(stdev/math.sqrt(size))

def ratio(val1 , val2):
	return val1/val2

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

