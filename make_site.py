import sys
import shutil
import re
from create_nav import *

first_uppercase = re.compile('[A-Z].*')
header_data = None
footer_data = None
# TODO: Eventually should have a variable definition table... but too complex for now
style_sheet_name = "style.css"

print "It's website making time Mother Fucker."

def gen_header(directory, depth, page):
    if header_data:
        for line in header_data:
            if '$' in line:
                bits = line.partition("$")
                new_line = bits[0]
                new_line = new_line + "\""
                for i in range(depth):
                    new_line = new_line + "..\\"

                new_line = new_line + style_sheet_name + "\""
                new_line = new_line + bits[2].partition("$")[2]

                page.write(new_line)
            else:
                page.write(line)
    else:
        page.write("HEADER\n")

def gen_content(directory, depth, page):
    content_f = open(directory + "/content.html")
    if content_f:
        for line in content_f:
            page.write(line)
    else:
        page.write("CONTENT\n")

def gen_footer(directory, depth, page):
    if footer_data:
        for line in footer_data:
            page.write(line)
    else:
        page.write("FOOTER\n")

def create_site(source_dir, output_dir, depth):
    out_file_name = output_dir + "/index.html"
    page = open(out_file_name, 'w')

    gen_header(source_dir, depth, page)
    gen_content(source_dir, depth, page)
    page.write("\t\t\t</div>\n")
    gen_nav_bar(source_dir, depth, page)
    gen_footer(source_dir, depth, page)

    for f in os.listdir(source_dir):
        if os.path.isdir(source_dir + '/' + f):
            if first_uppercase.match(f):
                new_output = output_dir + '/' + f
                os.makedirs(new_output)
                create_site(source_dir + '/' + f, new_output, depth + 1)

def print_usage():
    print "Usage: python make_site.py [source_tree_dir] [output_dir]"

if len(sys.argv) < 3:
    print_usage()
else:
    print "WARN: Should be validating input."
    source = sys.argv[1]
    header_f = open(source + "/header.html")
    header_data = header_f.readlines()
    footer_f = open(source + "/footer.html")
    footer_data = footer_f.readlines()
    shutil.copy(source + "/" + style_sheet_name, sys.argv[2] + "/" + style_sheet_name)
    create_site(source, sys.argv[2], 0)
