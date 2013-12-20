import sys
import os
import re

leading_number = re.compile('[0-9][0-9].*') # Introduces a limit of 100 (0 - 99) pages on the navigation bar. I'm okay with that.

def sub_nav_bar(folder, page):
    dir_names = []
    anchor_names = []
    for f in os.listdir(folder):
        if os.path.isdir(folder + '/' + f):
            if leading_number.match(f):
                dir_names.append(f)
#            else:
#                anchor_names.append(f)
#    dir_names.sort()
#    anchor_names.sort()

    page.write("\t\t<UL>\n")
    for n in dir_names:
        page.write("\t\t\t<LI><A href=\"" + n + "/index.html\">" + n + "</A></LI>\n")
#    for a in anchor_names:
#        page.write("\t\t\t<LI><A href=\"#" + a + "\">" + a + "</A></LI>\n")
    page.write("\t\t</UL>\n")


def gen_nav_bar(folder, depth, page):
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
            if leading_number.match(f):                
                dir_names.append(f)
    dir_names.sort()

    page.write("<div class=\"nav_bar\">\n")
    page.write("\t<UL>\n")
    page.write("\t\t<LI><A href=\"" + pre + "index.html\">Home</A></LI>\n")
    for n in dir_names:
        # [3:] Cuts out the begining "00_" from n
        page.write("\t\t<LI><A href=\"" + pre + n[3:] + "/index.html\">" + n[3:] + "</A></LI>\n")
        if n == base:
            sub_nav_bar(top_level + '/' + base, page)
    page.write("\t</UL>\n")
    page.write("</div>\n")
