from ROOT import *
from array import array
import os

def writeHistogram(name,points):
   chi_binning=array('d')
   for i in range(len(points)):
       chi_binning.append(points[i][0])
   chi_binning.append(points[len(points)-1][1])
   histogram=TH1F(name,name,len(chi_binning)-1,chi_binning)
   #histogram.Sumw2()
   for i in range(len(points)):
       histogram.Fill(points[i][0]+(points[i][1]-points[i][0])/2,points[i][2])
   histogram.Write()

if __name__=="__main__":
    paths=[("fnl5622i_v23"),
          ]
    for path in paths:
     rootfile=TFile(path+".root","RECREATE")
     for filename in os.listdir("."):
        skip=False
        if not ".log" in filename: skip=True
	for s in path:
	  if not s in filename: skip=True
        if skip: continue
        print filename
        f=file(filename)
        pointsNLO=[]
        name=""
	previousBin=None
        for line in f.readlines():
            split=line.replace("D","e").strip(" ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").split(" ")
	    print split
            if len(split)==12 and ".00" in split[6]:
               name="chi-"+str(int(float(split[3])))+"-"+str(int(float(split[4])))
    	       if previousBin!=name:
	          if previousBin!=None:
                      writeHistogram(previousBin,pointsNLO)
		  pointsNLO=[]
		  previousBin=name
               pointsNLO+=[(float(split[6]),float(split[7]),float(split[10]))]
        writeHistogram(previousBin,pointsNLO)
     rootfile.Close()
