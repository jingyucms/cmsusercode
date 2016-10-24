import os,sys
from ROOT import *
import array
import ROOT

massbins=[(4800,13000),
	      (4200,4800),
	      (3600,4200),
              ]

models=[1,2,3,4,5,6,7]
models+=[8,9]
models+=[10]
models=[20,21,22,23,24,25,26,27,28,29]
models+=[30,31,32,33,34,35,36,37]
models+=[40,41,42,43,44,45,46,47]
#models=[1]

xsecs={}
for l in open("xsecs_13TeV_dm.txt").readlines():
  xsecs[l.split("     ")[0]]=eval(l.split("     ")[1])

counter=100
signalName={}
signalExtraName={}
for gq in ["0.1","0.15","0.2","0.25","0.5","0.75","1.0","1.25","1.5","1.75","2.0","2.25","2.5","2.75","3.0","3.5","4.0","6.0","8.0", "10.0"]:
   for vector in ["800"]:#"801"
     models+=[counter]
     signalName[counter]="DM"
     signalExtraName[counter]="_1_"+gq+"_"+vector
     counter+=1
for gq in ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0", "5.5", "6.0", "8.0", "10.0", "12.0", "15.0", "20.0"]:
   for vector in ["800"]:#"801"
     models+=[counter]
     signalName[counter]="DM"
     signalExtraName[counter]="_1_"+gq+"_"+vector+"_zprime5"
     counter+=1

signalExtra=""
includeSignalTheoryUncertainties=False

if len(sys.argv)>1:
   models=[int(sys.argv[1])]

