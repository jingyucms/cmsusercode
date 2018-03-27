from ROOT import RooStats

import os
from ROOT import *
import array

massbinssets1=[[(4800,5400),(5400,6000),(6000,13000)],
	      [(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)],
	      ]
massbinssets2=[[(6000,13000)],
	      [(5400,6000)],
	      [(4800,5400)],
	      [(4200,4800)],
	      [(3600,4200)],
	      [(3000,3600)],
	      [(2400,3000)],
	      ]

for signal,signalMass,massbinsset in [("CIplusLL","12000",massbinssets2),
                                   ("cs_ct14nlo_","13000",massbinssets1),
				   ("AntiCIplusLL","12000",massbinssets2),
				   ("DMAxial_Dijet_LO_Mphi_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_1","6000",""),
				   ]:
  for massbins in massbinsset:
    limits={}
    name="pvalue_LHCa"+signal+"_"+("_".join([s[0:4] for s in str(massbins).strip("[]").split("(")])).strip("_")+"_exp_"+signalMass+"_2016"
    print name
    f1=open(name+".txt")
    observed=0
    for l in f1.readlines():
        if "CLb" in l:
	    pval=float(l.split("=")[1].split("+")[0].strip(" "))
            print "pvalue",pval,"significance",RooStats.PValueToSignificance((1.-pval)/2.)
        if "Significance:" in l:
	    significance=float(l.strip().split(" ")[-1].strip(")"))
            print "significance",significance
