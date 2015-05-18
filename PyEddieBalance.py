# Script to implement basic balance control in python.


import EddieIMU
import EddieMotor
from subprocess import call
from math import degrees, copysign
from time import sleep, time
import sys
import EddiePID

import csv

# Pin Name = Libmraa number. 
#RIGHT motor
pGP14      = 36
pGP15      = 48
pPWM1      = 14

#LEFT motor
pGP47      = 46
pGP48      = 33
pPWM0      = 20


RightMotor = EddieMotor.EddieMotor(pGP14,pGP15,pPWM1)
RightMotor.InitStandby() # Only do this for ONE MOTOR
LeftMotor  = EddieMotor.EddieMotor(pGP47,pGP48,pPWM0) # WiFi problem with pin 48
call(["systemctl", "restart", "wpa_supplicant"]) # This fixes it

IMUIni = '/home/root/PyEddieControl/EddieRTIMULib'
imu = EddieIMU.EddieIMU(IMUIni)

poll_interval = imu.imu.IMUGetPollInterval()

print "Proportional speed control begins..... NOW!"
print "10 seconds duration"
sys.stdout.flush()

sleep(0.1)

SetAngle = -1.29 #radians = -74deg
MaxError = 0.25 #radians
FallOver = 0.50 #radians

phiPID = EddiePID.PID()

# Set up the PID control variables
phiPID.SetKp(2.5)
phiPID.SetKi(0.25)
phiPID.SetKd(0.08)

TestDuration = 10.0


SAVE_CSV_DATA = True

if SAVE_CSV_DATA:
    CSVDataFile = open("EddieData.csv", 'wb')
    wr = csv.writer(CSVDataFile)
    wr.writerow(('Roll','Pitch','Yaw','mSpeed','Time'))

tStart = time()
phiPID.Initialize() # Sets errors to zero

while ((time() - tStart) < TestDuration):
    pose = imu.GetPose()
    if pose:
        #dAngle = degrees(pose[1])
        #print "R:{0:5.2f} P:{1:5.2f} Y:{2:5.2f}".format(degrees(pose[0]), degrees(pose[1]), degrees(pose[2]))
        
        Error = SetAngle - pose[1]
        
        if abs(Error) > FallOver:
            mSpeed = 0.0
            phiPID.Initialize() # Sets errors to zero
        else:
            if abs(Error) > MaxError: # Limit the maximum error signal
                Error = copysign(MaxError,Error)
            mSpeed = phiPID.GenOut(Error)
        
        
        # This "Pose Estimation" is TERRIBLE.
        if pose[2] < 0.0:
            mSpeed = -mSpeed
        #print "mSpeed = {0}".format(mSpeed)
        
        RightMotor.SetSpeed(mSpeed)
        LeftMotor.SetSpeed(-mSpeed)
        
        # This should be done in a faster way than comparing the flag _every time_!
        if SAVE_CSV_DATA: 
            wr.writerow(pose + (mSpeed,time()))
    sleep(poll_interval*1.0/1000.0)

print "Time's up, test is over"

RightMotor.SetSpeed(0)
LeftMotor.SetSpeed(0)

CSVDataFile.close()





