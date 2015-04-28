'''
To remote control Eddie you must gain control with a "bind" process that involves:

Sending "DISCOVER" to 255.255.255.255 on port 4240
  - All Eddie's on the network will respond with "DISCOVER: [unique name]".

**** BROADCAST UDP is currently not working in this Python implementation ****


Using the IP/name from the response send "BIND" to [ip address] on port 4240
- Eddie will respond with "BIND: OK".

Now you can send command packets (currently listed in main.c) to UDP port 4242.

EddieBalance listens for data on two ports:
    - One [4240] for gaining control and the other [4242] for sending commands.
    - And Eddie returns data to the last IP received on the response port.

/* Incoming UDP Command Packet handler:
 *
 * DRIVE[value]	=	+ is Forwards, - is Reverse, 0.0 is IDLE
 * TURN[value]	=	+ is Right, - is Left, 0.0 is STRAIGHT
 *
 * SETPIDS = Changes all PIDs for speed and pitch controllers
 * GETPIDS = Returns all PIDs for speed and pitch controllers via UDP
 *
 * PIDP[P,I,D][value] = adjust pitch PIDs
 * SPID[P,I,D][value] = adjust speed PIDs
 *
 * KALQA[value] = adjust Kalman Q Angle
 * KALQB[value] = adjust Kalman Q Bias
 * KALR[value] = adjust Kalman R Measure
 *
 * STOPUDP	= Will stop Eddie from sending UDP to current recipient
 *
 * STREAM[0,1] = Enable/Disable Live Data Stream
 *
 */
 
'''

import socket
#import ctypes
import sys
import numpy as np
import re


