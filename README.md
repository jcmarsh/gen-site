gen-site
========

Create a simple webpage from a directory structure and content files.

This is experimental, and does not work well.

To create a website:
 * run `python make_site.py source_folder destination_folder`

The system make a large number of assumptions.
* Every page will have the same header and footer.
* The navigation frame is create by create_nav.py and is based off of the source folders directory structure:
 * Each folder becomes a top level item.
 * TODO: This functionality is not yet fully implemented / decided upon.
* The main pane for each page comes from a "content.html" file.

Additionally, var.table holds a set of string substitutions to be made when the content file is parsed.


