#! /usr/bin/env python

# name csv_file.py
# author Julia Ramos Beltrao
# julia.beltrao@students.ic.unicamp.br
# since 2013

import verbose.py

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
	try:
		f = open(file, 'a')
		line = str(line).replace('[','').replace(']','').replace(' ','')
		f.write(newline+line)
		f.close()
	except IOError:
		return 1
	return 0
	
#TODO: escrever funcao
#def read(file, line, col):

