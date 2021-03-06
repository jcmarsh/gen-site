import sys
import shutil
import re
from create_nav import *

leading_number = re.compile('[0-9][0-9].*')
header_data = None
footer_data = None

def parse_vars(var_file):
    table = {}
    for line in var_file:
        bits = line.partition("=")
        table[bits[0]] = bits[2].rstrip()
    return table

# Recursive check to handle multiple variables in a line.
def replace_var(line, table):
    if '$' in line: # TODO: Should be able to handle multiple vars
        bits = line.partition("$")
        new_line = bits[0]
        var_name = bits[2].partition("$")[0]
        new_line = new_line + table[var_name]
        return new_line + replace_var(bits[2].partition("$")[2], table)
    else:
        return line
        
def gen_header(directory, page, table):
    if header_data:
        for line in header_data:
            page.write(replace_var(line, table))
    else:
        page.write("HEADER\n")

def gen_content(directory, page):
    content_f = open(directory + "/content.html")
    if content_f:
        for line in content_f:
            page.write(line)
        content_f.close()
    else:
        page.write("CONTENT\n")

def gen_footer(directory, page):
    if footer_data:
        for line in footer_data:
            page.write(line)
    else:
        page.write("FOOTER\n")

def copy_dir_contents(source_dir, output_dir):
    for f in os.listdir(source_dir):
        if os.path.isdir(source_dir + '/' + f):
            new_output = output_dir + '/' + f
            os.makedirs(new_output)
            copy_dir_contents(source_dir + '/' + f, new_output)
        else:
            shutil.copy(source_dir + '/' + f, output_dir + '/' + f)

def create_site(source_dir, output_dir, depth, table):
    out_file_name = output_dir + "/index.html"
    page = open(out_file_name, 'w')

    # insert _relative to table
    relative = ""
    for i in range(depth):
        relative = relative + "../"
    table['_relative'] = relative

    gen_header(source_dir, page, table)
    gen_content(source_dir, page)
    page.write("\t\t\t</div>\n")
    gen_nav_bar(source_dir, depth, page)
    gen_footer(source_dir, page)

    for f in os.listdir(source_dir):
        if os.path.isdir(source_dir + '/' + f):
            if leading_number.match(f):
                new_output = output_dir + '/' + f[3:] # Strip leading "##_"
                os.makedirs(new_output)
                create_site(source_dir + '/' + f, new_output, depth + 1, table)
            else: # Is a directory that should be copied over, but without a page made
                new_output = output_dir + '/' + f
                os.makedirs(new_output)
                copy_dir_contents(source_dir + '/' + f, new_output)
        else: # Is a file that may need to be copied?
            shutil.copy(source_dir + '/' + f, output_dir + '/' + f)

def print_usage():
    print "Usage: python make_site.py [source_tree_dir] [output_dir]"

if len(sys.argv) < 3:
    print_usage()
else:
    print "WARN: Should be validating input."
    source = sys.argv[1]
    var_f = open(source + "/var.table")
    var_table = parse_vars(var_f)
    var_f.close()
    header_f = open(source + "/header.html")
    header_data = header_f.readlines()
    header_f.close()
    footer_f = open(source + "/footer.html")
    footer_data = footer_f.readlines()
    footer_f.close()

    # Copy over stylesheet
    if var_table["style_sheet"]:
        shutil.copy(source + "/" + var_table["style_sheet"], sys.argv[2] + "/" + var_table["style_sheet"])
    else:
        print "No style sheet detected (in var.table as 'style_sheet=[name]')"

    create_site(source, sys.argv[2], 0, var_table)
