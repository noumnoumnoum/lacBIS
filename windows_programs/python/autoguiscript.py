import pyautogui
import subprocess
import os
import sys

cmdDirectory = sys.stdin.read().replace("\\", "/").replace("\n","") #use with cd | python <script name>
#print(cmdDirectory)
os.chdir(cmdDirectory)
#screenWidth, screenHeight = pyautogui.size()
print(os.getcwd())
#while 1:
#    x, y = pyautogui.position()
#    print(x, y)
#subprocess.Popen(str(pyautogui.position()), stdout=subprocess.PIPE)