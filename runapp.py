import os
import sys
import time
import errno
import getopt
import subprocess

def execute(c, n, o, a, w):

	cmd = "/usr/bin/time -f '%x %e %U %S %K %F %R' " + c
	fail = 0

	if not a:
		datafile = open(o+'.rdt', 'w')
		datafile.write("run,t_real,t_user,t_sys,memory_used,major_pagefaults,minor_pagefaults\n")
	else:
		datafile = open(o+'.rdt', 'a')

	if w:
		try:
			os.mkdir(o)
		except OSError as e:
			if e.errno == errno.EEXIST:
				print "The directory already exists. Resuming..."
			else: 
				print "WARNING: could not create directory (" + e + ")"
				sys.exit(4)
	
	for i in range(int(n)):
		date = time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime())
		handle = open(o+"_"+date , 'w')
		p = subprocess.Popen(cmd,shell=True, stdout=handle, stderr=subprocess.PIPE, cwd=o, close_fds=True)
		handle.close()
		data = p.stderr.readline().strip().split(" ")
		print data
		if not(int(data[0])):
			datafile.write(str(i+1)+','+data[1]+','+data[2]+','+data[3]+','+data[4]+','+data[5]+','+data[6]+'\n')
		else: fail+=1
									
	datafile.close()	

	if fail:
		print "The application has failed %i times" %(fail)
	

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

execute(cmd, numb, output, app, wd)
