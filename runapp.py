#! /usr/bin/env python

import os
import sys
import time
import errno
import getopt
import subprocess

def usage():
	print "Help on runapp"
        print "NAME"
        print "\trunapp"
        print "DESCRIPTION"
        print "\tThe runapp is a tool for collecting certain data about an application"
        print "ARGUMENTS"
        print "\t-n N: number of times the application will be run"
        print "\t-o filename: name of the file on which the collected data will be saved."
        print "\t-c cmd: a string containig the entire path for the application."
        print "\t-w: create a directory with the same name as the output file (minus the extension) and runs the application within it (optional)"
        print "\t-a: append the collected data into an existing file specified (optional)"

def execute(c, n, o, a, w):

	cmd = "/usr/bin/time -f '%x %e %U %S %K %F %R' " + c
	fail = 0
	wd = None

	if not a:
		try:
			datafile = open(o+'.rdt', 'w')
		except IOError:
			print "WARNING: could not create file ", o+'.rdt'
			sys.exit(2)
		datafile.write("run,t_real,t_user,t_sys,memory_used,major_pagefaults,minor_pagefaults\n")
	else:
		try:
			datafile = open(o+'.rdt', 'a')
		except IOError:
			print "WARNING: could not open file ", o+'.rdt'
			sys.exit(2)

	if w:
		try:
			os.mkdir(o)
			wd = o
		except OSError as e:
			if e.errno == errno.EEXIST:
				print "The directory already exists. Resuming..."
			else: 
				print "WARNING: could not create directory (" + e + ")"
				sys.exit(2)
	
	for i in range(int(n)):
		date = time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime())
		handle = open(o+"_"+date , 'w')
		p = subprocess.Popen(cmd,shell=True, stdout=handle, stderr=subprocess.PIPE, cwd=wd, close_fds=False)
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

try:
	opts, args = getopt.getopt(sys.argv[1:],flags)
except GetoptError:
	print "WARNING: one or more flags you entered requires an argument"
	usage()
	sys.exit(1)

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
	usage()        
	sys.exit(1)
if not cmd:
        print "Application name missing"
	usage()        
	sys.exit(1)
if not output:
        print "Name for the output file missing"
	usage()
        sys.exit(1)

execute(cmd, numb, output, app, wd)