for model in models:

 if model==1:
    signal="CIplusLL"    
    signalMasses=[8000,9000,10000,11000,12000,13000,14000,16000,18000]
 if model==2:
    signal="CIminusLL"    
    signalMasses=[8000,9000,10000,11000,12000,13000,14000,16000,18000]
 if model==3:
    signal="ADD"
    signalMasses=[6000,7000,8000,9000,10000,11000,12000,13000,14000]
 if model==4:
    signal="cs_nn30nlo_0_"
    signalExtra="_LL+"
    signalMasses=[8000,9000,10000,11000,12000,13000,14000,15000,16000,17000,18000]
    massbins=[(4200,4800),(4800,13000)]
 if model==5:
    signal="cs_nn30nlo_0_"
    signalExtra="_LL+"
    signalMasses=[8000,9000,10000,11000,12000,13000,14000,15000,16000,17000,18000]
    massbins=[(4800,13000)]
 if model==6:
    signal="cs_nn30nlo_0_"
    signalExtra="_LL+"
    signalMasses=[8000,9000,10000,11000,12000,13000,14000,15000,16000,17000,18000]
    massbins=[(4200,4800)]
 if model==7:
    signal="cs_nn30nlo_0_"
    signalExtra="_LL+"
    signalMasses=[8000,9000,10000,11000,12000,13000,14000,15000,16000,17000,18000]
    massbins=[(3600,4200)]
 if model==8:
    signal="cs_nn30nlo_0_"
    signalExtra="_LL-"
    signalMasses=[12000,13000,14000,15000,16000,17000,18000,19000,20000,22000,24000]
    massbins=[(4200,4800),(4800,13000)]
 if model==9:
    signal="cs_nn30nlo_0_"
    signalExtra="_LL-"
    signalMasses=[12000,13000,14000,15000,16000,17000,18000,19000,20000,22000,24000]
    massbins=[(4800,13000)]
 if model==10:
    signal="ADD6QBH"    
    signalMasses=[6500,7000,7500,8000,8500,9000]
    massbins=[(3600,4200),(4200,4800),(4800,13000)]
 if model==11:
    signal="RS1QBH"
    signalMasses=[4000,4500,5000,5500,6000,6500]
    massbins=[(3600,4200),(4200,4800),(4800,13000)]

 if model==18:
    signal="cs_ct14nlo_"
    signalExtra="_LL+"
    signalMasses=[8000,9000,10000,11000,12000,13000,14000,15000,16000,17000,18000]
 if model==19:
    signal="cs_ct14nlo_"
    signalExtra="_LL+"
    signalMasses=[8000,9000,10000,11000,12000,13000,14000,15000,16000,17000,18000]
    includeSignalTheoryUncertainties=True

 if model==20:
    signal="cs_nn30nlo_0_"
    signalExtra="_LL+"
    signalMasses=[8000,9000,10000,11000,12000,13000,14000,15000,16000,17000,18000]
 if model==21:
    signal="cs_nn30nlo_0_"
    signalExtra="_LL-"
    signalMasses=[12000,13000,14000,15000,16000,17000,18000,19000,20000,22000,24000]
 if model==22:
    signal="cs_nn30nlo_0_"
    signalExtra="_RR+"
    signalMasses=[8000,9000,10000,11000,12000,13000,14000,15000,16000,17000,18000]
 if model==23:
    signal="cs_nn30nlo_0_"
    signalExtra="_RR-"
    signalMasses=[12000,13000,14000,15000,16000,17000,18000,19000,20000,22000,24000]
 if model==24:
    signal="cs_nn30nlo_0_"
    signalExtra="_VV+"
    signalMasses=[10000,11000,12000,13000,14000,15000,16000,17000,18000,19000,20000]
 if model==25:
    signal="cs_nn30nlo_0_"
    signalExtra="_VV-"
    signalMasses=[13000,14000,15000,16000,17000,18000,19000,20000,22000,24000,26000]
 if model==26:
    signal="cs_nn30nlo_0_"
    signalExtra="_AA+"
    signalMasses=[10000,11000,12000,13000,14000,15000,16000,17000,18000,19000,20000]
 if model==27:
    signal="cs_nn30nlo_0_"
    signalExtra="_AA-"
    signalMasses=[13000,14000,15000,16000,17000,18000,19000,20000,22000,24000,26000]
 if model==28:
    signal="cs_nn30nlo_0_"
    signalExtra="_V-A+"
    signalMasses=[8000,9000,10000,11000,12000,13000,14000,15000,16000,17000,18000]
 if model==29:
    signal="cs_nn30nlo_0_"
    signalExtra="_V-A-"
    signalMasses=[8000,9000,10000,11000,12000,13000,14000,15000,16000,17000,18000]

 if model==30:
    signal="cs_nn30nlo_0_"
    signalExtra="_LL+"
    signalMasses=[12000]
    massbins=[(4800,13000),]
 if model==31:
    signal="cs_nn30nlo_0_"
    signalExtra="_LL+"
    signalMasses=[12000]
    massbins=[(4200,4800),]
 if model==32:
    signal="cs_nn30nlo_0_"
    signalExtra="_LL+"
    signalMasses=[12000]
    massbins=[(3600,4200),]
 if model==33:
    signal="cs_nn30nlo_0_"
    signalExtra="_LL+"
    signalMasses=[12000]
    massbins=[(3000,3600),]
 if model==34:
    signal="cs_nn30nlo_0_"
    signalExtra="_LL+"
    signalMasses=[12000]
    massbins=[(2400,3000),]
 if model==35:
    signal="cs_nn30nlo_0_"
    signalExtra="_LL+"
    signalMasses=[12000]
    massbins=[(1900,2400),]
 if model==36:
    signal="cs_nn30nlo_0_"
    signalExtra="_LL+"
    signalMasses=[12000]
    massbins=[(3600,4200),(4200,4800),(4800,13000)]
 if model==37:
    signal="cs_nn30nlo_0_"
    signalExtra="_LL+"
    signalMasses=[12000]
    massbins=[(1900,2400),(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,13000)]

 if model==40:
    signal="AntiCIplusLL"    
    signalMasses=[12000]
    massbins=[(4800,13000),]
 if model==41:
    signal="AntiCIplusLL"    
    signalMasses=[12000]
    massbins=[(4200,4800),]
 if model==42:
    signal="AntiCIplusLL"    
    signalMasses=[12000]
    massbins=[(3600,4200),]
 if model==43:
    signal="AntiCIplusLL"    
    signalMasses=[12000]
    massbins=[(3000,3600),]
 if model==44:
    signal="AntiCIplusLL"    
    signalMasses=[12000]
    massbins=[(2400,3000),]
 if model==45:
    signal="AntiCIplusLL"    
    signalMasses=[12000]
    massbins=[(1900,2400),]
 if model==46:
    signal="AntiCIplusLL"    
    signalMasses=[12000]
    massbins=[(3600,4200),(4200,4800),(4800,13000)]
 if model==47:
    signal="AntiCIplusLL"    
    signalMasses=[12000]
    massbins=[(1900,2400),(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,13000)]

 if model>=100:
    signal=signalName[model]
    signalExtra=signalExtraName[model]
    #if float(signalExtraName[model].split("_")[2])<=2:
    signalMasses=[1000,1250,1500,2000,2500,3000,3500,4000,5000,6000,7000]

 #dire="/afs/cern.ch/work/z/zhangj/private/dirQBH13TeVnloCi/CMSSW_7_4_15/src/cmsusercode/chi_analysis/"
 #prefix="/afs/cern.ch/work/z/zhangj/private/dirQBH13TeVnloCi/CMSSW_7_4_15/src/cmsusercode/chi_analysis/datacard_shapelimit13TeV"
 dire="/mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_1_20_patch2/src/cmsusercode/chi_analysis/"
 prefix="/mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/datacard_shapelimit13TeV"

 if model>=30 and model<100:
    name="pvalue_"+signal+"_"+("_".join([s[0:4] for s in str(massbins).strip("[]").split("(")])).strip("_")
 else:
    name="limits"+str(model)+"_"+signal

 limits={}
 for signalMass in signalMasses:
    signalWithMass=signal+str(signalMass)+signalExtra
    print signalWithMass
    cfg=open("chi_datacard13TeV"+str(model)+"_"+signalWithMass+".txt","w")
    #if signal=="ADD":
    #   fname=prefix+"_GENaddv3_chi.root"
    #elif signal=="CIplusLL":
    #   fname=prefix+"_GENciv3_chi.root"
    #else:
    #   fname=prefix+"_GENciminusv3_chi.root"
    if signalWithMass=="CIplusLL8000":
        fname=prefix + '_GENnp-0-v4_chi.root'
    elif signalWithMass=="CIplusLL9000":
        fname=prefix + '_GENnp-1-v4_chi.root'
    elif signalWithMass=="CIplusLL10000":
        fname=prefix + '_GENnp-2-v4_chi.root'
    elif signalWithMass=="CIplusLL11000":
        fname=prefix + '_GENnp-3-v4_chi.root'
    elif signalWithMass=="CIplusLL12000":
        fname=prefix + '_GENnp-4-v4_chi.root'
    elif signalWithMass=="CIplusLL13000":
        fname=prefix + '_GENnp-5-v4_chi.root'
    elif signalWithMass=="CIplusLL14000":
        fname=prefix + '_GENnp-6-v4_chi.root'
    elif signalWithMass=="CIplusLL16000":
        fname=prefix + '_GENnp-7-v4_chi.root'
    elif signalWithMass=="CIplusLL18000":
        fname=prefix + '_GENnp-8-v4_chi.root'
    elif signalWithMass=="CIminusLL8000":
        fname=prefix + '_GENnp-9-v4_chi.root'
    elif signalWithMass=="CIminusLL9000":
        fname=prefix + '_GENnp-10-v4_chi.root'
    elif signalWithMass=="CIminusLL10000":
        fname=prefix + '_GENnp-11-v4_chi.root'
    elif signalWithMass=="CIminusLL11000":
        fname=prefix + '_GENnp-12-v4_chi.root'
    elif signalWithMass=="CIminusLL12000":
        fname=prefix + '_GENnp-13-v4_chi.root'
    elif signalWithMass=="CIminusLL13000":
        fname=prefix + '_GENnp-14-v4_chi.root'
    elif signalWithMass=="CIminusLL14000":
        fname=prefix + '_GENnp-15-v4_chi.root'
    elif signalWithMass=="CIminusLL16000":
        fname=prefix + '_GENnp-16-v4_chi.root'
    elif signalWithMass=="CIminusLL18000":
        fname=prefix + '_GENnp-17-v4_chi.root'
    elif signalWithMass=="ADD6000":
        fname=prefix + '_GENnp-18-v4_chi.root'
    elif signalWithMass=="ADD7000":
        fname=prefix + '_GENnp-19-v4_chi.root'
    elif signalWithMass=="ADD8000":
        fname=prefix + '_GENnp-20-v4_chi.root'
    elif signalWithMass=="ADD9000":
        fname=prefix + '_GENnp-21-v4_chi.root'
    elif signalWithMass=="ADD10000":
        fname=prefix + '_GENnp-22-v4_chi.root'
    elif signalWithMass=="ADD11000":
        fname=prefix + '_GENnp-23-v4_chi.root'
    elif signalWithMass=="ADD12000":
        fname=prefix + '_GENnp-24-v4_chi.root'
    elif signalWithMass=="ADD13000":
        fname=prefix + '_GENnp-25-v4_chi.root'
    elif signalWithMass=="ADD14000":
        fname=prefix + '_GENnp-26-v4_chi.root'
    elif signalWithMass=="AntiCIplusLL12000":
        fname=prefix + '_GENnp-antici-v4_chi.root'
    elif signalWithMass=="ADD6QBH"+str(signalMass):
        fname=prefix+"_QBH_"+str(signalMass)+"_6_chi_v1.root"
    elif signalWithMass=="RS1QBH"+str(signalMass):
        fname=prefix+"_QBH_"+str(signalMass)+"_RS1_chi_v1.root"
    elif "cs" in signal:
        fname=prefix+"_"+str(signalWithMass)+"_chi.root"
    elif "DM" in signal:
        fname=prefix+"_"+str(signalWithMass)+"_chi.root"
	if not signalWithMass in xsecs.keys():
	  continue
	if signalMass<=2000:
            massbins=[(1900,2400),(2400,3000)]
	if signalMass==2500:
            massbins=[(1900,2400),(2400,3000)]
	if signalMass==3000:
            massbins=[(2400,3000),(3000,3600)]
	if signalMass==3500:
            massbins=[(3000,3600),(3600,4200)]
	if signalMass==4000:
            massbins=[(3600,4200),(4200,4800)]
	if signalMass>=5000:
            massbins=[(4200,4800),(4800,13000)]
    print fname
    if not "DM" in signal and not "cs" in signal:
        signalWithMass="QCD"+signalWithMass
    f=TFile(fname)
    cfg.writelines("""
imax """+str(len(massbins))+""" number of channels
jmax 2 number of backgrounds
kmax 4 number of nuisance parameters
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
       text+=signalWithMass+" "+signalWithMass+"_ALT QCD "
    text+="\nprocess "
    for i in range(len(massbins)):
       text+="-1 0 1 "
    text+="\nrate "
    for i in range(len(massbins)):
       hQCD=f.Get("QCD#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       hALT=f.Get(signalWithMass+"_ALT#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       h=f.Get(signalWithMass+"#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       print "QCD#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1",hQCD.Integral()
       print signalWithMass+"_ALT#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1",hALT.Integral()
       print signalWithMass+"#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1",h.Integral()
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
    text+="\npdf shape "
    for i in range(len(massbins)):
      if includeSignalTheoryUncertainties:
       text+="1 1 - "
      else:
       text+="- 1 - "
    text+="\nscale shape "
    for i in range(len(massbins)):
      if includeSignalTheoryUncertainties:
       text+="1 1 - "
      else:
       text+="- 1 - "
    cfg.writelines(text+"""
-----------
""")

    cfg.close()
    os.system("cp "+dire+"HiggsJPC.py ${CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/python")
    os.system("text2workspace.py -m "+str(signalMass)+" chi_datacard13TeV"+str(model)+"_"+signalWithMass.replace("QCD","")+".txt -P HiggsAnalysis.CombinedLimit.HiggsJPC:twoHypothesisHiggs -o fixedMu_"+signalWithMass.replace("QCD","")+".root")
    os.system("combine -m "+str(signalMass)+" -M HybridNew --singlePoint 1.0 --rule CLs --saveHybridResult --testStat LEP --fork 4 -T 30000 --clsAcc 0.1 -n "+signal+signalExtra+" fixedMu_"+signalWithMass.replace("QCD","")+".root > "+name+"_"+str(signalMass)+".txt") # --frequentist --testStat LHC
    os.system('root -q -b higgsCombine'+signal+signalExtra+'.HybridNew.mH'+str(signalMass)+'.root "${CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/test/plotting/hypoTestResultTree.cxx(\\"qmu_'+signal+str(signalMass)+signalExtra+'.root\\",'+str(signalMass)+',1,\\"x\\")"')
    os.system('root -q -b '+dire+'"extractSignificanceStats.C(\\"'+signal+str(signalMass)+signalExtra+'\\")" > '+name+'_exp_'+str(signalMass)+'.txt')

 for signalMass in signalMasses:
    limits[signalMass]=[]
    try:
      f=file(name+"_"+str(signalMass)+".txt")
    except:
      print "file not found", f
      continue
    for line in f.readlines():
        if "CLs = " in line:
           limits[signalMass]=[signalMass,float(line.strip().split(" ")[-3]),float(line.strip().split(" ")[-1])]
        if "CLb = " in line:
           print "observed signficance (p-value): ",ROOT.Math.normal_quantile_c((1.-float(line.strip().split(" ")[-3]))/2.,1),"(",(1.-float(line.strip().split(" ")[-3])),")"
    if len(limits[signalMass])==0:
         limits[signalMass]+=[signalMass,0,0]
    try:
      f=file(name+"_exp_"+str(signalMass)+".txt")
    except:
      print "file not found", f
      continue
    for line in f.readlines():
        if "Expected CLs" in line:
	  try:
           limits[signalMass]+=[float(line.strip().split(" ")[-1])]
	  except:
           print "didn't find one point"
    for i in range(len(limits[signalMass]),8):
         limits[signalMass]+=[0]

 print limits
 name=name+".txt"
 f=file(name,"w")
 f.write(str([limits[signalMass] for signalMass in signalMasses]))
 f.close()
