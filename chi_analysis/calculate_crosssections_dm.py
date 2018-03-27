import os

if __name__ == '__main__':

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
        samples+=[('Axial_Dijet_LO_Mphi',signalMass,mDM,("1p0","1p0")),]
        samples+=[('Vector_Dijet_LO_Mphi',signalMass,mDM,("1p5","1p0")),]

 print samples

 version="Mar5"

 for sample,signalMass,mDM,coupling in samples:
  
  numjobs=3

  for jobnum in range(2,numjobs):

    samplename=sample+"_"+str(signalMass)+"_"+str(mDM)+"_"+coupling[0]+"_"+coupling[1]+"_"+version

    crosssections={}
    f=file("/mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_1_25_patch3/src/cmsusercode/"+samplename+str(jobnum)+".log")
    for l in f.readlines():
      if "Total" in l:
        crosssections[samplename]=float(l.split("+/")[0].rstrip().split("	")[-1])
        break

print crosssections
fout=file("xsecs_13TeV_dm_2016.txt","w")
fout.write(str(crosssections))
fout.close()
