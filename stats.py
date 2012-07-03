# this a module with statistics functions

import math

def mean1(sum, size):
	return sum/size

def mean2(x):
	sum=0
	for n in x:
		sum+=n
	return sum/len(x)

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
	
	
def var(sum1, sum2, size):
	return (sum2-(sum1**2/size))/(size-1)

def stdv(sum1, sum2, size):
	return sqrt(var(sum1, sum2, size))

def conf(stdev, size):
	#atribuicao de tstar vira aqui
	return tstar*(stdev/sqrt(size))
