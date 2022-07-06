import sys
import matplotlib.pyplot as plt
import numpy
# Opening file
fl=''
try:
	fl=sys.argv[1]
except:
	print("No args using default")
	fl='nvideastats.txt'
file = open(fl, 'r')
count = 0

rvalues=[]
cpuvalues=[]
gpuvalues=[]
finalcount=[0]

# Using for loop
for line in file:
	count +=0.5
	line=line.split(" ")
	ram=line[1].split("/")[0]
	cpu=line[12].replace("[","").replace("]","").split(",")
	finalcpu=0
	for c in cpu:
		finalcpu += float(c.split("%")[0])
	finalcpu /= 4

	gpu=line[16].split("%")[0]
	print(finalcpu)
	print(ram)
	print(gpu)
	rvalues.append(float(ram))
	cpuvalues.append(float(finalcpu))
	gpuvalues.append(float(gpu))
	finalcount.append(count)

# Closing files
file.close()
finalcount=finalcount[:-1]

#normalize values
for i in range(len(rvalues)):
	rvalues[i] = rvalues[i]/1980
for i in range(len(cpuvalues)):
	cpuvalues[i] = cpuvalues[i]/100
for i in range(len(gpuvalues)):
	gpuvalues[i] = gpuvalues[i]/100
 
# converting list to array
r_arr = numpy.array(rvalues)
c_arr = numpy.array(cpuvalues)
g_arr = numpy.array(gpuvalues)

finalcount = numpy.array(finalcount)

plt.plot(finalcount,r_arr,'r',label='RAM')
plt.plot(finalcount,c_arr,'b',label='CPU')
plt.plot(finalcount,g_arr,'g',label='GPU')
leg = plt.legend(loc='upper left')
plt.ylabel('Percentage usage  (%)')
plt.xlabel('Time     (secs)')
plt.show()
