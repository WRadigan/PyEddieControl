# Script to implement basic balance control in python.


import EddieIMU
import EddieMotor
from subprocess import call
from math import degrees
from time import sleep

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


# This is the 'read loop'
while True:
    rAngle = imu.GetPitch()
    if rAngle:
        dAngle = degrees(rAngle)
        print "Pitch = {0}".format(dAngle)
        
        mSpeed = (dAngle+90) / 100
        print "mSpeed = {0}".format(mSpeed)
        RightMotor.SetSpeed(mSpeed)
        LeftMotor.SetSpeed(mSpeed)
    sleep(poll_interval*1.0/1000.0)


RightMotor.SetSpeed(0)
LeftMotor.SetSpeed(0)
