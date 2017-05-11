import os,sys
from ROOT import *
import array
import ROOT


VectorDM=False
AxialDM=True

models=[]

gas=["0p01","0p05","0p1","0p2","0p25","0p3","0p5","0p75","1","1p5","2p0","2p5","3p0"]
gvs=["0p01","0p05","0p1","0p2","0p25","0p3","0p5","0p75","1","1p5","2p0","2p5","3p0"]

if VectorDM:
  counter=100
  signalName={}
  signalExtraName={}
  for mdm in ["1","3000"]:
    for gv in gvs:
      models+=[counter]
      signalName[counter]="DMVector_Dijet_LO_Mphi"
      signalExtraName[counter]="_"+mdm+"_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_"+gv+"_ga_0"
      if not gv==gvs[-1]:
        print "python calculate_limit_shape_13TeV_2016.py "+str(counter)+" >& log"+str(counter)+" &"
      else:
        print "python calculate_limit_shape_13TeV_2016.py "+str(counter)
      counter+=1

if AxialDM:
  counter=1100
  signalName={}
  signalExtraName={}
  for mdm in ["1","3000"]:
    for ga in gas:
      models+=[counter]
      signalName[counter]="DMAxial_Dijet_LO_Mphi"
      signalExtraName[counter]="_"+mdm+"_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_"+ga
      if not ga==gas[-1]:
        print "python calculate_limit_shape_13TeV_2016.py "+str(counter)+" >& log"+str(counter)+" &"
      else:
        print "python calculate_limit_shape_13TeV_2016.py "+str(counter)
      counter+=1


print models
#print signalName
print signalExtraName
