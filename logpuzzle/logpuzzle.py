#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib
import urlparse

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def ksort(url):
  match = re.search(r'-(\w+)-(\w+)\.jpg$', url)
  if match:
    return match.group(2)
  else:
    return url


def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  f = open(filename, 'r')
  file_content = f.read()
  
  image_urls = re.findall('GET\s(.*images/puzzle.*)\sHTTP', file_content)
  
  urls = set()
  for image_url in image_urls:
    urls.add(urlparse.urljoin("http://code.google.com", image_url))
  
  return list(sorted(urls, key=ksort))
  

def download_images(img_urls, todir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  
  print 'Performing download_images to dir = ' + todir
  
  # Create directory if doesn't exist
  if not os.path.exists(todir):
    print 'create dir = ' + todir
    os.makedirs(todir)
  
  image_files = []
  
  for idx, url in enumerate(img_urls):
    print "Retrieving url: " + url
    ufile = urllib.urlopen(url)
    image_file = 'img' + str(idx)
    image_file_wdir = os.path.join(todir, image_file)
    
    # create img file
    ifile = open(image_file_wdir, 'w')
    print "Writing to file " + image_file_wdir
    ifile.write(ufile.read())
    ifile.close()
    image_files.append(image_file)
    
  # Create index.html
  indexfile = open(os.path.join(todir, 'index.html'), 'w')
  indexfile.write('<verbatim/><html><body>')
  for img_url in image_files:
    indexfile.write('<img src="' + img_url + '"/>')
  indexfile.write('</body></html>')
  indexfile.close()

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])
  
  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
