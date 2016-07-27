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
    paths=[("DijetAngularCMS13"),
           ]
    for path in paths:
     rootfile=TFile(path+"_ewk.root","RECREATE")
     for filename in os.listdir(path):
        skip=False
        #if not ".txt" in filename: skip=True
	for s in path:
	  if not s in filename: skip=True
        if skip: continue
        print filename
        f=file(path+"/"+filename)
        pointsNLO=[]
        name=""
        for line in f.readlines():
            split=line.replace("D","e").strip(" ").replace("  "," ").replace("  "," ").replace("  "," ").split(" ")
            if "MJJ" in line and "1.900000e+03, 2.400000e+03" in line or "1900.-2400." in line or "starting at 1900 GeV" in line:
		name="chi-1900-2400"
            elif "MJJ" in line and "2.400000e+03, 3.000000e+03" in line or "2400-.3000." in line or "starting at 2400 GeV" in line:
		name="chi-2400-3000"
            elif "MJJ" in line and "3.000000e+03, 3.600000e+03" in line or "3000.-3600." in line or "starting at 3000 GeV" in line:
		name="chi-3000-3600"
            elif "MJJ" in line and "3.600000e+03, 4.200000e+03" in line or "3600.-4200." in line or "starting at 3600 GeV" in line:
		name="chi-3600-4200"
            elif "MJJ" in line and "4.200000e+03, 4.800000e+03" in line or "4200.-4800." in line or "starting at 4200 GeV" in line:
		name="chi-4200-4800"
            elif "MJJ" in line and "4.800000e+03, 5.400000e+03" in line or "4800.-5400." in line or "starting at 4800 GeV" in line:
		name="chi-4800-5400"
            elif "MJJ" in line and "5.400000e+03, 6.000000e+03" in line or "5400.-6000." in line or "starting at 5400 GeV" in line:
		name="chi-5400-6000"
	    elif "#" in line:
                pass
            elif len(split)>2:
                pointsNLO+=[(float(split[0]),float(split[1]),float(split[2]))]
        if pointsNLO!=[]:
            writeHistogram(name,pointsNLO)
        pointsNLO=[]
     rootfile.Close()
