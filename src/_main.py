#!/usr/bin/env python
# -*- coding: utf-8 -*-#

"""
PyWeibo is a crawler and visualization tool for Sina Weibo

Usage 
    
    pyweibo.py <map/graph/tag/feel> <url> -d <db_type> -f <outputfile> -e <filetype>

Commands:

    pyweibo map YOUR_POST_URL (create a map of reposts from a post URL)
    pyweibo graph YOUR_PROFILE_URL (create a social graph from a user profile)
    pyweibo tag YOUR_POST_URL (create tag list from a post comments using text analysis)
    pyweibo feel YOUR_POST_URL (create report from a post comments using sentiment analysis)

Options :

    -d (redis/mongo) : chose storage option. You can use Redis or MongoDB (see settings.py)
    -f "filename" "filetype" : store to file
    -ext (dot/gdf) : chose file type. You can generate a .dot file or a .gdf graph file for Gephi
    
    


"""

import os
import sys
import getopt

from optparse import OptionParser


def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print __doc__
            sys.exit(0)

        elif opt in ("-f", "--file"):
         outfile = arg
         print 'Results will be written in '+outfile

        elif opt in ("-d", "--database"):
         db = arg
         print 'Data will be stored in '+db

        elif opt in ("-e", "--extension"):
         filetype = arg
         print 'Graph will be encoded using '+filetype

    # process arguments
    # for arg in args:
    #     print '==================================='
    #     print arg

if __name__ == "__main__":
    main()