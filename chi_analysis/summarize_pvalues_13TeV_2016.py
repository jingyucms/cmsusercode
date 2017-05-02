from ROOT import RooStats

import os
from ROOT import *
import array

massbinssets=[[(6000,13000)],
	      [(5400,6000)],
	      [(4800,5400)],
	      [(4200,4800)],
	      [(3600,4200)],
	      [(3000,3600)],
	      [(2400,3000)],
	      [(4800,5400),(5400,6000),(6000,13000)],
	      [(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)],
	      ]

for signal,signalMass in [("CIplusLL","12000"),("cs_ct14nlo_","13000"),("AntiCIplusLL","12000")]:
  for massbins in massbinssets:
    if signal=="cs_ct14nlo_" and len(massbins)==1: continue
    if signal!="cs_ct14nlo_" and len(massbins)>1: continue
    limits={}
    name="pvalue_TEV"+signal+"_"+("_".join([s[0:4] for s in str(massbins).strip("[]").split("(")])).strip("_")+"_exp_"+signalMass+"_2016"
    print name
    f1=open(name+".txt")
    observed=0
    for l in f1.readlines():
        if "CLb" in l:
	    pval=float(l.split("=")[1].split("+")[0].strip(" "))
            print "pvalue",pval,"significance",RooStats.PValueToSignificance((1.-pval)/2.)
