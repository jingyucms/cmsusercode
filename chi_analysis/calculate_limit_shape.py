import os
from ROOT import *
import array
import ROOT

massbins=[(4200,8000),
	      (3600,4200),
#	      (3000,3600),
#	      (2400,3000),
#	      (1900,2400),
              ]

models=[2]
#models=[3]
#models=[4]
#models=[5]
#models=[6]
#models=[7]
#models=[8]
#models=[9]
#models=[37,38,39,40,41,42,43,44,]
#models=[17,18,19,20,21,22,23,24,]

for model in models:

 if model==-1:
    signal="CIminusLL"    
    signalMasses=[6000,8000,9000,10000,12000,14000,16000,18000,20000]
 if model==0:
    signal="CI"    
    signalMasses=[6000,8000,9000,10000,12000,14000,16000,18000,20000]
 if model==1:
    signal="ADD_4_0_0_"
    signalMasses=[4000,5000,6000,7000,8000]
 if model==2:
    signal="ADD_4_0_1_"
    signalMasses=[6000,6500,7000,7500,8000,9000]
 if model==3:
    signal="LOCI"    
    signalMasses=[8000,9000,10000,11000,12000,13000,14000,15000]
 if model==4:
    signal="NLOCI"    
    signalMasses=[8000,9000,10000,11000,12000,13000,14000]
 if model==5:
    signal="DLOCI"    
    signalMasses=[8000,9000,10000,11000,12000]
 if model==6:
    signal="DNLOCI"    
    signalMasses=[7000,8000,9000,10000,11000]
 if model==7:
    signal="CI_0_0_1_"    
    signalMasses=[6000,7000,8000,9000,10000,11000,12000]
 if model==8:
    signal="CI_1_1_1_"    
    signalMasses=[9000,10000,11000,12000,14000]
 if model==9:
    signal="CI_-1_-1_-1_"    
    signalMasses=[11000,12000,14000,16000,18000,20000]
 
 if model==37:
    signal="ADLOCI"    
    signalMasses=[11000]
    massbins=[(4200,8000),]
 if model==38:
    signal="ADLOCI"    
    signalMasses=[11000]
    massbins=[(3600,4200),]
 if model==39:
    signal="ADLOCI"    
    signalMasses=[11000]
    massbins=[(3000,3600),]
 if model==40:
    signal="ADLOCI"    
    signalMasses=[11000]
    massbins=[(2400,3000),]
 if model==41:
    signal="ADLOCI"    
    signalMasses=[11000]
    massbins=[(1900,2400),]
 if model==42:
    signal="ADLOCI"    
    signalMasses=[11000]
    massbins=[(3600,4200),(4200,8000),]
 if model==43:
    signal="ADLOCI"    
    signalMasses=[11000]
    massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,8000),]
 if model==44:
    signal="ADLOCI"    
    signalMasses=[11000]
    massbins=[(1900,2400),(2400,3000),(3000,3600),(3600,4200),(4200,8000),]

 if model==17:
    signal="DLOCI"    
    signalMasses=[10000]
    massbins=[(4200,8000),]
 if model==18:
    signal="DLOCI"    
    signalMasses=[10000]
    massbins=[(3600,4200),]
 if model==19:
    signal="DLOCI"    
    signalMasses=[10000]
    massbins=[(3000,3600),]
 if model==20:
    signal="DLOCI"    
    signalMasses=[10000]
    massbins=[(2400,3000),]
 if model==21:
    signal="DLOCI"    
    signalMasses=[10000]
    massbins=[(1900,2400),]
 if model==22:
    signal="DLOCI"    
    signalMasses=[10000]
    massbins=[(3600,4200),(4200,8000),]
 if model==23:
    signal="DLOCI"    
    signalMasses=[10000]
    massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,8000),]
 if model==24:
    signal="DLOCI"    
    signalMasses=[10000]
    massbins=[(1900,2400),(2400,3000),(3000,3600),(3600,4200),(4200,8000),]

 prefix="datacard_shapelimit"

 if model<10:
    name="limits_"+signal
 else:
    name="pvalue_"+signal+"_"+("_".join([s[0:4] for s in str(massbins).strip("[]").split("(")])).strip("_")

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
    os.system("cp HiggsJPC.py ${CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/python")
    os.system("text2workspace.py -m "+str(signalMass)+" chi_datacard_"+signal+"_"+str(signalMass)+".txt -P HiggsAnalysis.CombinedLimit.HiggsJPC:twoHypothesisHiggs -o fixedMu_"+signal+"_"+str(signalMass)+".root")
    os.system("combine -m "+str(signalMass)+" -M HybridNew --singlePoint 1.0 --rule CLs --saveHybridResult --testStat LEP --fork 4 -T 30000 -n "+signal+" fixedMu_"+signal+"_"+str(signalMass)+".root > "+name+"_"+str(signalMass)+".txt") # --frequentist --testStat LHC
    os.system('root -q -b higgsCombine'+signal+'.HybridNew.mH'+str(signalMass)+'.root "${CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/test/plotting/hypoTestResultTree.cxx(\\"qmu_'+signal+str(signalMass)+'.root\\",'+str(signalMass)+',1,\\"x\\")"')
    os.system('root -q -b "./extractSignificanceStats.C(\\"'+signal+str(signalMass)+'\\")" > '+name+'_exp_'+str(signalMass)+'.txt')

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
 if model<10:
    name=name+".txt"
    f=file(name,"w")
    f.write(str([limits[signalMass] for signalMass in signalMasses]))
    f.close()
