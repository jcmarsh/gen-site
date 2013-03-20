import sys
import re

first_uppercase = re.compile('[A-Z].*')

print "It's website making time Mother Fucker."

def create_site(source_dir, output_dir, depth):
    out_file_name = output_dir + "/index.html"
    page = open(out_file_name, 'w')

    gen_header(source_dir, depth, page)
    gen_content(source_dir, depth, page)
    gen_nav_bar(source_dir, depth, page)
    gen_footer(source_dir, depth, page)

    for f in os.listdir(source_dir):
        if os.path.isdir(source_dir + '/' + f):
            if first_uppercase.match(f):
                create_site(source_dir + '/' + f, output_dir + '/' + f, depth + 1)

def print_usage():
    print "WARN: James is a lazy programmer"

if len(sys.argv) < 3:
    print_usage()
else:
    print "WARN: Should be validating input."
    create_site(sys.argv[1], sys.argv[2], 0)
