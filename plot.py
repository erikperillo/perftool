#! /usr/bin/env python

import sys
import os.path
import subprocess


def get_rev():
	cmd = "svn info https://neopz.googlecode.com/svn/trunk/ | grep Revision | cut -d ' ' -f2" 
	P = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=False)
	return int(P.stdout.readline())

def plot():


# Main

dir_base = "/local/julia/performance_regression/"
dir_input = dir_base + "results/r"
dir_output = dir_base + "graphs/"

nrev_min = 4166
nrev_max = get_rev()
nrev = nrev_min

conf = 95


for p in ['1', '2']:

	for nsub in ['2', '4', '8', '16', '32', '64']:

		for nt_ in ['0', '1', '2', '4', '8']:

			time=[]
			error=[]
			pos=0

			while nrev <= nrev_max:

				dir_name = dir_input + str(nrev)
				if os.path.exists(dir_name):

					av=[]
					ci=[]
					r=[]

					for ntsm in ['0', '2', '4', '8']:

						filename = dir_name + "/cubo1.double.txt.ckpt1.p" + p + ".nsub" + nsub + ".nt_a." + nt_ + ".nt_d." + nt_ + ".nt_m." + nt_ + ".nt_sm." + ntsm + ".ass.rdt"
			 			if os.path.exists(filename):
							cmd = "/local/julia/perftool/compd.py --ds " + filename + " --cf ELAPSED --cl " + str(conf) + " --of '(ds-av) (ds-ci)'"
							print cmd 	
							process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=False)
							data = process.stdout.readline().strip().split(" ")	
							av.append(float(data[0]))
							ci.append(float(data[1]))
							r.append(nrev)
						else: 	
							sys.stderr.write("WARNING: could not find " + filename + "\n") 		
							v.append(0)
                                                        ci.append(0)
                                                        r.append(nrev)
	
								
					time.insert(pos, av)
					error.insert(pos, ci)
					pos = pos+1
					print "time: ", time
					print "error: ", error
					print "pos: ", pos

				nrev = nrev+1

			plot()
			#sys.exit(1)
			nrev = nrev_min



