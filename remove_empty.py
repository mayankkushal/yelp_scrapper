import os
import sys
"""
Removes all the files which are empty. Just need to give the location, ie. the name of the folder in the `path`
"""

path = sys.argv[1]
for filename in os.listdir(path):
	print(filename)
	new_path = path+"/"+filename
	if os.path.getsize(new_path) == 0:
		os.remove(new_path)