
import os
import sys
os.putenv("PATH","PATH=C:\Program Files (x86)\Dev-Cpp\MinGW64\bin")


#exec("g++ hello.c -o hello.exe")
answer=exec("hello.c")
runcmd = "./a.out > output.txt"

