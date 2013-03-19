import sys
import os
import re

first_uppercase = re.compile('[A-Z].*')

def sub_nav_bar(folder):
    dir_names = []
    anchor_names = []
    for f in os.listdir(folder):
        if os.path.isdir(folder + '/' + f):
            if first_uppercase.match(f):
                dir_names.append(f)
            else:
                anchor_names.append(f)
    dir_names.sort()
    anchor_names.sort()

    print "\t\t<UL>"
    for n in dir_names:
        print "\t\t\t<LI><A href=\"" + n + "/index.html\">" + n + "</A></LI>"
    for a in anchor_names:
        print "\t\t\t<LI><A href=\"#" + a + "\">" + a + "</A></LI>"
    print "\t\t</UL>"


def nav_bar(folder, depth):
    print "WARN: Should use a non-platform specific delimeter"

    
    pre = ""
    base = ""
    top_level = os.path.abspath(folder)
    print top_level
    for x in range(depth):
        pre = pre + "../"
        base = os.path.basename(top_level)
        top_level = os.path.dirname(top_level)
        print "base: " + base

    print "top-level: " + top_level

    dir_names = []
    for f in os.listdir(top_level):
        if os.path.isdir(top_level + '/' + f):
            if first_uppercase.match(f):
                dir_names.append(f)
    dir_names.sort()

    print "<div class=\"nav_bar\">"
    print "\t<UL>"
    print "\t\t<LI><A href=\"" + pre + "index.html\">Home</A></LI>"
    for n in dir_names:
        print "\t\t<LI><A href=\"" + pre + n + "/index.html\">" + n + "</A></LI>"
        if n == base:
            sub_nav_bar(top_level + '/' + base)
    print "\t</UL>"
    print "</div>"

def print_usage():
    print "WARN: James is a lazy programmer"


if len(sys.argv) < 2:
    print_usage()
else:
    print "WARN: Should be validating input."
    nav_bar(sys.argv[1], 1)
