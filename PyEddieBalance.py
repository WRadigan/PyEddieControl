# Script to implement basic balance control in python.


import EddieIMU
import EddieMotor
from subprocess import call
from math import degrees
from time import sleep, time

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

IMUIni = '/home/root/PyEddieControl/EddieRTIMULib.ini'
imu = EddieIMU.EddieIMU(IMUIni)

poll_interval = imu.imu.IMUGetPollInterval()

print "Proportional speed control begins..... NOW!"
print "10 seconds duration"

sleep(0.1)

tStart = time()

# This is the 'read loop'
while ((time() - tStart) < 10):
    #rAngle = imu.GetPitch()
    pose = imu.GetPose()
    #if rAngle:
    if pose:
        dAngle = degrees(pose[1])
        #print "R:{0:5.2f} P:{1:5.2f} Y:{2:5.2f}".format(degrees(pose[0]), degrees(pose[1]), degrees(pose[2]))
        
        mSpeed = (dAngle+90) / 50
        if pose[2] > 0:
            mSpeed = -mSpeed
        #print "mSpeed = {0}".format(mSpeed)
        RightMotor.SetSpeed(mSpeed)
        LeftMotor.SetSpeed(-mSpeed)
    sleep(poll_interval*1.0/1000.0)

print "Time's up, test is over"

RightMotor.SetSpeed(0)
LeftMotor.SetSpeed(0)




