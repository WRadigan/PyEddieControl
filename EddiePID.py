#-------------------------------------------------------------------------------
# PID.py
# A simple implementation of a PID controller
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

import time

class PID:
    """ Simple PID control.

        This class implements a simplistic PID control algorithm. When first
        instantiated all the gain variables are set to zero, so calling
        the method GenOut will just return zero.
    """
    def __init__(self):
        # initialze gains
        self.Kp = 0
        self.Kd = 0
        self.Ki = 0
        
        self.Initialize()
        
    def SetKp(self, invar):
        """ Set proportional gain. """
        self.Kp = invar
        #print "Kp = {0}".format(self.Kp)
        
    def SetKi(self, invar):
        """ Set integral gain. """
        self.Ki = invar
        #print "Ki = {0}".format(self.Ki)

    def SetKd(self, invar):
        """ Set derivative gain. """
        self.Kd = invar
        
    def SetPrevErr(self, preverr):
        """ Set previous error value. """
        self.prev_err = preverr
        
    def Initialize(self):
        # initialize delta t variables
        self.currtm = time.time()
        self.prevtm = self.currtm
        
        self.prev_err = 0
        
        # term result variables
        self.Cp = 0
        self.Ci = 0
        self.Cd = 0
        
    def GenOut(self, error):
        """ Performs a PID computation and returns a control value based on
            the elapsed time (dt) and the error signal from a summing junction
            (the error parameter).
        """
        self.currtm = time.time()               # get t
        dt = self.currtm - self.prevtm          # get delta t
        #print "dt = {0}".format(dt)
        de = error - self.prev_err              # get delta error
        
        self.Cp = self.Kp * error               # proportional term
        self.Ci += error * dt                   # integral term
        
        self.Cd = 0
        if dt > 0:                              # no div by zero
            self.Cd = de/dt                     # derivative term
        
        
        # Might need to add min/max limits to the Ci and Cd term
        # It's common to refer to the Ki and Kd gains using a time-constant
        # E.g. Kp = K, Ki = K/Ti & Kd = K Td
        # http://ww1.microchip.com/downloads/en/AppNotes/00964A.pdf
        
        #print "Cp = {0} Ci = {1} Cd = {2}".format(self.Cp, self.Ci, self.Cd)
        self.prevtm = self.currtm               # save t for next pass
        self.prev_err = error                   # save t-1 error
        
        # sum the terms and return the result
        return self.Cp + (self.Ki * self.Ci) + (self.Kd * self.Cd)