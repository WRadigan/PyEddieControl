# Class to get (and report) pose data from the RTIMULib module.

import RTIMU
import sys

class EddieIMU:
    
    def __init__(self,IniFile):
        # Set up the INI File and initialize the RTIMULib
        
        self.s = RTIMU.Settings(IniFile) # Should have some check to make sure that INI is good
        self.imu = RTIMU.RTIMU(self.s)
        
        print("IMU Name: " + self.imu.IMUName())
        
        if (not self.imu.IMUInit()):
            print("IMU Init Failed")
            sys.exit(1)
        else:
            print("IMU Init Succeeded")
        
        # this is a good time to set any fusion parameters        
        self.imu.setSlerpPower(0.02)
        self.imu.setGyroEnable(True)
        self.imu.setAccelEnable(True)
        self.imu.setCompassEnable(True)
        
        poll_interval = self.imu.IMUGetPollInterval()
        print("Recommended Poll Interval: %dmS\n" % poll_interval)
                
    def GetPose(self):
        # Returns Eddie's current pitch (forward & backward) angle
        if self.imu.IMURead():
            data = self.imu.getIMUData()
            fusionPose = data["fusionPose"]
            return fusionPose
            # Pitch = ~ -90deg [-1.571rad] is 'standing up' for Eddie
                
    def GetPitch(self):
        # Returns Eddie's current pitch (forward & backward) angle
        if self.imu.IMURead():
            data = self.imu.getIMUData()
            fusionPose = data["fusionPose"]
            angle = fusionPose[1] # In Radians!!!!!
            return angle
            # Pitch = ~ -90deg [-1.571rad] is 'standing up' for Eddie
            
    def GetRoll(self):
        # Returns Eddie's current pitch (forward & backward) angle
        if self.imu.IMURead():
            data = self.imu.getIMUData()
            fusionPose = data["fusionPose"]
            angle = fusionPose[0] # In Radians!!!!!
            return angle
            
    def GetYaw(self):
        # Returns Eddie's current pitch (forward & backward) angle
        if self.imu.IMURead():
            data = self.imu.getIMUData()
            fusionPose = data["fusionPose"]
            angle = fusionPose[2] # In Radians!!!!!
            return angle
            
            
        
if __name__ == "__main__":
    #from subprocess import call
    from os import getcwd
    from math import degrees
    from time import sleep
    
    # From the Intel Edison
    #>>> os.getcwd()
    #'/home/root/RTIMULib/Linux/python/tests'
    IMUIni = getcwd() + '/EddieRTIMULib.ini'
    IMUIni = '/home/root/PyEddieControl/EddieRTIMULib.ini'
    
    imu = EddieIMU(IMUIni)
    
    poll_interval = imu.imu.IMUGetPollInterval()
    
    
    # This is the 'read loop'
    while True:
        pAngle = imu.GetPitch()
        if pAngle:
            print "Pitch = {0}".format(degrees(pAngle))
        sleep(poll_interval*1.0/1000.0)
    
