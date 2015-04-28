'''
This is a script to 'drive' Eddie via keyboard input

*** NOTE ***

This script does not work within the Enthought Canopy environment.
It must be run from the command line via: python EddieDrive.py

It is also currently only operable on Windows, sorry.
'''

# WARNING # - Getch is a Windows only function.  Similar functionality
# is available on Linux/MacOS.
from msvcrt import getch, kbhit


from PyEddiePlus import EddiePlus
import sys
from time import sleep

# This is the IP address for my Eddie, yours will probably be different
MyEddie = EddiePlus("Edward","192.168.1.133")

print "Use a,d,w & x to drive Eddie"
print "Press q to Quit"
print 
sys.stdout.flush()

MaxSpeed = 10
MaxTurn = 6

SpeedVal = 0
TurnVal = 0
KeyPress = 's'

while KeyPress is not "q":
    # Take keyboard input and issue appropriate commands to Eddie

    if kbhit():
        # If a new keystroke is waiting to be read
        KeyPress = getch()
        
        if KeyPress is 'a':
            TurnVal -= 1
        elif KeyPress is 'd':
            TurnVal += 1
        elif KeyPress is 'w':
            SpeedVal += 1
        elif KeyPress is 'x':
            SpeedVal -= 1
        elif KeyPress is 's':
            SpeedVal = 0
            TurnVal = 0
        else:
            # Do nothing
            # Received a character other than an Eddie command
            print "Key Received: {0}".format(KeyPress)
            #pass
    else:
        # Increment Eddie's speed towards zero
        if TurnVal > 0:
            TurnVal = abs(TurnVal) - 1
        elif TurnVal < 0:
            TurnVal = - (abs(TurnVal) - 1)
            
        if SpeedVal > 0:
            SpeedVal = abs(SpeedVal) - 1
        elif SpeedVal < 0:
            SpeedVal = - (abs(SpeedVal) - 1)
    
    # Limit the maximum speed
    if SpeedVal > MaxSpeed:
        SpeedVal = MaxSpeed
    
    if TurnVal > MaxTurn:
        TurnVal = MaxTurn
        
    #print "Turn  = {0}".format(TurnVal)
    #print "Speed = {0}".format(SpeedVal)

    MyEddie.Turn(TurnVal)
    MyEddie.Drive(SpeedVal)
    
    # Go through the loop at about 10Hz
    sleep(.05)

MyEddie.Disconnect()
        
print "Eddie is tired, he needs to rest now."
    


