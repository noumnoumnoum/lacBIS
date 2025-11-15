@echo off & REM this is not necessary, and if anything it makes troubleshooting more difficult. I include it as a loose nod to convention, so that I am technically not *completely* ignoring it.
set /a var=1
type nul > liveaddresses.txt
:start
set /a var+=1
echo Testing 10.10.0.%var%
type nul > temp.txt
ping 10.10.0.%var% -n 1 -w 150 | find "TTL" > temp.txt
echo x>> temp.txt
set /p reply=<temp.txt
if "%reply%" NEQ "x" arp -a | find "%var% " >>liveaddresses.txt & arp -a | find "%var%"
if %var% EQU 255 goto exit
goto start
:exit
type liveaddresses.txt
goto end

"""
*ahem* pseudocode time
set a number. starts at 2, goes up to 254
then, ping 10.0.0.<number>, outputting the contents to a text file in Desktop/blanchfolder/whothefuckisnmap

as a text file, because I don't respect other file types. .txt is love, .txt is life.

I could leave that code alone and check it all later, or I could parse the text file immediately after creation and delete it if the text file contains the phrase
"." fuck I forget the phrase, but basically if I pinged a dead IP then delete the text file.

I am like, 99% sure that this is just a worse version of nmap, but I don't care enough to download it. so yeah.


UPDATE: I have changed how this code works significantly, and I do not care to explain it. For what it's worth, I tried to make it readable.
UPDATE 2: Due to how the network is set up, I don't think it's even possible to do what I'm trying to do. I'll run it by one of the instructors. End of diary /s.
UPDATE 3: it works. docstring subject to rewrite. many features have been added and changed.
"""
type nul > temp.txt
:end