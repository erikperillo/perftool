

import sys
import time
import getopt
import subprocess

flags = 'n:c:o:aw'

opts, args = getopt.getopt(sys.argv[1:],flags)

numb=cmd=output=app=wd=0

for p,v in opts:
	if p == '-n':
		numb = v
	elif p == '-c':
		cmd = v
	elif p == '-o':
		output = v
	elif p == '-a':
		app = 1
	elif p == '-w':
		wd = 1

if not numb:
	print "Number of runs missing"
	sys.exit(1)
if not cmd:
	print "Application name missing"
	sys.exit(2)
if not output:
	print "Name for the output file missing"
	sys.exit(3)

execute(cmd, numb, app, wd)


def execute(c, n, a, w):

	cmd = "/usr/bin/time -f '%x %e %U %S %K %F %R' " + c
	date = time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime())
	datafile = open(c+'_'+date+'.rdt', 'w')
	datafile.write("run,t_real,t_user,t_sys,memory_used,major_pagefaults,minor_pagefaults")
	fail = 0

	for i in range(n):
		date = time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime())
		handle = open(c+"_"+date , 'w')
		p = subprocess.Popen(cmd,shell=True, stdout=handle, stderr=subprocess.PIPE, close_fds=True)
		handle.close()
		data = p.stderr.readline().strip().split(" ")
		if not(data[0]):
			datafile.write("%i,"%i+data[1]+','+data[2]+','+data[3]+','+data[4]+','+data[5]+','+data[6])
		else: fail+=1
									
	datafile.close()	
		

