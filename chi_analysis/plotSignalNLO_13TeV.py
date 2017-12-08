samples=[
             ("ll_ct14lo_LL+_10000",[]),
             ("ll_ct14lo_LL-_10000",[]),
             ("ll_ct14nlo_LL+_10000",[]),
             ("ll_ct14nlo_LL-_10000",[]),
             ]

for m in range(5,31):
       samples+=[("cs_ct14nlo_"+str(m*1000)+"_LL+",[]),
               ("cs_ct14nlo_"+str(m*1000)+"_LL-",[]),
               ("cs_ct14nlo_"+str(m*1000)+"_RR+",[]),
               ("cs_ct14nlo_"+str(m*1000)+"_RR-",[]),
               ("cs_ct14nlo_"+str(m*1000)+"_VV+",[]),
               ("cs_ct14nlo_"+str(m*1000)+"_VV-",[]),
               ("cs_ct14nlo_"+str(m*1000)+"_AA+",[]),
               ("cs_ct14nlo_"+str(m*1000)+"_AA-",[]),
               ("cs_ct14nlo_"+str(m*1000)+"_V-A+",[]),
               ("cs_ct14nlo_"+str(m*1000)+"_V-A-",[]),
               ]

import os

for sample,l in samples:
  os.system("cp datacard_shapelimit13TeV_QCD_chi.root datacard_shapelimit13TeV_"+sample+"_chi.root")
