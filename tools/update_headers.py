﻿# -*- coding: utf-8 -*-
# find and replace in a dir by multiple pairs of regex

import os, sys,shutil,re

mydir = sys.argv[1]

x3dom_includes = '''
<link rel="stylesheet" type="text/css" href="../../src/x3dom.css" />
<script type="text/javascript" src="../../src/lang/Array.js"></script>
<script type="text/javascript" src="../../src/x3dom-internals.js"></script>
<script type="text/javascript" src="../../src/x3dmain.js"></script>
<script type="text/javascript" src="../../src/debug.js"></script>
<script type="text/javascript" src="../../src/gfx_webgl.js"></script>
<script type="text/javascript" src="../../src/gfx_flash.js"></script>
<script type="text/javascript" src="../../src/x3d.js"></script>
<script type="text/javascript" src="../../src/x3d_document.js"></script>
<script type="text/javascript" src="../../src/MatrixMixer.js"></script>
<script type="text/javascript" src="../../src/x3d_viewarea.js"></script>
<script type="text/javascript" src="../../src/mesh.js"></script>
<script type="text/javascript" src="../../src/fields.js"></script>
<script type="text/javascript" src="../../src/x3d_follower.js"></script>
'''

findreplace = [
	(re.compile(
		ur'<!-- BEGIN:X3DOM -->.*<!-- END:X3DOM -->',re.U|re.M|re.DOTALL), 
		ur'<!-- BEGIN:X3DOM -->' + x3dom_includes + '<!-- END:X3DOM -->'
	),
]


def replaceStringInFile(filePath):
   "replaces all string by a regex substitution"
   backupName=filePath+'~backup~'

   print 'reading:', filePath
   input = open(filePath,'rb')
   s=unicode(input.read(),'utf-8')
   input.close()

   numRep=None
   for couple in findreplace:
      if numRep == None:
         numRep = re.search(couple[0],s)
      outtext = re.sub(couple[0],couple[1], s)
      s=outtext

   if numRep:
      print ' writing:', filePath
      shutil.copy2(filePath, backupName)
      outF = open(filePath,'r+b')
      outF.read() # we do this way to preserve file creation date
      outF.seek(0)
      outF.write(outtext.encode('utf-8'))
      outF.truncate()
      outF.close()

def myfun(dummy, curdir, filess):
   for child in filess:
      if re.search(r'.*\.html|xhtml$',child,re.U) and os.path.isfile(curdir+'/'+child):
         replaceStringInFile(curdir+'/'+child)

os.path.walk(mydir, myfun, 3)