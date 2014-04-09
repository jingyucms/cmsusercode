import os
from ROOT import *
import array
import ROOT

massbins=[(4200,8000),
	      (3600,4200),
	      #(3000,3600),
#	      (2400,3000),
#	      (1900,2400),
              ]

#models=[37,38,39,40,41,42,43,44,]
#models=[17,18,19,20,21,22,23,24,]

models=[9]
#models=[2,3,4,5]
#models=[100,101]
#models=[102,103,104]
#models=[105,106]
#models=[107,108,109]
#models=[300,301]

#models=[2,3,4,5,6,7,8,9]
#models=[200,201,202,203,204,205,206,207,208,209]
#models=[300,301,302,303,304,305,306,307,308,309]

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
 if model==9:
    signal="ADD_4_0_1_"
    signalMasses=[6000,6500,7000,7500,8000,9000]
 if model==5:
    signal="LOCI"    
    signalMasses=[8000,9000,10000,11000,12000,13000,14000,15000]
 if model==3:
    signal="NLOCI"    
    signalMasses=[8000,9000,10000,11000,12000,13000,14000]
 if model==4:
    signal="DLOCI"    
    signalMasses=[8000,9000,10000,11000,12000]
 if model==2:
    signal="DNLOCI"    
    signalMasses=[7000,8000,9000,10000,11000]
 if model==8:
    signal="CI_0_0_1_"    
    signalMasses=[6000,7000,8000,9000,10000,11000,12000]
 if model==6:
    signal="CI_1_1_1_"    
    signalMasses=[9000,10000,11000,12000,14000]
 if model==7:
    signal="CI_-1_-1_-1_"    
    signalMasses=[11000,12000,14000,16000,18000,20000]


 if model==100:
    signal="CT10nlo_LL+"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==101:
    signal="CT10nlo_LL-"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==102:
    signal="CT10nlo_RR+"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==103:
    signal="CT10nlo_RR-"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==104:
    signal="CT10nlo_VV+"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==105:
    signal="CT10nlo_VV-"
    signalMasses=[8000,9000,10000,12000,13000,14000,15000,16000,17000,18000,19000,20000]
 if model==106:
    signal="CT10nlo_AA+"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==107:
    signal="CT10nlo_AA-"
    signalMasses=[8000,9000,10000,12000,13000,14000,15000,16000,17000,18000,19000,20000]
 if model==108:
    signal="CT10nlo_V-A+"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==109:
    signal="CT10nlo_V-A-"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]

 if model==200:
    signal="cteq66_LL+"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==201:
    signal="cteq66_LL-"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==202:
    signal="cteq66_RR+"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==203:
    signal="cteq66_RR-"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==204:
    signal="cteq66_VV+"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==205:
    signal="cteq66_VV-"
    signalMasses=[8000,9000,10000,12000,13000,14000,15000,16000,17000,18000,19000,20000]
 if model==206:
    signal="cteq66_AA+"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==207:
    signal="cteq66_AA-"
    signalMasses=[8000,9000,10000,12000,13000,14000,15000,16000,17000,18000,19000,20000]
 if model==208:
    signal="cteq66_V-A+"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==209:
    signal="cteq66_V-A-"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]

 if model==300:
    signal="cteq6ll_LL+"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==301:
    signal="cteq6ll_LL-"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==302:
    signal="cteq6ll_RR+"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==303:
    signal="cteq6ll_RR-"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==304:
    signal="cteq6ll_VV+"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==305:
    signal="cteq6ll_VV-"
    signalMasses=[8000,9000,10000,12000,13000,14000,15000,16000,17000,18000,19000,20000]
 if model==306:
    signal="cteq6ll_AA+"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==307:
    signal="cteq6ll_AA-"
    signalMasses=[8000,9000,10000,12000,13000,14000,15000,16000,17000,18000,19000,20000]
 if model==308:
    signal="cteq6ll_V-A+"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]
 if model==309:
    signal="cteq6ll_V-A-"
    signalMasses=[5000,6000,7000,8000,9000,10000,12000,13000,14000,15000]


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

 if model>10 and model<100:
    name="pvalue_"+signal+"_"+("_".join([s[0:4] for s in str(massbins).strip("[]").split("(")])).strip("_")
 else:
    name="limits_"+signal

 limits={}
 for signalMass in signalMasses:
    if model>=100:
      signalWithMass=signal.split("_")[0]+"_"+str(signalMass)+"_"+signal.split("_")[1]
    else:
      signalWithMass=signal+str(signalMass)
    print signalWithMass
    cfg=open("chi_datacard_"+signalWithMass+".txt","w")
    f=TFile(prefix+"_"+signalWithMass+"_chi.root")
    cfg.writelines("""
imax """+str(len(massbins))+""" number of channels
jmax 2 number of backgrounds
kmax 3 number of nuisance parameters
-----------
""")
    for i in range(len(massbins)):
        cfg.writelines("""shapes * bin"""+str(i)+""" """+prefix+"""_"""+signalWithMass+"""_chi.root $PROCESS#chi"""+str(massbins[i][0])+"""_"""+str(massbins[i][1])+"""_rebin1 $PROCESS#chi"""+str(massbins[i][0])+"""_"""+str(massbins[i][1])+"""_rebin1_$SYSTEMATIC
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
    os.system("cp HiggsJPC.py ${CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/python")
    os.system("text2workspace.py -m "+str(signalMass)+" chi_datacard_"+signalWithMass+".txt -P HiggsAnalysis.CombinedLimit.HiggsJPC:twoHypothesisHiggs -o fixedMu_"+signalWithMass+".root")
    os.system("combine -m "+str(signalMass)+" -M HybridNew --singlePoint 1.0 --rule CLs --saveHybridResult --testStat LEP --fork 4 -T 30000 -n "+signal+" fixedMu_"+signalWithMass+".root > "+name+"_"+str(signalMass)+".txt") # --frequentist --testStat LHC
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
 if not (model>10 and model<100):
    name=name+".txt"
    f=file(name,"w")
    f.write(str([limits[signalMass] for signalMass in signalMasses]))
    f.close()