class EddiePlus:
    # Basic class to control an instance of a single EddiePlus
    
    def __init__(self,Name,IPAddress):
        
        self.IPAddress = IPAddress
        self.Name = Name
        self.host_any = ""
        self.EddieBroadcastAddr = ('<broadcast>',4240)
        self.EddieControlAddr = (self.IPAddress, 4240)
        self.EddieCommandAddr = (self.IPAddress, 4242)
        self.EddieResponseAddr = (self.host_any, 4243)
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
        self.sock.settimeout(2.0)
        
        
        self.GetStreamingData = False
        #self.UDPTimer = RepeatedTimer(1, self.GetPIDS())

        # Initialize this particular Eddy to make sure he's alive and well.
        if self.InitializeEddie():
            # Initialization successful!
            print "Eddie has been found!"
            print "IP Addr = {0}".format(self.IPAddress)
        else:
            print "Failed to find Eddy"
            print "You might try restarting your Python interpreter,"
            print "sometimes the sockets get stuck there."
            sys.exit()
        
        
    def InitializeEddie(self):
        # If an Eddie responds, then there is a robot on the other side, and 
        # commands can be sent.
        
        print "Looking for Eddie on: {0}".format(self.EddieControlAddr)
        # Set up the receive port
        try:
            try:
                self.sock.bind(self.EddieResponseAddr)
                print 'Socket bound successfully '
            except socket.error , msg:
                print 'Bind failed.  Error : ' + str(msg)
                sys.exit() # bail
            
            # Send "DISCOVER" to the control UDP address to confirm that an Eddie exists here.
            ByteCount = self.sock.sendto("DISCOVER", self.EddieControlAddr)
            #ByteCount = self.sock.sendto("DISCOVER", self.EddieBroadcastAddr)
            #print "Send Byte Count: {0}".format(ByteCount)
            
            # Try to recieve DISCOVER return message
            try:
                data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
                print "received message:", data
            except socket.timeout:
                print "Oops. Timed out.  Maybe nobody's home?"
                
            # Send "BIND" to the control UDP address to enable commands
            ByteCount = self.sock.sendto("BIND", self.EddieControlAddr)
            #print "Send Byte Count: {0}".format(ByteCount)

            # Try to recieve BIND return message
            try:
                data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
                print "received message:", data
                
                if data.find("OK"): # If the return string contains "OK", we're good.
                    return 1
                else:
                    print "Eddie was found, but he's unavailable for some reason."
            except socket.timeout:
                print "Oops. Timed out.  Maybe nobody's home?"

            # Eddie is here, looks like we're good to go.
            return 1
            
        except:
            # Hmmmm. Something didn't work.
            self.sock.close()
            return 0
    
    def Drive(self,Speed):
        # Send the command to drive, along with the speed integer.
        Speed = int(Speed)
        if abs(Speed) > 15:
            print "Whoa there sparky!  Slow down"
            return 0
        
        cmd = "DRIVE{0}".format(int(Speed))
        #print self.Name + ": " + cmd
        ByteCount = self.sock.sendto(cmd, self.EddieCommandAddr)
        return ByteCount

                        
    def Turn(self,TurnSpeed):
        # Send the command to drive, along with the speed integer.
        TurnSpeed = int(TurnSpeed)
        if abs(TurnSpeed) > 15:
            print "Seriously, do I look like a Corvette to you?"
            return 0
            
        cmd = "TURN{0}".format(int(TurnSpeed))
        #print self.Name + ": " + cmd
        ByteCount = self.sock.sendto(cmd, self.EddieCommandAddr)
        return ByteCount

    
    def Disconnect(self):
        # Make sure that Eddie is stopped before we go.
        self.Drive(0)
        self.Turn(0)
        self.StreamControl(False) # Shut down streaming data

        # We're done for now.
        self.sock.close()

    def GetPIDS(self):
        # GETPIDS = Returns all PIDs for speed and pitch controllers via UDP
        
        ByteCount = self.sock.sendto("GETPIDS", self.EddieCommandAddr)
        
        # Should return a string like:
        # "  CURRENTPIDS:6.500,600.000,30.000,0.020,800.000,340.000  "
        try:
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
            print "received message:", data
        except socket.timeout:
            print "Oops. Timed out.  Maybe nobody's home?"


    def StreamControl(self,StreamOnOff):
        # GETPIDS = Returns all PIDs for speed and pitch controllers via UDP
        
        if StreamOnOff and self.GetStreamingData:
            print "Already streaming data"
            return
        
        if StreamOnOff:
            ByteCount = self.sock.sendto("STREAM1", self.EddieCommandAddr)
            self.GetStreamingData = True
            #self.UDPTimer.start()
            print "DATA STREAM: On"
        else:
            ByteCount = self.sock.sendto("STREAM0", self.EddieCommandAddr)
            self.GetStreamingData = False
            #self.UDPTimer.stop()
            print "DATA STREAM: Off"
        
        # Should cause Eddie to start sending a string like:
        # "  "PIDout: %0.2f,%0.2f\tcompPitch: %6.2f kalPitch: %6.2f\tPe: %0.3f\tIe: %0.3f\tDe: %0.3f\tPe: %0.3f\tIe: %0.3f\tDe: %0.3f\r\n"  "
        
            
    def GetStreamData(self,DataPoints):
        
        '''
        speedPIDoutput = np.zeros(DataPoints) 
	pitchPIDoutput = np.zeros(DataPoints)
        filteredPitch = np.zeros(DataPoints)
        kalmanAngle = np.zeros(DataPoints)
        pitchPIDError = np.zeros(DataPoints) 
        pitchPIDAccumulatedError = np.zeros(DataPoints)
        pitchPIDDifferentialError = np.zeros(DataPoints) 
        speedPIDError = np.zeros(DataPoints)
        speedPIDAccumulatedError = np.zeros(DataPoints)
	speedPIDDifferentialError = np.zeros(DataPoints)
	'''
	
	DataValues = np.zeros((DataPoints,10))
	ThisRow = 0
	
	for ii in range(DataPoints):
            try:
                data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
                #print data
                values = re.findall("[-+]?\d+[\.]?\d*", data) # Pull the data out of the formatted string
                #print "length is {0}".format(len(values))
                if len(values) != 10:
                    print "Incomplete message"
                else:
                    DataValues[ThisRow] = values
                #print values
                ThisRow += 1
                #for term in data.split('\t'):
                #    values = term.split(':')
                #    #print "{0} = {1}".format(values[0],float(values[1]))
                #print "received message:", data.split("\t")
            except socket.timeout:
                print "Oops. Timed out.  Maybe nobody's home?"

        sys.stdout.flush()
        
        return DataValues


    
    def SendCommand(self):
        # Seems like there ought to be a use for a 'generic' command, but I'm
        # not sure what it is.
        pass
                   
    def __exit__(self, type, value, traceback):
        # Close the UDP Port
        self.StreamControl(False) # Shut down streaming data
        self.sock.close()





from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        #self.start() # Don't start the timer by default.

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
        
        
        
# Usage:
#
#
#
if __name__ == "Not Really":
    from time import sleep
    
    def hello(name):
        print "Hello %s!" % name
    
    print "starting..."
    rt = RepeatedTimer(1, hello, "World") # it auto-starts, no need of rt.start()
    try:
        sleep(5) # your long-running job goes here...
    finally:
        rt.stop() # better in a try/finally block to make sure the program ends!
#
#
#
#
#




        
        
        
        
if __name__ == "__main__":
    
    import time # for the 'sleep' delay timer
    
    # Create an instance of an EddiePlus
    MyEddie = EddiePlus("Edward","192.168.1.109")

    MyEddie.GetPIDS()
    time.sleep(3)
    
    MyEddie.Turn(4)
    time.sleep(3)
    MyEddie.Drive(6)
    time.sleep(2)
    MyEddie.Turn(-4)
    time.sleep(3)
    MyEddie.Drive(-3)
    time.sleep(3)
    
    MyEddie.Disconnect()