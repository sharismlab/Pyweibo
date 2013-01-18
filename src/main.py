#!/usr/bin/env python

from argparse import ArgumentParser
import Pyweibo



def main():
    desc ="PyWeibo is a crawler and visualization tool for Sina Weibo"
    usage="""
        pyweibo URL [-a 'action'] [options] 
        """
    parser = ArgumentParser(usage=usage, version=" 0.1", description=desc)
    
    parser.add_argument('-a', "--action", 
                      help='Select a way to process the data', 
                      dest='action', 
                      action='store',
                      metavar='<map/graph/tag/feel>',
                      required=True)

    parser.add_argument("-o", "--outputfile",
                      action="store", # optional because action defaults to "store"
                      dest="outputfile",
                      default="./out/graph",
                      help="file to write graph info. Default: './out/graph'",
                      metavar='<FILENAME>')

    parser.add_argument("-d", "--database",
                      action="store_true",
                      dest="db",
                      default=False,
                      help="select between MongoDB and Redis to store raw data")

    parser.add_argument("-g", "--graph",
                      action="store", # optional because action defaults to "store"
                      dest="graphtype",
                      default="dot",
                      help="chose Graph file type: .dot or .gdf (for Gephi). Default: .dot",
                      metavar='<graphtype>')

    args = parser.parse_args()

    # if args != 1:
    #     parser.error("wrong number of arguments")

    # if args.action is None:
    #     parser.error("You have to chose an action to start crawling data \n")
    #     parser.print_help()

    print args

if __name__ == '__main__':
    main()


