import pyautogui
import subprocess
import os
import sys

#cmdDirectory = sys.stdin.read().replace("\\", "/").replace("\n","") #use with cd | python <script name>
#print(cmdDirectory)
#os.chdir(cmdDirectory)
#screenWidth, screenHeight = pyautogui.size()
#print(os.getcwd())

#this code is a mess. there's literally more commented out lines than lines of actual code.
#I changed my mind about how it should work like, 4 times while writing it. and yet, it is now perfect.


#while 1 because this is intended to be used to prepare mouse positions for another pyautogui script, for automating mouse inputs.
#usually I record the mouse positions by hand, although you could set up a text file to record inputs into a text file.
#if you can't afford a pen
while 1:
    x, y = pyautogui.position()
    print(x, y)

#subprocess.Popen(str(pyautogui.position()), stdout=subprocess.PIPE) #yeah this failed entirely. I don't even care enough to try to fix it.
#the original idea was to get the mouse position with pyautogui.position() then pipe it to the echo command (python cursor_position.py | echo)...
#but I couldn't figure out how to get python to output the way I wanted. which is fine for now, since print works just like echo.
#still. I'll need to figure out that capability eventually.