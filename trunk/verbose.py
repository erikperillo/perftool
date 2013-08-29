#! /usr/bin/env python

import sys

# prints an error message and the module info
# exits if required
# message: string
# status: int
def fail(message, status=0):
        sys.stderr.write("ERROR: " + message+'\n')
#        usage()
        if status:
                sys.exit(status)

# prints a warning message and returns
# message: string
def warning(message):
        sys.stderr.write("WARNING: " + message + '\n')

def verbose (v, msg):
        if v < VERBOSE_LEVEL:
                sys.stdout.write(msg + '\n')

