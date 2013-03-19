import sys
import os

def nav_bar(path):
    for f in os.listdir(path):
        print f

def print_usage():
    print "WARN: James is a lazy programmer"


if len(sys.argv) < 2:
    print_usage()
else:
    print "WARN: Should be validating input."
    nav_bar(sys.argv[1])
