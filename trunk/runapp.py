

import sys
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

print numb
print cmd
print output
print app

execute(cmd, numb)



def execute(c, n):
	for i in range(n)
		status, output = os.system("usr\bin\time " + c)
		if (!status)
		handle = os.popen("usr\bin\time " + c, 'r', 1)
			for line in handle:
   				 if line ==
		handle.close()
		
		

