import os
import subprocess 

#os.getenv("PATH=C:\Program Files (x86)\Dev-Cpp\MinGW64\bin");
a=subprocess.call(["g++", "static/program/hello_world.cpp"]) 
#tmp=subprocess.call("./a.out") 
#print("printing result")
print(a) 
