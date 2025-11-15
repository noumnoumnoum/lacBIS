@echo off
echo Welcome to batch scripting!
mkdir C:\LabDirectory
echo This is a test file. >C:\LabDirectory\testfile.txt
copy C:\LabDirectory\testfile.txt C:\LabDirectory\copiedfile.txt
echo Here are the files in C:\LabDirectory:
dir C:\LabDirectory
pause 
