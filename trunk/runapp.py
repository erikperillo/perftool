

import re
import sys
import time
import getopt
import commands

flags = 'n:c:o:aw'

opts, args = getopt.getopt(sys.argv[1:],flags)

print opts
print args

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
	for i in range(n)
#		status, output = os.system("usr\bin\time " + c)
#		if (!status)
		handle = os.popen("/usr/bin/time -f '%x %e %U %S %K %F %R' " + c, 'r', 1)
			for line in handle:
		handle.close()
		
		

