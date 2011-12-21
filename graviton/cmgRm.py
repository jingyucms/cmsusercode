#! /bin/env python
import sys

import CMGTools.Production.eostools as eostools

print "remove",sys.argv[1]
files=eostools.ls(sys.argv[1])
print "listing",files
print "filter",sys.argv[2]
files=[f for f in files if sys.argv[2] in f]
print "removing",files
ok=len(sys.argv)>3
print "ok",ok
if ok:
    eostools.remove( files )
    lfn = eostools.eosToLFN(sys.argv[1])
    eostools.runEOSCommand(lfn,'rmdir','')
