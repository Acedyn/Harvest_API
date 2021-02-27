import os, sys, getopt

# Get the root path to the current file
basepath = os.path.dirname(__file__)

# Get aguments
argv = sys.argv[1:]
opts, args = getopt.getopt(argv, "e:d:")

command_args = ""

# Gather all the passed arguments
for opt, arg in opts:
    command_args += opt + " " + arg + " "

# Run the app.py file with all the arguments
os.system("python \"" + str(os.path.join(basepath, "app.py")) + "\" " + command_args)

