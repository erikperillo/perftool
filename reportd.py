#! /usr/bin/env python

import sys
import plot
import os.path
import subprocess

# gets number of latest revision of svn
def get_rev():
	cmd = "svn info https://neopz.googlecode.com/svn/trunk/ | grep Revision | cut -d ' ' -f2" 
	P = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=False)
	return int(P.stdout.readline())

# ensure compd has permission to be run
def make_exec():
	cmd = "chmod +x /local/julia/perftool/compd.py"
        P = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=False)
        return 

def reassemble_data(v):

	j=0
	cfg=[]

	while j < len(v[0]):
		i=0
		aux=[]
		while i < len(v):
			aux.append(v[i][j])		
			i=i+1
		cfg.insert(j, aux)
		j=j+1

	return cfg


# Main

dir_base = "/local/julia/performance_regression/"
dir_input = dir_base + "results/r"
dir_output = dir_base + "graphs/"

nrev_min = 4166
nrev_max = get_rev()
nrev = nrev_min

conf = 95 #confidence level for compd
CPG=5 #number of curves per graph

make_exec()

#print "rev_max", nrev_max

for p in '1', '2':

	for nsub in '2', '4', '8', '16' ,'32', '64':

		for nt_ in '0', '1', '2', '4', '8':

			r=[]
			time=[]
			error=[]
			pos=0

			while nrev <= nrev_max:
				
				dir_name = dir_input + str(nrev)

				if os.path.exists(dir_name):

					av=[]
					ci=[]

					for ntsm in '0', '2', '4', '8':

						filename = "/cubo1.double.txt.ckpt1.p" + p + ".nsub" + nsub + ".nt_a." + nt_ + ".nt_d." + nt_ + ".nt_m." + nt_ + ".nt_sm." + ntsm + ".ass"
						path = dir_name + filename + ".rdt"
			 			if os.path.exists(path):
							cmd = "/local/julia/perftool/compd.py --ds " + path + " --cf ELAPSED --cl " + str(conf) + " --of '(ds-av) (ds-ci)'"
							#print cmd 	
							process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=False)
							data = process.stdout.readline().strip().split(" ")	
							#print data
							av.append(float(data[0]))
							ci.append(float(data[1]))
							#print "nrev: ", nrev
							#print r
						else: 	
							sys.stderr.write("WARNING: could not find " + path + "\n") 		
							av.append(0)
                                                        ci.append(0)
	
								
					time.insert(pos, av)
					error.insert(pos, ci)
					r.append(nrev)
					pos = pos+1
					#print "time: ", time
					#print "error: ", error
					#print "pos: ", pos

				nrev = nrev+1
			
			filename = "cubo1.double.txt.ckpt1.p" + p + ".nsub" + nsub + ".nt_a." + nt_ + ".nt_d." + nt_ + ".nt_m." + nt_ + ".nt_sm.ass."
			plot.x_vs_time_plot([0,2,4,8], time, error, r, cpg=5, l1='r', l2='ntsm', dout=dir_output, file=filename)
			#sys.exit(1)
			#print "time: ", time
			#print ' '
			filename = "cubo1.double.txt.ckpt1.p" + p + ".nsub" + nsub + ".nt_a." + nt_ + ".nt_d." + nt_ + ".nt_m." + nt_ + ".ass"
			plot.x_vs_time_plot(r, reassemble_data(time), reassemble_data(error), leg=[0,2,4,8], cpg=4, l1='ntsm=', l2='revision', dout=dir_output, file=filename)
			#sys.exit(1)
			#print "no de revisoes: ", len(r)
			#print r
			nrev = nrev_min



