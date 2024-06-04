import subprocess
import re
def run_with_timeout(timeout):
    # Define the path to the instance file
    path_to_instance = r"..\..\Documents\GitHub\Timetabling-problem\encoding.wcnf"

    # Define the shell command
    command = r"cd ..\..\..\Pumpkin\pumpkin-private && target\release\pumpkin-cli.exe -t " + str(timeout) + " " + path_to_instance

    # Specify the starting directory for the command
    starting_directory = r"C:"

    # Execute the command and capture its output line by line
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True, cwd="C:")
    number = None
    #print(process.stdout.read())
    for line in process.stdout:
        # Find the last occurrence of "o" followed by a space and capture the number after it
       match = re.search(r"o (\d+)", line)
       #print(line)
       if match:
           #print("matched")
           # Extract the captured number
           number = match.group(1)
    return number
print(run_with_timeout(100000))