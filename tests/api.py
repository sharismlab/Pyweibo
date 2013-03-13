import os
import fnmatch
import json
# from .context import pyweibo
# from ..lib import Pyweibo

# path="/media/Data/Sites/Pyweibo/out/"

# Resume failed API data extraction
######


def select_from_folder(path):
	files_in_dir = os.listdir( path )
	index=0
	sets=[]

	# Create index from directory
	for f in files_in_dir:
		if os.path.isdir( path+ os.sep+ f ) and fnmatch.fnmatch(f, "post_*"):
			sets.append(f)
			print str(index)+") "+f
			index=index+1

	# Interactive selection
	sel = raw_input( "Input the folder index (0 to "+str(len(sets)-1)+" :" ) 
	folder = sets[int(sel)]
	print "Will now resume fetching for" + path + os.sep+ folder
	return folder


def resume_fetch_data(path, folder):

	# List all existing json files 
	pages=[]

	query=''
	for f in os.listdir( path+os.sep+folder ):
		# Find basic info about post
		if fnmatch.fnmatch(f, "statuses__show_*"):
			print "Original post can be found at = "+ path+os.sep+folder+os.sep+f 
		# RT
		elif fnmatch.fnmatch(f, "RT_*"):
			page = int(f[3:-5])
			pages.append(page)
			query='RT'
		# Comments
		elif fnmatch.fnmatch(f, "coms_*"):
			page = int(f[5:-5])
			pages.append(page)
			print "comments"
			query='coms'
		# Unknown
		else:
			print "directory name seems invalid"

	# Check if already pages inside folder
	if len(pages)==0 or len(pages)==1:
		print ("The folder you selected is empty. No posts fetched.")
	else:
		print str(len(pages))+" pages have already been fetched on a total of "+str(max(page))
		# Ask for confirmation
		pursue = raw_input("Do you want to resume data extraction (y/n)?")
		
		# Go !	
		if pursue == 'y' or pursue == "Y":
			print "let s fetch it"
			
			# Find last comment
			raw = open(path+os.sep+folder+os.sep+query+'_'+str( min(pages) )+".json")
			print str( min(pages) )
			d = json.load(raw);
			since_id=str(d['reposts'][49]['id'])

			# Trigger extraction of  missing posts
			if query=="coms":
				print 'pyWeibo '+query +" since_id "+since_id

			elif query=="RT":
				print 'pyWeibo '+query +" since_id "+since_id
			
		else :
			print 'bye'


# Trigger
my_path="D:\Sites\Pyweibo\out"
my_folder = select_from_folder(my_path)
resume_fetch_data(my_path,my_folder)

# my_folder="post_3534311687371818_130123_185741"
# resume_fetch_data(my_folder)

# Token File
####

# Write token file 
token_file="D:\Sites\Pyweibo\lib\api\access_token.txt"
access_token='''clement.renaud@gmail.com 2.009zcHyB0WnLF5354c35bbd90jxbTS 1516632568'''

