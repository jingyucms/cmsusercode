import os
from ROOT import *
import array
import ROOT

massbins=[(4800,13000),
	      (4200,4800),
	      (3600,4200),
              ]

#models=[1,2]
#models=[36,37,38,39,40,41,42,43]
#models=[36,37,38,42]
models=[1,2]

for model in models:

 if model==1:
    signal="CIplusLL"    
    signalMasses=[8000,9000,10000,11000,12000,13000,14000,16000,18000]
 if model==2:
    signal="ADD"
    signalMasses=[6000,7000,8000,9000,10000,11000,12000,13000,14000]

 if model==36:
    signal="CIplusLL"    
    signalMasses=[12000]
    massbins=[(4800,13000),]
 if model==37:
    signal="CIplusLL"    
    signalMasses=[12000]
    massbins=[(4200,4800),]
 if model==38:
    signal="CIplusLL"    
    signalMasses=[12000]
    massbins=[(3600,4200),]
 if model==39:
    signal="CIplusLL"    
    signalMasses=[12000]
    massbins=[(3000,3600),]
 if model==40:
    signal="CIplusLL"    
    signalMasses=[12000]
    massbins=[(2400,3000),]
 if model==41:
    signal="CIplusLL"    
    signalMasses=[11000]
    massbins=[(1900,2400),]
 if model==42:
    signal="CIplusLL"    
    signalMasses=[12000]
    massbins=[(3600,4200),(4200,4800),(4800,13000)]
 if model==43:
    signal="CIplusLL"    
    signalMasses=[11000]
    massbins=[(1900,2400),(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,13000)]


 dire="/shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/"
 prefix=dire+"datacard_shapelimit13TeV"

 if model>10 and model<100:
    name="pvalue_"+signal+"_"+("_".join([s[0:4] for s in str(massbins).strip("[]").split("(")])).strip("_")
 else:
    name="limits_"+signal

 limits={}
 for signalMass in signalMasses:
    signalWithMass=signal+str(signalMass)
    print signalWithMass
    cfg=open("chi_datacard13TeV_"+signalWithMass+".txt","w")
    if signal=="ADD":
       fname=prefix+"_GENaddv2_chi.root"
    else:
       fname=prefix+"_GENciv2_chi.root"
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
    print "data_obs#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1"
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
       text+="QCD"+signalWithMass+" QCD"+signalWithMass+"_ALT QCD "
    text+="\nprocess "
    for i in range(len(massbins)):
       text+="-1 0 1 "
    text+="\nrate "
    for i in range(len(massbins)):
       hQCD=f.Get("QCD#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       hALT=f.Get("QCD"+signalWithMass+"_ALT#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       h=f.Get("QCD"+signalWithMass+"#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       print "QCD#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1",hQCD.Integral()
       print "QCD"+signalWithMass+"_ALT#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1",hALT.Integral()
       print "QCD"+signalWithMass+"#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1",h.Integral()
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
    #text+="\npdf shape "
    #for i in range(len(massbins)):
    #   text+="- 1 - "
    text+="\nscale shape "
    for i in range(len(massbins)):
       text+="- 1 - "
    cfg.writelines(text+"""
-----------
""")

    cfg.close()
    os.system("cp "+dire+"HiggsJPC.py ${CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/python")
    os.system("text2workspace.py -m "+str(signalMass)+" chi_datacard13TeV_"+signalWithMass+".txt -P HiggsAnalysis.CombinedLimit.HiggsJPC:twoHypothesisHiggs -o fixedMu_"+signalWithMass+".root")
    os.system("combine -m "+str(signalMass)+" -M HybridNew --singlePoint 1.0 --rule CLs --saveHybridResult --testStat LEP --fork 4 -T 30000 -n "+signal+" fixedMu_"+signalWithMass+".root > "+name+"_"+str(signalMass)+".txt") # --frequentist --testStat LHC
    os.system('root -q -b higgsCombine'+signal+'.HybridNew.mH'+str(signalMass)+'.root "${CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/test/plotting/hypoTestResultTree.cxx(\\"qmu_'+signal+str(signalMass)+'.root\\",'+str(signalMass)+',1,\\"x\\")"')
    os.system('root -q -b '+dire+'"extractSignificanceStats.C(\\"'+signal+str(signalMass)+'\\")" > '+name+'_exp_'+str(signalMass)+'.txt')

 for signalMass in signalMasses:
    limits[signalMass]=[]
    f=file(name+"_"+str(signalMass)+".txt")
    for line in f.readlines():
        if "CLs = " in line:
           limits[signalMass]=[signalMass,float(line.strip().split(" ")[-3]),float(line.strip().split(" ")[-1])]
        if "CLb      = " in line:
           print "observed signficance (p-value): ",ROOT.Math.normal_quantile_c((1.-float(line.strip().split(" ")[-3]))/2.,1),"(",(1.-float(line.strip().split(" ")[-3])),")"
    if len(limits[signalMass])==0:
         limits[signalMass]+=[signalMass]
    f=file(name+"_exp_"+str(signalMass)+".txt")
    for line in f.readlines():
        if "Expected CLs" in line:
           limits[signalMass]+=[float(line.strip().split(" ")[-1])]
    for i in range(len(limits[signalMass]),8):
         limits[signalMass]+=[0]

 print limits
 name=name+".txt"
 f=file(name,"w")
 f.write(str([limits[signalMass] for signalMass in signalMasses]))
 f.close()
