import os
for mass in [1000,1250,1500,2000,2500,3000,3500,4000,5000,6000,7000]:
  for gq in ["0.05","0.1","0.25","0.5","1.0","1.5","2.0","2.5","3.0","3.5","4.0"]:
   for vector in ["800","801"]:
     print "python plotSignal_13TeV_lxplus.py "+str(mass)+"_1_"+gq+"_"+vector+" &"