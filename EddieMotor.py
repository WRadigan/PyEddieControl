#EddieMotor.py

#print (mraa.getVersion())

import mraa

class EddieMotor:
    
    def __init__(self,pIN1,pIN2,pPWM):
        # Set up the motor pins 
        
        # These are the motor direction pins IN1 and IN2
        self.in1 = mraa.Gpio(pIN1)
        self.in1.dir(mraa.DIR_OUT)
        
        self.in2 = mraa.Gpio(pIN2)
        self.in2.dir(mraa.DIR_OUT)
        
        self.pwm = mraa.Pwm(pPWM)
        self.pwm.period_us(1000) # Is this the correct PWM period?
        self.pwm.enable(True)
        
        #self.pwm.max_period()
        #self.pwm.min_period()
        #self.pwm.read() # Read the current PWM status
        
    def InitStandby(self):
        # Take H Bridge out of standby mode
        pGP49 = 47
        self.stby = mraa.Gpio(pGP49)
        self.stby.dir(mraa.DIR_OUT)
        
        # StandbyValue = 1 --> Take H Bridge out of standby mode
        # StandbyValue = 0 --> Put H Bridge in standby mode
        self.stby.write(1)
        
    def SetSpeed(self,MotorSpeed):
        # The MotorSpeed input can range from -1 to +1
        # and indicates a % of full-scale motor speed.
        # (-) indicates backwards
        # (+) indicates forwards
        
        if MotorSpeed > 0:
            self.in1.write(1)
            self.in2.write(0)                        
        else:
            self.in1.write(0)
            self.in2.write(1)
        
        # Set the PWM value to the motor speed
        self.pwm.write(abs(MotorSpeed))


def RevMotors(M1, M2, max_speed, inc, Revs):
    value = 0.0    
    counter = 0
    
    while True:
        value += inc
        if value >= max_speed:
            inc = -0.01
            value = max_speed + inc
        elif value <= -max_speed :
            inc = 0.01
            value = -max_speed + inc
        elif abs(value) < 0.001:
            counter += 1
        M1.SetSpeed(value)
        M2.SetSpeed(-value)
        time.sleep(0.002)
        if counter > Revs:
            break
    
    M1.SetSpeed(0)
    M2.SetSpeed(0)


# GPIO Interupts (isr) are available on GPIO pins
# This should be very useful for working with the encoders
# ***********************************************************
# http://iotdk.intel.com/docs/master/mraa/python/example.html
# ***********************************************************

if __name__ == "__main__":
    import time
    from subprocess import call
        
    # Pin Name = Libmraa number. 
    #RIGHT motor
    pGP14      = 36
    pGP15      = 48
    pPWM1      = 14
    
    #LEFT motor
    pGP47      = 46
    pGP48      = 33
    pPWM0      = 20
        
    RightMotor = EddieMotor(pGP14,pGP15,pPWM1)
    
    #//Take H Bridge out of standby mode
    RightMotor.InitStandby() # Only do this for ONE MOTOR
    
    LeftMotor  = EddieMotor(pGP47,pGP48,pPWM0) # WiFi problem with pin 48
    call(["systemctl", "restart", "wpa_supplicant"]) # This fixes it
        
    RevMotors(RightMotor, LeftMotor, 0.8, 0.1, 4)
    
        
    #//Motor A
    #int PWMA = PWM0 -> IO3; //Speed control 
    #int AIN1 = GP48 -> IO7; //Direction
    #int AIN2 = GP47 -> IO17(A3); //Direction
    
    #STBY - GP49 -> IO8
    
    #//Motor B
    #int PWMB = PWM1 -> IO5; //Speed control
    #int BIN1 = GP15; ???         //Direction
    #int BIN2 = GP14 -> IO18(A4); //Direction
    
    # The edison pinout is available here:
    # https://cdn.sparkfun.com/assets/learn_tutorials/3/2/2/edison-pinout.pdf
    
    # Libmraa uses a different naming convention for the pin names:
    # MRAA Pin mapping here:
    # ***************************************************
    # http://iotdk.intel.com/docs/master/mraa/edison.html
    # ***************************************************
    
    
