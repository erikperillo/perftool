import getopt
import sys

flags = ['ds1=', 'ds2=', 'cf=', 'cl=', 'of1', 'of2', 'of=']

opts, args = getopt.getopt(sys.argv[1:], '', flags)

dataset1=dataset2=field=output=0
conf = 95

for p,v in opts:
        if p == '--ds1':
                dataset1 = v
        elif p == '--ds2':
                dataset2 = v
        elif p == '--cf':
                field = v
        elif p == '--cl':
                conf = v
        elif p == '--of1':
                output = 1
	elif p == '--of2':
		output = 2
	elif p == '--of':
		output = v

file1 = open(dataset1, 'r')
file2 = open(dataset2, 'r')

temp1 = file1.readline() 
temp2 = file2.readline()

list1 = temp1.split(",")
list2 = temp2.split(",")

pos1=pos2=0

for word in list1:
	if word == field: break
	pos1++

for word in list2:
	if word == field: break
	pos2++

check1=check2=0

while 1:

	if len(temp1) != 0 and !check1:
		temp1 = file1.readline()
	else check1++

	if len(temp2) != 0 and !check2: 
		temp2 = file2.readline()
	else check2++

	if check1 and check2: break


