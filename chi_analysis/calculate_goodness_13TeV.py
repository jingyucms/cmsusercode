import os
from ROOT import *
import array

massbinssets=[[(4800,13000)],
              [(4200,4800)],
	      [(3600,4200)],
	      [(3000,3600)],
	      [(2400,3000)],
	      [(1900,2400)],
              [(3600,4200),(4200,4800),(4800,13000)],
	      [(1900,2400),(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,13000)],
	      ]

signal="QCD"    
signalMass=""

prefix="datacard_shapelimit13TeV"

for massbins in massbinssets:
    limits={}
    name=("_".join([s[0:4] for s in str(massbins).strip("[]").split("(")])).strip("_")
    print name
    cfg=open("chi_datacard_"+name+"_bestfit.txt","w")
    f=TFile(prefix+"_GENv2_chi.root")
    cfg.writelines("""
imax """+str(len(massbins))+""" number of channels
jmax 0 number of backgrounds
kmax 3 number of nuisance parameters
-----------
""")
    for i in range(len(massbins)):
        cfg.writelines("""shapes * bin"""+str(i)+""" """+prefix+"""_GENv2_chi.root $PROCESS#chi"""+str(massbins[i][0])+"""_"""+str(massbins[i][1])+"""_rebin1_$SYSTEMATIC
""")
    cfg.writelines("""-----------
""")
    text="bin "
    for i in range(len(massbins)):
       text+=str(i)+" "
    text+="\nobservation "
    for i in range(len(massbins)):
       hData=f.Get("data_obs#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       text+=str(hData.Integral())+" "
    cfg.writelines(text+"""
-----------
""")
    text="bin "
    for i in range(len(massbins)):
       text+=str(i)+" "
    text+="\nprocess "
    for i in range(len(massbins)):
       text+=""+str(signal)+str(signalMass)+"_ALT"
    text+="\nprocess "
    for i in range(len(massbins)):
       text+="1 "
    text+="\nrate "
    for i in range(len(massbins)):
       #hQCD=f.Get("QCD#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       hALT=f.Get(""+str(signal)+str(signalMass)+"_ALT#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       h=f.Get(""+str(signal)+str(signalMass)+"#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       #print "QCD#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1",hQCD.Integral()
       print ""+str(signal)+str(signalMass)+"_ALT#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1",hALT.Integral()
       print ""+str(signal)+str(signalMass)+"#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1",h.Integral()
       text+=str(hALT.Integral())+" "
    cfg.writelines(text+"""
-----------
""")
    text=""
    text+="jer shape "
    for i in range(len(massbins)):
       text+="1 "
    #text+="\nunfold shape "
    #for i in range(len(massbins)):
    #   text+="1 "
    text+="\njes shape "
    for i in range(len(massbins)):
       text+="1 "
    #text+="\npdf shape "
    #for i in range(len(massbins)):
    #   text+="1 "
    text+="\nscale shape "
    for i in range(len(massbins)):
       text+="1 "
    cfg.writelines(text+"""
-----------
""")

    cfg.close()
    #os.system("combine chi_datacard_"+name+"_bestfit.txt -M MaxLikelihoodFit -n "+name+"bestfit > bestfit"+name+".txt")
    #os.system("python diffNuisances.py -a mlfit"+name+"bestfit.root > bestfit"+name+"_nuisances.txt")
    os.system("combine chi_datacard_"+name+"_bestfit.txt -M GoodnessOfFit --algo saturated --fixedSignalStrength=0 -n "+name+"goodnessfit > goodnessfit"+name+".txt")
    for toy in range(0,20):
       command="combine chi_datacard_"+name+"_bestfit.txt -M GoodnessOfFit --algo saturated --fixedSignalStrength=0 -t 450 --saveToys -n "+name+"goodnessfittoys_toy"+str(toy)+" > goodnessfittoys"+name+"_toy"+str(toy)+".txt"
       if toy!=9 and toy!=18 and toy!=19:
          command+="&"
       os.system(command)
    os.system('hadd -f higgsCombine'+name+'goodnessfittoys.GoodnessOfFit.mH120.123456.root higgsCombine'+name+'goodnessfittoys_toy*.GoodnessOfFit.mH120.123456.root')
    os.system('root -q -b "./extractGoodnessStats.C(\\"'+name+'\\")" > goodnessfittoysmulti'+name+'.txt')
