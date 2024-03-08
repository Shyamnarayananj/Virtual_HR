import subprocess

result = subprocess.run(["python", "test4.py"], capture_output=True, text=True)

print(result.stdout)
