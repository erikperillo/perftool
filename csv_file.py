#! /usr/bin/env python

# name csv_file.py
# author Julia Ramos Beltrao
# julia.beltrao@students.ic.unicamp.br
# since 2013

import os.path
import verbose as vb

newline='\n'

def create(file, header):
	#TODO: checar se arquivo contem extensao pdt
	try:
		f = open(file, 'w')
		f.write(header)
		f.close()
	except IOError:
		return 1
	return 0

def write(file, line):
	check(file)
	try:
		f = open(file, 'a')
		line = str(line).replace('[','').replace(']','').replace(' ','')
		f.write(newline+line)
		f.close()
	except IOError:
		return 1
	return 0
	
#TODO: testar funcao
def read(file, line='*', col='*'):
	status=0
	list=[]
	check(file)
	try:
		f = open(file, 'r')
		if line=='*' and col=='*':
			list=f.readlines()
		else:
			if line == '*':
				temp=f.readlines()
				for l in temp:
					list.append(l[col-1])

			elif col == '*':
				list=f.readlines()[line-1]

			else:
				list=f.readlines()[line-1]
				list=list.split(',')[col-1]	

		f.close()
	except IOError:
		status=1 
	return status, list

#TODO: testar funcao
def check(file):
	status=0
	if not os.path.exists(file):
		vb.fail("could not find "+file+": file does not exist.",2)
	try:
		f = open(file, 'r')
		lines = f.readlines()
	except IOError:
		return 1
	ncol = len(line[0])
	for line in lines:
		if len(line) != ncol:
			status=1
			break
	f.close()
	return status		
