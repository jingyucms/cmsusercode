import os
from ROOT import *
import array

massbins=[(4200,8000),
	      (3600,4200),
#	      (3000,3600),
#	      (2400,3000),
#	      (1900,2400),
              ]

model=4

if model==0:
    signal="CI"    
    signalMasses=[8000,9000,10000,12000,14000]
if model==1:
    signal="ADD_4_0_0_"
    signalMasses=[4000,5000,6000,7000,8000]
if model==2:
    signal="ADD_4_0_1_"
    signalMasses=[4000,5000,6000,7000,8000,9000]
if model==3:
    signal="LOCI"    
    signalMasses=[8000,9000,10000,11000,12000,13000,14000]
if model==4:
    signal="NLOCI"    
    signalMasses=[8000,9000,10000,11000,12000,13000,14000]

prefix="datacard_shapelimit"

limits={}
for signalMass in signalMasses:
    cfg=open("chi_datacard_"+signal+"_"+str(signalMass)+".txt","w")
    f=TFile(prefix+"_"+str(signal)+str(signalMass)+"_chi.root")
    cfg.writelines("""
imax """+str(len(massbins))+""" number of channels
jmax 2 number of backgrounds
kmax 3 number of nuisance parameters
-----------
""")
    for i in range(len(massbins)):
        cfg.writelines("""shapes * bin"""+str(i)+""" """+prefix+"""_"""+str(signal)+str(signalMass)+"""_chi.root $PROCESS#chi"""+str(massbins[i][0])+"""_"""+str(massbins[i][1])+"""_rebin1 $PROCESS#chi"""+str(massbins[i][0])+"""_"""+str(massbins[i][1])+"""_rebin1_$SYSTEMATIC
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
       text+=str(i)+" "+str(i)+" "+str(i)+" "
    text+="\nprocess "
    for i in range(len(massbins)):
       text+="QCD"+str(signal)+str(signalMass)+" QCD"+str(signal)+str(signalMass)+"_ALT QCD "
    text+="\nprocess "
    for i in range(len(massbins)):
       text+="-1 0 1 "
    text+="\nrate "
    for i in range(len(massbins)):
       hQCD=f.Get("QCD#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       hALT=f.Get("QCD"+str(signal)+str(signalMass)+"_ALT#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       h=f.Get("QCD"+str(signal)+str(signalMass)+"#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       print "QCD#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1",hQCD.Integral()
       print "QCD"+str(signal)+str(signalMass)+"_ALT#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1",hALT.Integral()
       print "QCD"+str(signal)+str(signalMass)+"#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1",h.Integral()
       text+=str(h.Integral())+" "+str(hALT.Integral())+" "+str(hQCD.Integral())+" "
    cfg.writelines(text+"""
-----------
""")
    text=""
    text+="jes shape "
    for i in range(len(massbins)):
       text+="1 1 - "
    text+="\npdf shape "
    for i in range(len(massbins)):
       text+="- 1 - "
    text+="\nscale shape "
    for i in range(len(massbins)):
       text+="- 1 - "
    cfg.writelines(text+"""
-----------
""")

    cfg.close()
    os.system("cp HiggsJPC.py ${CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/python")
    os.system("text2workspace.py -m "+str(signalMass)+" chi_datacard_"+signal+"_"+str(signalMass)+".txt -P HiggsAnalysis.CombinedLimit.HiggsJPC:twoHypothesisHiggs -o fixedMu_"+str(signalMass)+".root")
    os.system("combine -m "+str(signalMass)+" -M HybridNew --singlePoint 1.0 --rule CLs --saveHybridResult --testStat LEP --fork 4 -T 10000 fixedMu_"+str(signalMass)+".root > limits"+signal+"_"+str(signalMass)+".txt") # --frequentist --testStat LHC
    os.system('root -q -b higgsCombineTest.HybridNew.mH'+str(signalMass)+'.root "${CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/test/plotting/hypoTestResultTree.cxx(\\"qmu_'+str(signalMass)+'.root\\",'+str(signalMass)+',1,\\"x\\")"')
    os.system('root -q -b "./extractSignificanceStats.C(\\"'+str(signalMass)+'\\")" > limits'+signal+'_exp_'+str(signalMass)+'.txt')

    f=file("limits"+signal+"_"+str(signalMass)+".txt")
    for line in f.readlines():
        if "CLs = " in line:
           limits[signalMass]=[signalMass,float(line.strip().split(" ")[-3]),float(line.strip().split(" ")[-1])]
	   break

    f=file("limits"+signal+"_exp_"+str(signalMass)+".txt")
    for line in f.readlines():
        if "Expected CLs" in line:
           limits[signalMass]+=[float(line.strip().split(" ")[-1])]
    for i in range(len(limits[signalMass]),8):
         limits[signalMass]+=[0]

print limits
f=file("limits"+signal+".txt","w")
f.write(str([limits[signalMass] for signalMass in signalMasses]))
f.close()
