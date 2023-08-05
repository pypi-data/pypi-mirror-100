##  Created by Jim Sadlek
##  Copyright © 2021 VMware, Inc. All rights reserved.
##
import xml.dom.minidom
import sys
import os.path
import argparse

Description = """
This script parses code from vRO Workflow XML that contain embedded Scriptable Tasks.
By: Jim Sadlek - VMware, Inc.

This must be run from the vRO Package's top-level folder, which contains a 'workflows/src/main/resources/Workflow' subfolder.
This script traverses all sub folders of the above and stores embedded code in a '.parsevro' folder.
This is usually run after a 'mvn vro:pull' command when using vRealize Build Tools, or exporting to a folder with native vRO.
"""
parser = argparse.ArgumentParser(description=Description,formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-v','--verbose',action='store_true',help='Display verbose logging output')
args = parser.parse_args()

#####################################
## parse xml scriptable task elements 
## and save resulting program code
## as discrete files in the form: <path>/.parsevro/<wfName>_<taskName>_<displayName>.js
def parseJS(xmlfile):
  dirName = os.path.dirname(xmlfile)
  wfName = os.path.splitext(os.path.basename(xmlfile))[0]
  subDirName = "%s/.parsevro" % (dirName)
  #print("wfName:%s"%wfName)

  # use the parse() function to load and parse an XML file
  doc = xml.dom.minidom.parse(xmlfile)
  
  # get a list of XML tags from the document and print each one
  wfItems = doc.getElementsByTagName("workflow-item")
  if args.verbose: print("%d workflow-item(s): (not all are Scriptable Tasks)" % wfItems.length)

  for wfItem in wfItems:
    typeAttr = wfItem.getAttribute("type")
    #print("type: %s" % typeAttr)
    if typeAttr == "task":
      taskName = wfItem.getAttribute("name")
      if args.verbose: print("\ttaskName: %s" % taskName)

      displayNameItem = wfItem.getElementsByTagName("display-name")[0]
      for node in displayNameItem.childNodes:
        displayName = node.data
        if args.verbose: print("\tdisplay-name: %s" % displayName)

      for scriptItem in wfItem.getElementsByTagName("script"):
        for node in scriptItem.childNodes:
          script = node.data
          #print("\nscript: \n%s" % script)

      fileName = "%s/%s_%s_%s.js" % (subDirName, wfName, taskName, displayName)
      if args.verbose: print("\tScript exported to fileName:\n\t%s" % fileName)

      # Fix for TKTVSDL-388
      # check for file names in absolute file path form
      prefix = is_filename_safe(subDirName, fileName)
      if prefix == subDirName:
        try:
          with open(fileName,"w+") as f:
            f.write(script)

        except IOError:
          print ("Error: creating file: ", fileName)


#####################################
## provided by vSDL Service Desk team
## TKTVSDL-388
def is_filename_safe(dirName, fileName):
    if not dirName.endswith('/'):
        dirName += '/'
    abs_dirname = os.path.abspath(dirName)
    abs_filename = os.path.abspath(fileName)
    return os.path.commonprefix([abs_dirname,abs_filename])

#########################
## rm all files in folder
def clearFiles(path):
  for root, dirs, files in os.walk(path):
    for file in files:
        os.remove(os.path.join(root, file))


##############################
## create sub folder to contain 
## parsed code files, or
## clear sub folder before
## adding parsed code files
def createOrClearParseFolder(dirName):
    subDirName = "%s/.parsevro" % (dirName)
    #print("subdirName: ",subDirName)
    if not os.path.isdir(subDirName):
      #print("make subDirName")
      os.makedirs(subDirName)
    else:
      #print("clearFiles")
      clearFiles(subDirName)



###########
## main
def main():
  rootDir = './workflows/src/main/resources/Workflow'
  rootDir = os.path.abspath(rootDir)
  
  if not os.path.isdir(rootDir):
    print("Looking for XML files in %s"%rootDir)
    print("Are you in the right location?  CD to the top leve of a 'mixed' project that contains the %s sub folder structure."%rootDir)
    exit

  print("Parsing vRO Workflows ...")
  
  for dirName, subdirList, fileList in os.walk(rootDir):

    if os.path.basename(dirName) == ".parsevro":
      continue
    
    if len(fileList) > 0:
      createOrClearParseFolder(dirName)

      for filename in fileList:
        if filename.endswith(".xml"):
          if args.verbose: print("\n*** PROCESSING Workflow XML filename: %s"%filename)  
          parseJS(dirName+"/"+filename)


#if __name__ == "__main__":
#  main()