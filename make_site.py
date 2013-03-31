import sys
import shutil
import re
from create_nav import *

first_uppercase = re.compile('[A-Z].*')
header_data = None
footer_data = None

def parse_vars(var_file):
    table = {}
    for line in var_file:
        bits = line.partition("=")
        table[bits[0]] = bits[2].rstrip()
    return table

def gen_header(directory, depth, page, table):
    if header_data:
        for line in header_data:
            if '$' in line:
                bits = line.partition("$")
                new_line = bits[0]
                var_name = bits[2].partition("$")[0]
                print "VAR NAME %s: %s" % (var_name, table[var_name])
                new_line = new_line + "\""
                for i in range(depth):
                    new_line = new_line + "..\\"

                new_line = new_line + table[var_name] + "\""
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

def create_site(source_dir, output_dir, depth, table):
    out_file_name = output_dir + "/index.html"
    page = open(out_file_name, 'w')

    gen_header(source_dir, depth, page, table)
    gen_content(source_dir, depth, page)
    page.write("\t\t\t</div>\n")
    gen_nav_bar(source_dir, depth, page)
    gen_footer(source_dir, depth, page)

    for f in os.listdir(source_dir):
        if os.path.isdir(source_dir + '/' + f):
            if first_uppercase.match(f):
                new_output = output_dir + '/' + f
                os.makedirs(new_output)
                create_site(source_dir + '/' + f, new_output, depth + 1, table)

def print_usage():
    print "Usage: python make_site.py [source_tree_dir] [output_dir]"

if len(sys.argv) < 3:
    print_usage()
else:
    print "WARN: Should be validating input."
    source = sys.argv[1]
    var_f = open(source + "/var.table")
    var_table = parse_vars(var_f)
    header_f = open(source + "/header.html")
    header_data = header_f.readlines()
    footer_f = open(source + "/footer.html")
    footer_data = footer_f.readlines()
#    shutil.copy(source + "/" + style_sheet_name, sys.argv[2] + "/" + style_sheet_name)
    # Copy image file
    create_site(source, sys.argv[2], 0, var_table)
