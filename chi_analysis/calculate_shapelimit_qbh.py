import os, sys
from ROOT import *
import array, math

massbins=[(4800,13000),(4200,4800),(3600,4200)]

## for ADD6 black hole
#signalMasses=[6500,7000,7500,8000,8500,9000]
#key="6"

## for RS1 black hole
signalMasses=[3500,4000,4500,5000,5500,6000,6500,7000]
key="RS1"

signal="qbh_"

dire="/afs/cern.ch/work/z/zhangj/private/CMSSW_7_4_15/src/"
prefix=dire+"datacard_shapelimit13TeV_"

name="limits"+"_"+signal

limits={}
for signalMass in signalMasses:
    signalWithMasses=signal+str(signalMass)+"_6_"
    cfg=open("chi_datacard13TeV_"+signalWithMasses+".txt","w")
    fname=prefix+"QBH_"+str(signalMass)+"_"+key+"_chi_v1.root"
    print fname
    f=TFile(fname)
    cfg.writelines("""
imax """+str(len(massbins))+""" number of channels
jmax 2 number of backgrounds
kmax 3 number of nuisance parameters
-----------
""")
    for i in range(len(massbins)):
        cfg.writelines("""shapes * bin"""+str(i)+""" """+fname+""" $PROCESS#chi"""+str(massbins[i][0])+"""_"""+str(massbins[i][1])+"""_rebin1 $PROCESS#chi"""+str(massbins[i][0])+"""_"""+str(massbins[i][1])+"""_rebin1_$SYSTEMATIC
""")
    cfg.writelines("""-----------
""")
    text="bin "
    for i in range(len(massbins)):
       text+=str(i)+" "
    text+="\nobservation "
    print "data_obs#chi_"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1"
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
       text+=signalWithMasses+" "+ signalWithMasses+"ALT QCD "
    text+="\nprocess "
    for i in range(len(massbins)):
       text+="-1 0 1 "
    text+="\nrate "
    for i in range(len(massbins)):
       hQCD=f.Get("QCD#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       hALT=f.Get(signalWithMasses+"ALT#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       h=f.Get(signalWithMasses+"#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       print "QCD#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1",hQCD.Integral()
       print signalWithMasses+"ALT#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1",hALT.Integral()
       print signalWithMasses+"#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1",h.Integral()
       text+=str(h.Integral())+" "+str(hALT.Integral())+" "+str(hQCD.Integral())+" "
    cfg.writelines(text+"""
-----------
""")
    text=""
    text+="jer shape "
    for i in range(len(massbins)):
       text+="1 1 - "
    text+="\njes shape "
    for i in range(len(massbins)):
       text+="1 1 - "
    text+="\nscale shape "
    for i in range(len(massbins)):
       text+="- 1 - "
    cfg.writelines(text+"""
-----------
""")

    cfg.close()
    os.system("cp "+dire+"HiggsJPC.py ${CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/python")
    os.system("text2workspace.py -m "+str(signalMass)+" chi_datacard13TeV_"+signalWithMasses+".txt -P HiggsAnalysis.CombinedLimit.HiggsJPC:twoHypothesisHiggs -o fixedMu_"+signalWithMasses+".root")
    os.system("combine -m "+str(signalMass)+" -M HybridNew --singlePoint 1.0 --rule CLs --saveHybridResult --testStat LEP --fork 4 -T 30000 -n "+signal+" fixedMu_"+signalWithMasses+".root > "+name+str(signalMass)+".txt") # --frequentist --testStat LHC
    os.system('root -q -b higgsCombine'+signal+'.HybridNew.mH'+str(signalMass)+'.root "${CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/test/plotting/hypoTestResultTree.cxx(\\"qmu_'+signal+str(signalMass)+'.root\\",'+str(signalMass)+',1,\\"x\\")"')
    os.system('root -q -b '+dire+'"extractSignificanceStats.C(\\"'+signal+str(signalMass)+'\\")" > '+name+'exp_'+str(signalMass)+'.txt')

for signalMass in signalMasses:
    limits[signalMass]=[]
    f=file(name+str(signalMass)+".txt")
    for line in f.readlines():
        if "CLs = " in line:
           limits[signalMass]=[signalMass,float(line.strip().split(" ")[-3]),float(line.strip().split(" ")[-1])]
        if "CLb      = " in line:
           print "observed signficance (p-value): ",ROOT.Math.normal_quantile_c((1.-float(line.strip().split(" ")[-3]))/2.,1),"(",(1.-float(line.strip().split(" ")[-3])),")"
    if len(limits[signalMass])==0:
         limits[signalMass]+=[signalMass]
    f=file(name+"exp_"+str(signalMass)+".txt")
    for line in f.readlines():
        if "Expected CLs" in line:
           limits[signalMass]+=[float(line.strip().split(" ")[-1])]
    for i in range(len(limits[signalMass]),8):
         limits[signalMass]+=[0]

print limits
name=name+key+".txt"
f=file(name,"w")
f.write(str([limits[signalMass] for signalMass in signalMasses]))
f.close()

