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
    uncprefix="fnl5662i_v23_fix_CT14"
    uncpaths=[("6P"),
           ("HC"),
          ]
    uncpoints={}
    for path in uncpaths:
     for filename in os.listdir("."):
        skip=False
        if not ".log" in filename: skip=True
	if not path.replace("_ak4","").replace("_ak5","") in filename: skip=True
	if not uncprefix in filename: skip=True
        if skip: continue
        print filename
        f=file(filename)
        pointsNLO=[]
        name=""
	previousBin=None
        for line in f.readlines():
            split=line.replace("D","e").strip(" ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").split(" ")
	    #print split
            if len(split)==4 and "E-02" in split[1]:
	       uncpoints[path+split[0]]=(float(split[2]),float(split[3]))

    paths=[("fnl5622i_v23_ak5"),
           ("fnl5662i_v23_fix_CT14_ak4"),
           ("fnl5662j_v23_fix_CT14nlo_allmu_ak4"),
	  ]
    for path in paths:
     rootfile=TFile(path+".root","RECREATE")
     for filename in os.listdir("."):
        skip=False
        if not ".log" in filename: skip=True
	if not path.replace("_ak4","").replace("_ak5","") in filename: skip=True
	if "6P" in filename or "HC" in filename: skip=True
	if "norm" in filename: skip=True
        if skip: continue
        print filename
        f=file(filename)
        pointsNLO=[]
        name=""
	previousBin=None
        for line in f.readlines():
            split=line.replace("D","e").strip(" ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").split(" ")
	    if "xmur" in line and ("0.5" in line or "2.0" in line): break
	    #print split
            if len(split)==12 and ".00" in split[6]:
               name="chi-"+str(int(float(split[3])))+"-"+str(int(float(split[4])))
    	       if previousBin!=name:
	          if previousBin!=None:
                     writeHistogram(previousBin,pointsNLO)
		     try:
        	      # scale Down
        	      pointsScaleDown=[(chimin,chimax,value*(1+uncpoints["6P"+index][0])) for chimin,chimax,value,index in pointsNLO]
        	      writeHistogram(previousBin+"scaleDown",pointsScaleDown)
        	      # scale up
        	      pointsScaleUp=[(chimin,chimax,value*(1+uncpoints["6P"+index][1])) for chimin,chimax,value,index in pointsNLO]
        	      writeHistogram(previousBin+"scaleUp",pointsScaleUp)
        	      # PDF Down
        	      pointsPDFDown=[(chimin,chimax,value*(1+uncpoints["HC"+index][0])) for chimin,chimax,value,index in pointsNLO]
        	      writeHistogram(previousBin+"PDFDown",pointsPDFDown)
        	      # PDF up
        	      pointsPDFUp=[(chimin,chimax,value*(1+uncpoints["HC"+index][1])) for chimin,chimax,value,index in pointsNLO]
        	      writeHistogram(previousBin+"PDFUp",pointsPDFUp)
		     except: print "non systematic found"
		  pointsNLO=[]
		  previousBin=name
               pointsNLO+=[(float(split[6]),float(split[7]),float(split[10]),split[0])]
        writeHistogram(previousBin,pointsNLO)
	try:
	 # scale Down
	 pointsScaleDown=[(chimin,chimax,value*(1+uncpoints["6P"+index][0])) for chimin,chimax,value,index in pointsNLO]
         writeHistogram(previousBin+"scaleDown",pointsScaleDown)
	 # scale up
 	 pointsScaleUp=[(chimin,chimax,value*(1+uncpoints["6P"+index][1])) for chimin,chimax,value,index in pointsNLO]
         writeHistogram(previousBin+"scaleUp",pointsScaleUp)
 	 # PDF Down
	 pointsPDFDown=[(chimin,chimax,value*(1+uncpoints["HC"+index][0])) for chimin,chimax,value,index in pointsNLO]
         writeHistogram(previousBin+"PDFDown",pointsPDFDown)
	 # PDF up
	 pointsPDFUp=[(chimin,chimax,value*(1+uncpoints["HC"+index][1])) for chimin,chimax,value,index in pointsNLO]
         writeHistogram(previousBin+"PDFUp",pointsPDFUp)
        except: print "non systematic found"
     rootfile.Close()
