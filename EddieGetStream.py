'''
This is a script to collect the output data stream from Eddie for the 
purpose of optimizing the control loop.

The data is sent with this format:
print( "PIDout: %0.2f,%0.2f\tcompPitch: %6.2f kalPitch: %6.2f\tPe: %0.3f\tIe: %0.3f\tDe: %0.3f\tPe: %0.3f\tIe: %0.3f\tDe: %0.3f\r\n",

'''

from PyEddiePlus import EddiePlus
import sys
from time import sleep

# The standard 'scientific python' import statements
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


col_names = [
'speedPIDoutput',
'pitchPIDoutput',
'filteredPitch',
'kalmanAngle',
'pitchPIDError',
'pitchPIDAccumulatedError',
'pitchPIDDifferentialError', 
'speedPIDError',
'speedPIDAccumulatedError',
'speedPIDDifferentialError',
]



# This is the IP address for my Eddie, yours will probably be different
MyEddie = EddiePlus("Edward","192.168.1.113")

MyEddie.StreamControl(True)

data = MyEddie.GetStreamData(1000)

MyEddie.StreamControl(False)

EddyData = pd.DataFrame(data, columns = col_names)

#print EddyData

print "\n\n\nSize Data = {0} \n\n\n".format(len(data))

plt.figure()
plt.plot(EddyData)
plt.legend(col_names)

plt.figure()
plt.plot(EddyData.filteredPitch)
plt.legend('Pitch Angle')

plt.show()


MyEddie.Disconnect()

# Return the dataset to the user for further analysis in an iPython shell
#return EddyData