from ROOT import RooStats

import os
from ROOT import *
import array

massbinssets=[[(4200,8000)],
	      [(3600,4200)],
	      [(3000,3600)],
	      [(2400,3000)],
	      [(1900,2400)],
              [(3600,4200),(4200,8000)],
	      [(3000,3600),(3600,4200),(4200,8000)],
	      [(2400,3000),(3000,3600),(3600,4200),(4200,8000)],
	      [(1900,2400),(2400,3000),(3000,3600),(3600,4200),(4200,8000)],
	      ]

for signal,signalMass in [("ADLOCI","11000"),("DLOCI","10000"),("EWK","0")]:
  for massbins in massbinssets:
    if massbins==[(3000,3600),(3600,4200),(4200,8000)] and signal!="DLOCI": continue
    limits={}
    name="pvalue_"+signal+"_"+("_".join([s[0:4] for s in str(massbins).strip("[]").split("(")])).strip("_")+"_"+signalMass
    print name
    f1=open(name+".txt")
    observed=0
    for l in f1.readlines():
        if "CLb" in l:
	    pval=float(l.split("=")[1].split("+")[0].strip(" "))
            print "pvalue",pval,"significance",RooStats.PValueToSignificance((1.-pval)/2.)
