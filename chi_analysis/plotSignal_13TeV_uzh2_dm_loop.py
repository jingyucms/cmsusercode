import os

signalMasses=[1000,1500,1750,2000,2250,2500,3000,3500,4000,4500,5000,6000,7000,8000]
minMass=1900
samples=[]

for signalMass in signalMasses:
  if signalMass==6000:
   mDMs=[1,2990]
  elif signalMass==7000:
   mDMs=[1,4000]
  elif signalMass==8000:
   mDMs=[1,3990]
  else:
   mDMs=[1,3000]
  for mDM in mDMs:
      for nxsec in range(13):
        samples+=[('Axial_Dijet_LO_Mphi',signalMass,mDM,("1p0","1p0"),nxsec),]
        samples+=[('Vector_Dijet_LO_Mphi',signalMass,mDM,("1p5","1p0"),nxsec),]

#print samples

version="Mar5"
count=0

for sample,signalMass,mDM,coupling,nxsec in samples:
  
    samplename=sample+"_"+str(signalMass)+"_"+str(mDM)+"_"+coupling[0]+"_"+coupling[1]+"_"+version
    string="python plotSignal_13TeV_uzh2_dm.py "+samplename+" "+str(nxsec)
    if count%5!=4:
      string+=" &"
    print string
    count+=1
