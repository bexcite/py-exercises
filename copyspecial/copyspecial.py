#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them

def findspecialfiles(dir):
  filenames = os.listdir(dir)
  special_pattern = re.compile(r'__\w+__')
  result = []
  for filename in filenames:
    print 'filename to evaluate = ' + filename
    if special_pattern.search(filename):
      print 'special pattern!'
      result.append(os.path.abspath(filename))
      
  return result
  
def copyspecialfiles(specialfiles, todir):
  print 'Dir to copy = ' + todir
  print 'Special files to copy = ' + str(specialfiles)
  
  # Create directory if doesn't exist
  if not os.path.exists(todir):
    print 'create dir = ' + todir
    os.makedirs(todir)
    
  # Copy special files to dir
  for specialfile in specialfiles:
    print 'Copying ... ' + specialfile
    shutil.copy(specialfile, todir)
    
def tozipspecialfiles(specialfiles, tozip):
  print "We are going to zip files to " + tozip
  cmd = 'zip -j %s %s' % (tozip, ' '.join(specialfiles))
  print 'Going to execute command: ' + cmd
  (status, output) = commands.getstatusoutput(cmd)
  if status != 0:
    sys.stderr.write('Something bad happened ...' + output)
    sys.exit(1)
  print output

def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)
  
  # iterate over all dir arguments  
  for dir in args:
    specialfiles = findspecialfiles(dir)
    if len(todir) > 0:
      copyspecialfiles(specialfiles, todir)
    if len(tozip) > 0:
      tozipspecialfiles(specialfiles, tozip)
    
  # +++your code here+++
  # Call your functions
  
  
if __name__ == "__main__":
  main()
