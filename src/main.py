#!/usr/bin/env python

from optparse import OptionParser


desc="""

    PyWeibo is a crawler and visualization tool for Sina Weibo

"""

def main():
    parser = OptionParser(usage="usage: %prog URL [-a 'action'] [options] ",
                          version="%prog 0.1", description=desc)
    
    parser.add_option('-a', "--action", 
                      help='Select a way to process the data', 
                      dest='action', 
                      action='store',
                      metavar='<map/graph/tag/feel>')

    parser.add_option("-o", "--outputfile",
                      action="store", # optional because action defaults to "store"
                      dest="outputfile",
                      default="./out/graph",
                      help="file to write graph info. Default: '%default'",
                      metavar='<FILENAME>')

    parser.add_option("-d", "--database",
                      action="store_true",
                      dest="db",
                      default=False,
                      help="select between MongoDB and Redis to store raw data")

    parser.add_option("-g", "--graph",
                      action="store", # optional because action defaults to "store"
                      dest="graphtype",
                      default="dot",
                      help="chose Graph file type: .dot or .gdf (for Gephi). Default: .%default",
                      metavar='<graphtype>')

    
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("wrong number of arguments")

    if options.action is None:
        parser.error("You have to chose an action to start crawling data \n")
        parser.print_help()

    print options
    print args

if __name__ == '__main__':
    main()