fname="even2.c"
ff=open("static/path.txt","r")
path=ff.read()
ff.close()

    
#ff=open(path+"/"+fname,"w")
#ff.write(ccode)
#ff.close()

result = ""
with open(path+"/"+fname, "r+") as file:
    result += "".join(line for line in file if not line.isspace())
    file.seek(0)
    file.write(result)

print(result)
