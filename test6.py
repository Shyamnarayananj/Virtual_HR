import subprocess 
 
# Command to compile the C++ program 
compile_command = ["g++", "your_program.cpp", "-o", "your_program"] 
 
# Command to execute the compiled program 
run_command = ["./your_program"] 
 
# Compile the C++ program 
compile_process = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
 
# Check if the compilation was successful 
if compile_process.returncode == 0: 
    print("Compilation successful.") 
    # Run the compiled program 
    run_process = subprocess.run(run_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
     
    # Get the output and error messages from the program 
    output = run_process.stdout.decode() 
    error = run_process.stderr.decode() 
     
    # Print the output and error messages 
    print("Output:") 
    print(output) 
     
    print("Error:") 
    print(error) 
else: 
    # Print the compilation error messages 
    print("Compilation failed.") 
    print(compile_process.stderr.decode()) 
