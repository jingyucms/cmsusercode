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
    paths=[("CIJET_fnl5662i_ll_nn30lo_LL+_10000"),
           ("CIJET_fnl5662i_ll_nn30lo_LL-_10000"),
           ("CIJET_fnl5662i_ll_nn30nlo_LL+_10000"),
           ("CIJET_fnl5662i_ll_nn30nlo_LL-_10000"),
           ]
    for m in range(5,31):
       paths+=[("CIJET_fnl5662i_cs_nn30nlo_0_"+str(m*1000)+"_LL+"),
               ("CIJET_fnl5662i_cs_nn30nlo_0_"+str(m*1000)+"_LL-"),
               ("CIJET_fnl5662i_cs_nn30nlo_0_"+str(m*1000)+"_RR+"),
               ("CIJET_fnl5662i_cs_nn30nlo_0_"+str(m*1000)+"_RR-"),
               ("CIJET_fnl5662i_cs_nn30nlo_0_"+str(m*1000)+"_VV+"),
               ("CIJET_fnl5662i_cs_nn30nlo_0_"+str(m*1000)+"_VV-"),
               ("CIJET_fnl5662i_cs_nn30nlo_0_"+str(m*1000)+"_AA+"),
               ("CIJET_fnl5662i_cs_nn30nlo_0_"+str(m*1000)+"_AA-"),
               ("CIJET_fnl5662i_cs_nn30nlo_0_"+str(m*1000)+"_V-A+"),
               ("CIJET_fnl5662i_cs_nn30nlo_0_"+str(m*1000)+"_V-A-"),
               ]
    for path in paths:
     rootfile=TFile(path+".root","RECREATE")
     if True:
        filename=path+".xsc"
	print filename
        lam=filename.split(".")[0].split("_")[-1]
        f=file(filename)
        pointsNLO=[]
        name=""
        histogram=None
	nextBin=False
	lowerChi=0
	upperChi=0
        for line in f.readlines():
            split=line.replace("D","e").strip(" ").replace("  "," ").replace("  "," ").replace("  "," ").split(" ")
            if nextBin:
                if pointsNLO!=[] and name!="" and float(split[3])!=float(name.split("-")[-1]):
                    writeHistogram(name,pointsNLO)
	            print name
                    pointsNLO=[]
		nextBin=False
                lowerChi=float(split[0])
                upperChi=float(split[1])
		name="chi-"+str(int(float(split[2])))+"-"+str(int(float(split[3])))
            elif "Bin information" in line:
                nextBin=True
            elif "Lambda" in line:
                pass
            elif "lo" in line:
                pass
            elif "cj" in line:
                pass
            elif "muf" in line:
                pass
            elif len(split)==4 and float(split[0])==1 and float(split[1])==1:
	        if "lo" in path[0]:
		  #print "saving LO",name
                  pointsNLO+=[(lowerChi,upperChi,float(split[2])/(upperChi-lowerChi))]
                else:
		  #print "saving NLO",name
		  pointsNLO+=[(lowerChi,upperChi,float(split[3])/(upperChi-lowerChi))]
        if pointsNLO!=[]:
            writeHistogram(name,pointsNLO)
	    print name
            pointsNLO=[]
     rootfile.Close()
