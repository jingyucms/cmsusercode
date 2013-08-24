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
    paths=[("cidijet_DijetChi_CILHC_2012_Lambda-5000","Order-0_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-6000","Order-0_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-7000","Order-0_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-8000","Order-0_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-9000","Order-0_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-10000","Order-0_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-11000","Order-0_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-12000","Order-0_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-13000","Order-0_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-14000","Order-0_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-15000","Order-0_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-5000","Order-1_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-6000","Order-1_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-7000","Order-1_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-8000","Order-1_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-9000","Order-1_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-10000","Order-1_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-11000","Order-1_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-12000","Order-1_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-13000","Order-1_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-14000","Order-1_xmu-1"),
           ("cidijet_DijetChi_CILHC_2012_Lambda-15000","Order-1_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-5000","Order-0_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-6000","Order-0_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-7000","Order-0_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-8000","Order-0_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-9000","Order-0_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-10000","Order-0_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-11000","Order-0_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-12000","Order-0_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-13000","Order-0_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-14000","Order-0_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-15000","Order-0_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-5000","Order-1_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-6000","Order-1_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-7000","Order-1_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-8000","Order-1_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-9000","Order-1_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-10000","Order-1_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-11000","Order-1_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-12000","Order-1_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-13000","Order-1_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-14000","Order-1_xmu-1"),
           ("cidijet_DijetChi_DILHC_2012_Lambda-15000","Order-1_xmu-1"),
           ]
    for path in paths:
     rootfile=TFile("_".join(path)+".root","RECREATE")
     for filename in os.listdir("."):
        skip=False
        if not ".dat" in filename: skip=True
        for p in path:
            if not p in filename: skip=True
        if skip: continue
        print filename
        lam=filename.split(".")[0].split("-")[-1]
        f=file(filename)
        pointsNLO=[]
        name=""
        histogram=None
        for line in f.readlines():
            if "mass" in line:
                if pointsNLO!=[]:
                    writeHistogram(name,pointsNLO)
                name="chi-"+str(int(float(line.split(",")[0].split("[")[1].strip(" "))))+"-"+str(int(float(line.split(",")[1].split("]")[0].strip(" "))))
                pointsNLO=[]
            elif "Lambda" in line:
                pass
            elif "chi" in line:
                pass
            else:
                split=line.replace("D","e").strip(" ").replace("  "," ").replace("  "," ").replace("  "," ").split(" ")
                pointsNLO+=[(float(split[0]),float(split[1]),float(split[2]))]
        if pointsNLO!=[]:
            writeHistogram(name,pointsNLO)
        pointsNLO=[]
     rootfile.Close()
