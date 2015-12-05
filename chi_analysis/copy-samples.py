import os
di="/pnfs/psi.ch/cms/trivcat/store/user/hinzmann/dijet_angular"
samples=os.listdir(di)

i=0

for sample in samples:
 if "Nov28" in sample and "herwig" in sample:
  command="gfal-copy srm://t3se01.psi.ch"+di+"/"+sample+"/GEN.root srm://srm-eoscms.cern.ch//eos/cms/store/cmst3/user/hinzmann/dijet_angular/"+sample+".root"
  if i%4!=3:command+="&"
  print command
  i+=1

qwe

di="/pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/Wtagging"
samples=os.listdir(di)

for sample in samples:
  if "QCD_Pt_" in sample:
    command="gfal-copy srm://t3se01.psi.ch"+di+"/"+sample+" srm://srm-eoscms.cern.ch//eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCDnew/"+sample
    if i%5!=4:command+="&"
    print command
    i+=1
