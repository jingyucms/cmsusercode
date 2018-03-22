import os,sys
from ROOT import *
import array
import ROOT
import subprocess

def system_call(command):
    print command
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    return p.stdout.read()
    
#massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)]
massbins=[(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)] # did not calculate CI for lower mass bins yet

xsecs={}
for l in open("xsecs_13TeV_dm.txt").readlines():
  xsecs[l.split("     ")[0]]=eval(l.split("     ")[1])

models=[]
models+=[11]
#models+=[10,11]
#models+=[60,61,62,63,64,65,66,67,68,69]
#models+=[70,71,72,73,74,75,76,77]
#models+=[78,79,80,81,82,83,84,85]
#models+=[30,31,32,33,34,35,36,37,38]
#models+=[40,41,42,43,44,45,46]
#models=[88,89]
#models=[60,61]

VectorDM=True
AxialDM=True

injectSignal=False
dataWithSignal="_DMAxial_Dijet_LO_Mphi_4000_3000_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_1_chi2016_inject.root"

jesSources=16 # 1 corresponds to the single overall variation, 16 to all
separateScaleUncertainties=False

isGen=False

isCB=False

isInjection=False

signalName={}
signalExtraName={}
  
if VectorDM:
  counter=100
  for mdm in ["1","3000"]:
  #for mdm in ["1"]:
    for gv in ["0p01","0p05","0p1","0p2","0p25","0p3","0p5","0p75","1","1p5","2p0","2p5","3p0"]:
      #models+=[counter]
      signalName[counter]="DMVector_Dijet_LO_Mphi"
      signalExtraName[counter]="_"+mdm+"_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_"+gv+"_ga_0"
      counter+=1

if AxialDM:
  counter=1100
  for mdm in ["1","3000"]:
  #for mdm in ["1"]:
    for ga in ["0p01","0p05","0p1","0p2","0p25","0p3","0p5","0p75","1","1p5","2p0","2p5","3p0"]:
      #models+=[counter]
      signalName[counter]="DMAxial_Dijet_LO_Mphi"
      signalExtraName[counter]="_"+mdm+"_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_"+ga
      counter+=1    


testStat="LHC"# in 2012 and 2015 data used "LEP", checking "TEV" and "LHC" for 2016 data
asym="a" #"a" for asymptotic CLS
#testStat="LEP"
#asym=""
# The POI for LHC-style CLS is not clear, since CI models have no freedom  in signal strength or cross section.
# The LEP-style and TEV-style CLS do not fit the POI.

version="_v5" #version number controls how many massbin to use for DM

if len(sys.argv)>1:
   models=[int(sys.argv[1])]

for model in models:

 signalExtra=""
 includeSignalTheoryUncertainties=False

 if model<100:
    version=""
 
 if model==1:
    signal="CIplusLL"    
    signalMasses=[9000,10000,11000,12000,13000,14000,16000,18000]
 if model==2:
    signal="CIminusLL"    
    signalMasses=[9000,10000,11000,12000,13000,14000,16000,18000]
 if model==3:
    signal="ADD"
    signalMasses=[9000,10000,11000,12000,13000,14000,15000,16000,17000]
    #massbins=[(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)] #signal MC statistics not enough in bins <4200
    massbins=[(4800,5400),(5400,6000),(6000,13000)] #signal MC statistics not enough in bins <4200
    #includeSignalTheoryUncertainties=True # from QCD-only though
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
    signal="QBH_"    
    signalMasses=[7500,8000,8500,9000,9500,10000,10500,11000]
    massbins=[(4800,5400),(5400,6000),(6000,13000)]
    signalExtra="_6"
 if model==11:
    signal="QBH_"
    signalMasses=[4500,5000,5500,6000,6500,7000]
    #massbins=[(4800,5400),(5400,6000),(6000,13000)]
    massbins=[(5400,6000),(6000,13000)]
    signalExtra="_RS1"

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

 if model>=30 and model<50:
    includeSignalTheoryUncertainties=True

 if model==30:
    signal="CIplusLL"
    signalMasses=[12000]
    massbins=[(6000,13000),]
 if model==31:
    signal="CIplusLL"
    signalMasses=[12000]
    massbins=[(5400,6000),]
 if model==32:
    signal="CIplusLL"
    signalMasses=[12000]
    massbins=[(4800,5400),]
 if model==33:
    signal="CIplusLL"
    signalMasses=[12000]
    massbins=[(4200,4800),]
 if model==34:
    signal="CIplusLL"
    signalMasses=[12000]
    massbins=[(3600,4200),]
 if model==35:
    signal="CIplusLL"
    signalMasses=[12000]
    massbins=[(3000,3600),]
 if model==36:
    signal="CIplusLL"
    signalMasses=[12000]
    massbins=[(2400,3000),]
 if model==37:
    signal="cs_ct14nlo_"
    signalExtra="_LL+"
    signalMasses=[13000]
    massbins=[(4800,5400),(5400,6000),(6000,13000)]
 if model==38:
    signal="cs_ct14nlo_"
    signalExtra="_LL+"
    signalMasses=[13000]
    massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)]

 if model==40:
    signal="AntiCIplusLL"    
    signalMasses=[12000]
    massbins=[(6000,13000),]
 if model==41:
    signal="AntiCIplusLL"    
    signalMasses=[12000]
    massbins=[(5400,6000),]
 if model==42:
    signal="AntiCIplusLL"    
    signalMasses=[12000]
    massbins=[(4800,5400),]
 if model==43:
    signal="AntiCIplusLL"    
    signalMasses=[12000]
    massbins=[(4200,4800),]
 if model==44:
    signal="AntiCIplusLL"    
    signalMasses=[12000]
    massbins=[(3600,4200),]
 if model==45:
    signal="AntiCIplusLL"    
    signalMasses=[12000]
    massbins=[(3000,3600),]
 if model==46:
    signal="AntiCIplusLL"    
    signalMasses=[12000]
    massbins=[(2400,3000),]
 #if model==47:
 #   signal="AntiCIplusLL"    
 #   signalMasses=[12000]
 #   massbins=[(4800,5400),(5400,6000),(6000,13000)]
 #if model==48:
 #   signal="AntiCIplusLL"    
 #   signalMasses=[12000]
 #   massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)]

 if model>=60 and model<100:
    includeSignalTheoryUncertainties=True

 if model==60 or model==88:
    signal="cs_ct14nlo_"
    signalExtra="_LL+"
    signalMasses=[11000,12000,13000,14000,15000,16000,17000,18000,19000,20000,21000]
 if model==61 or model==89:
    signal="cs_ct14nlo_"
    signalExtra="_LL-"
    signalMasses=[14000,15000,16000,17000,18000,19000,20000,22000,24000,25000,26000,28000,30000]
 if model==62:
    signal="cs_ct14nlo_"
    signalExtra="_RR+"
    signalMasses=[11000,12000,13000,14000,15000,16000,17000,18000,19000,20000,21000]
 if model==63:
    signal="cs_ct14nlo_"
    signalExtra="_RR-"
    signalMasses=[16000,17000,18000,19000,20000,22000,24000,25000,26000,27000,28000]
 if model==64:
    signal="cs_ct14nlo_"
    signalExtra="_VV+"
    signalMasses=[14000,15000,16000,17000,18000,19000,20000,21000,22000,23000,24000]
 if model==65:
    signal="cs_ct14nlo_"
    signalExtra="_VV-"
    signalMasses=[20000,22000,24000,26000,27000,28000,29000,30000]#,32000,34000,36000
 if model==66:
    signal="cs_ct14nlo_"
    signalExtra="_AA+"
    signalMasses=[14000,15000,16000,17000,18000,19000,20000,21000,22000,23000,24000]
 if model==67:
    signal="cs_ct14nlo_"
    signalExtra="_AA-"
    signalMasses=[20000,22000,24000,26000,27000,28000,29000,30000]#,32000,34000,36000
 if model==68:
    signal="cs_ct14nlo_"
    signalExtra="_V-A+"
    signalMasses=[7000,8000,9000,10000,11000,12000,13000,14000,15000,16000]
 if model==69:
    signal="cs_ct14nlo_"
    signalExtra="_V-A-"
    signalMasses=[7000,8000,9000,10000,11000,12000,13000,14000,15000,16000]

 if model==70:
    signal="cs_ct14nlo_"
    signalExtra="_LL+"
    signalMasses=[10000,11000,12000,13000,14000,15000,16000,17000,18000,19000]
    massbins=[(6000,13000)]
 if model==71:
    signal="cs_ct14nlo_"
    signalExtra="_LL+"
    signalMasses=[11000,12000,13000,14000,15000,16000,17000,18000,19000,20000]
    massbins=[(5400,6000)]
 if model==72:
    signal="cs_ct14nlo_"
    signalExtra="_LL+"
    signalMasses=[11000,12000,13000,14000,15000,16000,17000,18000,19000,20000]
    massbins=[(4800,5400)]
 if model==73:
    signal="cs_ct14nlo_"
    signalExtra="_LL+"
    signalMasses=[12000,13000,14000,15000,16000,17000,18000,19000,20000,21000,22000,23000]
    massbins=[(5400,6000),(6000,13000)]
 if model==74:
    signal="cs_ct14nlo_"
    signalExtra="_LL-"
    signalMasses=[13000,14000,15000,16000,17000,18000,19000,20000,22000]
    massbins=[(6000,13000)]
 if model==75:
    signal="cs_ct14nlo_"
    signalExtra="_LL-"
    signalMasses=[15000,16000,17000,18000,19000,20000,22000,24000]
    massbins=[(5400,6000)]
 if model==76:
    signal="cs_ct14nlo_"
    signalExtra="_LL-"
    signalMasses=[14000,15000,16000,17000,18000,19000,20000,22000,24000]
    massbins=[(4800,5400)]
 if model==77:
    signal="cs_ct14nlo_"
    signalExtra="_LL-"
    signalMasses=[14000,15000,16000,17000,18000,19000,20000,22000,24000]
    massbins=[(5400,6000),(6000,13000)]
 if model==78:
    signal="cs_ct14nlo_"
    signalExtra="_LL+"
    signalMasses=[12000,13000,14000,15000,16000,17000,18000,19000,20000,21000,22000,23000]
    massbins=[(4800,5400),(5400,6000),(6000,13000)]
 if model==79:
    signal="cs_ct14nlo_"
    signalExtra="_LL-"
    signalMasses=[14000,15000,16000,17000,18000,19000,20000,22000,24000,26000,28000,30000]
    massbins=[(4800,5400),(5400,6000),(6000,13000)]
 if model==80:
    signal="cs_ct14nlo_"
    signalExtra="_LL+"
    signalMasses=[12000,13000,14000,15000,16000,17000,18000,19000,20000,21000,22000,23000]
    massbins=[(4200,4800),(4800,5400),(5400,6000),(6000,13000)]
 if model==81:
    signal="cs_ct14nlo_"
    signalExtra="_LL-"
    signalMasses=[14000,15000,16000,17000,18000,19000,20000,22000,24000,26000,28000,30000]
    massbins=[(4200,4800),(4800,5400),(5400,6000),(6000,13000)]
 if model==82:
    signal="cs_ct14nlo_"
    signalExtra="_LL+"
    signalMasses=[12000,13000,14000,15000,16000,17000,18000,19000,20000,21000,22000,23000]
    massbins=[(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)]
 if model==83:
    signal="cs_ct14nlo_"
    signalExtra="_LL-"
    signalMasses=[14000,15000,16000,17000,18000,19000,20000,22000,24000,26000,28000,30000]
    massbins=[(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)]
 if model==84:
    signal="cs_ct14nlo_"
    signalExtra="_LL+"
    signalMasses=[12000,13000,14000,15000,16000,17000,18000,19000,20000,21000,22000,23000]
    massbins=[(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)]
 if model==85:
    signal="cs_ct14nlo_"
    signalExtra="_LL-"
    signalMasses=[14000,15000,16000,17000,18000,19000,20000,22000,24000,26000,28000,30000]
    massbins=[(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)]
 if model==86:
    signal="cs_ct14nlo_"
    signalExtra="_LL+"
    signalMasses=[12000,13000,14000,15000,16000,17000,18000,19000,20000,21000,22000,23000]
    massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)]
 if model==87:
    signal="cs_ct14nlo_"
    signalExtra="_LL-"
    signalMasses=[14000,15000,16000,17000,18000,19000,20000,22000,24000,26000,28000,30000]
    massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)]

 dire="/uscms_data/d3/jingyu/ChiAnalysis/DMlimits/CMSSW_8_0_25/src/cmsusercode/chi_analysis/"
 prefix="/uscms_data/d3/jingyu/ChiAnalysis/DMlimits/CMSSW_8_0_25/src/cmsusercode/chi_analysis/smearedDatacardsNov2/datacard_shapelimit13TeV"

 if model>=30 and model<60:
    name="pvalue_"+testStat+asym+signal+"_"+("_".join([s[0:4] for s in str(massbins).strip("[]").split("(")])).strip("_")    
 elif model>=100:  # Dark Matter
    signal=signalName[model]
    signalExtra=signalExtraName[model]
    #if float(signalExtraName[model].split("_")[2])<=2:
    #signalMasses=[1000,1500,1750,2000,2250,2500,3000,3500,4000,4500,5000,6000,7000]
    signalMasses=[2000,2250,2500,3000,3500,4000,4500,5000,6000]
    #signalMasses=[6000]
    includeSignalTheoryUncertainties=True # Assign QCD-only scale uncertainty to QCD+DM
    
    if isGen:
        dire="/uscms_data/d3/jingyu/ChiAnalysis/DMlimits/CMSSW_8_0_25/src/cmsusercode/chi_analysis/"
        prefix="/uscms_data/d3/jingyu/ChiAnalysis/DMlimits/CMSSW_8_0_25/src/cmsusercode/chi_analysis/invertMatrixOct20/datacard_shapelimit13TeV"
        #prefix="/uscms_data/d3/jingyu/ChiAnalysis/DMlimits/CMSSW_8_0_25/src/cmsusercode/chi_analysis/dAgostiniNoPdfOct20/datacard_shapelimit13TeV"
        #prefix="/uscms_data/d3/jingyu/ChiAnalysis/DMlimits/CMSSW_8_0_25/src/cmsusercode/chi_analysis/invertMatrixNoPdfOct20/datacard_shapelimit13TeV"
    elif isCB:
        dire="/uscms_data/d3/jingyu/ChiAnalysis/DMlimits/CMSSW_9_2_4/src/cmsusercode/chi_analysis/"
        #prefix="/uscms_data/d3/jingyu/ChiAnalysis/DMlimits/CMSSW_9_2_4/src/cmsusercode/chi_analysis/smearedDatacardsAug30/datacard_shapelimit13TeV"
        prefix="/uscms_data/d3/jingyu/ChiAnalysis/DMlimits/CMSSW_9_2_4/src/cmsusercode/chi_analysis/crystalBallSmearedAug30/datacard_shapelimit13TeV"
    else:
        dire="/uscms_data/d3/jingyu/ChiAnalysis/DMlimits/CMSSW_8_0_25/src/cmsusercode/chi_analysis/"
        prefix="/uscms_data/d3/jingyu/ChiAnalysis/DMlimits/CMSSW_8_0_25/src/cmsusercode/chi_analysis/smearedDatacardsNov2/datacard_shapelimit13TeV"
        #prefix="/uscms_data/d3/jingyu/ChiAnalysis/DMlimits/CMSSW_8_0_25/src/cmsusercode/chi_analysis/smearedDatacardsNoPdfOct20/datacard_shapelimit13TeV"
    if isInjection:
        prefix=prefix.replace("/datacard_","Injection0p75/datacard_")
    print prefix

    name="limits"+testStat+asym+str(model)+"_"+signal
   
    if isGen:
        name=name.replace("limits","limitsGen")
    elif isCB:
        name=name.replace("limits","limitsDetCB")
    else:
        name=name.replace("limits","limitsDet")
        
    if isInjection:
        name=name+"Injection0p75"
 else:
    name="limits"+testStat+asym+str(model)+"_"+signal  
 print name

 limits={}
 for signalMass in signalMasses:
    signalWithMass=signal+str(signalMass)+signalExtra
    print signalWithMass
    #cfg=open("chi_datacard13TeV"+str(model)+"_"+signalWithMass+"_2016.txt","w")
    if signalWithMass=="CIplusLL8000":
    	fname=prefix + '_GENnp-0-v4_chi2016.root'
    elif signalWithMass=="CIplusLL9000":
    	fname=prefix + '_GENnp-1-v4_chi2016.root'
    elif signalWithMass=="CIplusLL10000":
    	fname=prefix + '_GENnp-2-v4_chi2016.root'
    elif signalWithMass=="CIplusLL11000":
    	fname=prefix + '_GENnp-3-v4_chi2016.root'
    elif signalWithMass=="CIplusLL12000":
    	fname=prefix + '_GENnp-4-v4_chi2016.root'
    elif signalWithMass=="CIplusLL13000":
    	fname=prefix + '_GENnp-5-v4_chi2016.root'
    elif signalWithMass=="CIplusLL14000":
    	fname=prefix + '_GENnp-6-v4_chi2016.root'
    elif signalWithMass=="CIplusLL16000":
    	fname=prefix + '_GENnp-7-v4_chi2016.root'
    elif signalWithMass=="CIplusLL18000":
    	fname=prefix + '_GENnp-8-v4_chi2016.root'
    elif signalWithMass=="CIminusLL8000":
    	fname=prefix + '_GENnp-9-v4_chi2016.root'
    elif signalWithMass=="CIminusLL9000":
    	fname=prefix + '_GENnp-10-v4_chi2016.root'
    elif signalWithMass=="CIminusLL10000":
    	fname=prefix + '_GENnp-11-v4_chi2016.root'
    elif signalWithMass=="CIminusLL11000":
    	fname=prefix + '_GENnp-12-v4_chi2016.root'
    elif signalWithMass=="CIminusLL12000":
    	fname=prefix + '_GENnp-13-v4_chi2016.root'
    elif signalWithMass=="CIminusLL13000":
    	fname=prefix + '_GENnp-14-v4_chi2016.root'
    elif signalWithMass=="CIminusLL14000":
    	fname=prefix + '_GENnp-15-v4_chi2016.root'
    elif signalWithMass=="CIminusLL16000":
    	fname=prefix + '_GENnp-16-v4_chi2016.root'
    elif signalWithMass=="CIminusLL18000":
    	fname=prefix + '_GENnp-17-v4_chi2016.root'
    elif signalWithMass=="ADD6000":
        fname=prefix + '_GENnp-18-v5_chi2016.root'
    elif signalWithMass=="ADD7000":
        fname=prefix + '_GENnp-19-v5_chi2016.root'
    elif signalWithMass=="ADD8000":
        fname=prefix + '_GENnp-20-v5_chi2016.root'
    elif signalWithMass=="ADD9000":
        fname=prefix + '_GENnp-21-v5_chi2016.root'
    elif signalWithMass=="ADD10000":
        fname=prefix + '_GENnp-22-v5_chi2016.root'
    elif signalWithMass=="ADD11000":
        fname=prefix + '_GENnp-23-v5_chi2016.root'
    elif signalWithMass=="ADD12000":
        fname=prefix + '_GENnp-24-v5_chi2016.root'
    elif signalWithMass=="ADD13000":
        fname=prefix + '_GENnp-25-v5_chi2016.root'
    elif signalWithMass=="ADD14000":
        fname=prefix + '_GENnp-26-v5_chi2016.root'
    elif signalWithMass=="ADD15000":
        fname=prefix + '_GENnp-27-v5_chi2016.root'
    elif signalWithMass=="ADD16000":
        fname=prefix + '_GENnp-28-v5_chi2016.root'
    elif signalWithMass=="ADD17000":
        fname=prefix + '_GENnp-29-v5_chi2016.root'
    elif signalWithMass=="ADD18000":
        fname=prefix + '_GENnp-30-v5_chi2016.root'
    elif signalWithMass=="ADD19000":
        fname=prefix + '_GENnp-31-v5_chi2016.root'
    elif signalWithMass=="ADD20000":
        fname=prefix + '_GENnp-32-v5_chi2016.root'
    elif signalWithMass=="ADD21000":
        fname=prefix + '_GENnp-33-v5_chi2016.root'
    elif signalWithMass=="ADD22000":
        fname=prefix + '_GENnp-34-v5_chi2016.root'
    elif signalWithMass=="AntiCIplusLL12000":
        fname=prefix + '_GENnp-antici-v4_chi2016.root'
    elif signalWithMass=="QBH_"+str(signalMass)+"_6":
        fname=prefix + "_" + signalWithMass + "_chi2016.root"
    elif signalWithMass=="QBH_"+str(signalMass)+"_RS1":
        fname=prefix + "_" + signalWithMass + "_chi2016.root"
    elif "cs" in signal:
        fname=prefix+"_"+str(signalWithMass)+"_chi2016.root"
    elif "DM" in signal and version=="_v1":
      signalWithMass=signal+'_'+str(signalMass)+signalExtra
      fname=prefix+"_"+str(signalWithMass)+"_chi2016.root"
      fname=fname.replace("6000_3000","6000_2990").replace("7000_3000","7000_4000").replace("8000_3000","8000_3990")
      signalWithMass=signalWithMass.replace("6000_3000","6000_2990").replace("7000_3000","7000_4000").replace("8000_3000","8000_3990")
      if signalMass<=2000:
        massbins=[(2400,3000)]
      elif signalMass==2500:
        massbins=[(2400,3000)]
      elif signalMass==3000:
        massbins=[(2400,3000),(3000,3600)]
      elif signalMass==3500:
        massbins=[(3000,3600),(3600,4200)]
      elif signalMass==4000:
        massbins=[(3600,4200),(4200,4800)]
      elif signalMass==4500:
        massbins=[(4200,4800),(4800,5400)]
      elif signalMass==5000:
        massbins=[(4800,5400),(5400,6000)]
      elif signalMass>=6000:
        massbins=[(5400,6000),(6000,13000)]
    elif "DM" in signal and version=="_v2":
      signalWithMass=signal+'_'+str(signalMass)+signalExtra
      fname=prefix+"_"+str(signalWithMass)+"_chi2016.root"
      fname=fname.replace("6000_3000","6000_2990").replace("7000_3000","7000_4000").replace("8000_3000","8000_3990")
      signalWithMass=signalWithMass.replace("6000_3000","6000_2990").replace("7000_3000","7000_4000").replace("8000_3000","8000_3990")
      massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)]
    elif "DM" in signal and version=="_v3":
      signalWithMass=signal+'_'+str(signalMass)+signalExtra
      fname=prefix+"_"+str(signalWithMass)+"_chi2016.root"
      fname=fname.replace("6000_3000","6000_2990").replace("7000_3000","7000_4000").replace("8000_3000","8000_3990")
      signalWithMass=signalWithMass.replace("6000_3000","6000_2990").replace("7000_3000","7000_4000").replace("8000_3000","8000_3990")
      if signalMass<=1500:
        massbins=[(2400,3000)]
      elif signalMass<=2000:
        massbins=[(2400,3000),(3000,3600)]
      elif signalMass<=2500:
        massbins=[(2400,3000),(3000,3600),(3600,4200)]
      elif signalMass<=3000:
        massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000)]
      elif signalMass<=6000:
        massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)]
      elif signalMass<=7000:
        massbins=[(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)]
    elif "DM" in signal and version=="_v4":
      signalWithMass=signal+'_'+str(signalMass)+signalExtra
      fname=prefix+"_"+str(signalWithMass)+"_chi2016.root"
      fname=fname.replace("6000_3000","6000_2990").replace("7000_3000","7000_4000").replace("8000_3000","8000_3990")
      signalWithMass=signalWithMass.replace("6000_3000","6000_2990").replace("7000_3000","7000_4000").replace("8000_3000","8000_3990")
      if signalMass<=1500:
        massbins=[(2400,3000)]
      elif signalMass<=2000:
        massbins=[(2400,3000)]
      elif signalMass<=2500:
        massbins=[(2400,3000),(3000,3600),(3600,4200)]
      elif signalMass<=3000:
        massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,4800)]
      elif signalMass<=3500:
        massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,5400)]
      elif signalMass<=4000:
        massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000)]
      elif signalMass<=4500:
        massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)]  
      elif signalMass<=5000:
        massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)]
      elif signalMass<=6000:
        massbins=[(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)]
    elif "DM" in signal and version=="_v5":
      signalWithMass=signal+'_'+str(signalMass)+signalExtra
      fname=prefix+"_"+str(signalWithMass)+"_chi2016.root"
      fname=fname.replace("6000_3000","6000_2990").replace("7000_3000","7000_4000").replace("8000_3000","8000_3990")
      signalWithMass=signalWithMass.replace("6000_3000","6000_2990").replace("7000_3000","7000_4000").replace("8000_3000","8000_3990")
      if signalMass<=2500:
        massbins=[(2400,3000)]
      elif signalMass<=3000:
        massbins=[(2400,3000),(3000,3600)]
      elif signalMass<=3500:
        massbins=[(2400,3000),(3000,3600),(3600,4200)]
      elif signalMass<=4000:
        massbins=[(2400,3000),(3000,3600),(3600,4200)]
      elif signalMass<=4500:
        massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,4800)]  
      elif signalMass<=5000:
        massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000)]
      elif signalMass<=6000:
        massbins=[(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)]
    print fname
    if not "DM" in signal and not "cs" in signal and not "QBH" in signal:
        signalWithMass="QCD"+signalWithMass
    f=TFile(fname)
    cfg=open("chi_datacard13TeV"+str(model)+"_"+signalWithMass.replace("QCD","")+"_2016.txt","w")
    cfg.writelines("""
imax """+str(len(massbins))+""" number of channels
jmax 2 number of backgrounds
kmax """+str(3+jesSources+1*separateScaleUncertainties)+""" number of nuisance parameters""")
    cfg.writelines("""
-----------
""")
    for i in range(len(massbins)):
        if injectSignal:
          cfg.writelines("""shapes data_obs bin"""+str(i)+""" """+prefix+dataWithSignal+""" data_obs#chi"""+str(massbins[i][0])+"""_"""+str(massbins[i][1])+"""_rebin1 data_obs#chi"""+str(massbins[i][0])+"""_"""+str(massbins[i][1])+"""_rebin1_$SYSTEMATIC
""")
        cfg.writelines("""shapes * bin"""+str(i)+""" """+fname+""" $PROCESS#chi"""+str(massbins[i][0])+"""_"""+str(massbins[i][1])+"""_rebin1 $PROCESS#chi"""+str(massbins[i][0])+"""_"""+str(massbins[i][1])+"""_rebin1_$SYSTEMATIC
""")
    cfg.writelines("""
-----------
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
    if jesSources>1:
     for n in range(jesSources):
      text+="\njes"+str(n+1)+" shape "
      for i in range(len(massbins)):
         text+="1 1 - "
    else:
      text+="\njes shape "
      for i in range(len(massbins)):
         text+="1 1 - "
    text+="\npdf shape "
    for i in range(len(massbins)):
      if includeSignalTheoryUncertainties:
       text+="1 1 - "
      else:
       text+="- 1 - "
    if separateScaleUncertainties:
      text+="\nscaleMuR shape "
      for i in range(len(massbins)):
        if includeSignalTheoryUncertainties:
         text+="1 1 - "
        else:
         text+="- 1 - "
      text+="\nscaleMuF shape "
      for i in range(len(massbins)):
        if includeSignalTheoryUncertainties:
         text+="1 1 - "
        else:
         text+="- 1 - "
    else:
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

    out=system_call("cp "+dire+"HiggsJPC.py ${CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/python")
    out=system_call("text2workspace.py -m "+str(signalMass)+" chi_datacard13TeV"+str(model)+"_"+signalWithMass.replace("QCD","")+"_2016.txt -P HiggsAnalysis.CombinedLimit.HiggsJPC:twoHypothesisHiggs -o fixedMu_"+signalWithMass.replace("QCD","")+".root")
    
    if testStat=="LEP":
     poi=""
     add=""
     method=testStat+" --singlePoint 1.0"
     ntoys=30000
    if testStat=="LHC":
     poi=" --redefineSignalPOIs x" # -H ProfileLikelihood
     method=testStat+" --frequentist"
     add="LHC"
     ntoys=1000
    if testStat=="TEV":
     poi=" --redefineSignalPOIs x"
     add=""
     method=testStat+" --singlePoint 1.0"
     ntoys=30000
    
    if asym:
     if "limit" in name:
      out=system_call("combine -m "+str(signalMass)+" -M Asymptotic -n "+signal+signalExtra+" fixedMu_"+signalWithMass.replace("QCD","")+".root")
      # -H ProfileLikelihood
      f = open(name+"_exp_"+str(signalMass)+"_2016"+version+".txt","w");f.write(out);f.close()
     else: 
      out=system_call("combine --signif -m "+str(signalMass)+" -M ProfileLikelihood -n "+signal+signalExtra+" fixedMu_"+signalWithMass.replace("QCD","")+".root")
      f = open(name+"_exp_"+str(signalMass)+"_2016"+version+".txt","w");f.write(out);f.close()

    elif testStat=="LHC":
     
     for point in [0.1,0.2,0.4,0.6,0.8,1.0,1.3,1.6,2.0,5.0,10.0]:
       out=system_call("combine -m "+str(signalMass)+" -M HybridNew --rule CLs --saveHybridResult --singlePoint "+str(point)+" -s 10000"+str(int(point*100))+" --saveToys --testStat "+method+poi+" --fork 4 -T "+str(ntoys)+" -i 2 --clsAcc 0 -n "+signal+signalExtra+" fixedMu_"+signalWithMass.replace("QCD","")+".root")
       f = open(name+"_"+str(signalMass)+str(point)+"_2016"+version+".txt","w");f.write(out);f.close()
     system_call("hadd -f grid_mX"+str(signalMass)+"_"+signal+signalExtra+".root higgsCombine"+signal+signalExtra+".HybridNew.mH"+str(signalMass)+".10000*.root")

     system_call("combine -M HybridNew --frequentist --grid grid_mX"+str(signalMass)+"_"+signal+signalExtra+".root -m "+str(signalMass) + " -n "+signal+signalExtra+" fixedMu_"+signalWithMass.replace("QCD","")+".root &> "+name+"_"+str(signalMass)+"_2016"+version+".txt")
     system_call("combine -M HybridNew --frequentist --grid grid_mX"+str(signalMass)+"_"+signal+signalExtra+".root -m "+str(signalMass) + " -n "+signal+signalExtra+" --expectedFromGrid 0.5 fixedMu_"+signalWithMass.replace("QCD","")+".root &> "+name+"_exp_"+str(signalMass)+"_2016"+version+".txt")
     system_call("combine -M HybridNew --frequentist --grid grid_mX"+str(signalMass)+"_"+signal+signalExtra+".root -m "+str(signalMass) + " -n "+signal+signalExtra+" --expectedFromGrid 0.84 fixedMu_"+signalWithMass.replace("QCD","")+".root &>> "+name+"_exp_"+str(signalMass)+"_2016"+version+".txt")
     system_call("combine -M HybridNew --frequentist --grid grid_mX"+str(signalMass)+"_"+signal+signalExtra+".root -m "+str(signalMass) + " -n "+signal+signalExtra+" --expectedFromGrid 0.16 fixedMu_"+signalWithMass.replace("QCD","")+".root &>> "+name+"_exp_"+str(signalMass)+"_2016"+version+".txt")
     system_call("combine -M HybridNew --frequentist --grid grid_mX"+str(signalMass)+"_"+signal+signalExtra+".root -m "+str(signalMass) + " -n "+signal+signalExtra+" --expectedFromGrid 0.975 fixedMu_"+signalWithMass.replace("QCD","")+".root &>> "+name+"_exp_"+str(signalMass)+"_2016"+version+".txt")
     system_call("combine -M HybridNew --frequentist --grid grid_mX"+str(signalMass)+"_"+signal+signalExtra+".root -m "+str(signalMass) + " -n "+signal+signalExtra+" --expectedFromGrid 0.025 fixedMu_"+signalWithMass.replace("QCD","")+".root &>> "+name+"_exp_"+str(signalMass)+"_2016"+version+".txt")

    else:
    
     out=system_call("combine -m "+str(signalMass)+" -M HybridNew --rule CLs --saveHybridResult --testStat "+method+poi+" --fork 4 -T "+str(ntoys)+" --clsAcc 0.1 -n "+signal+signalExtra+" fixedMu_"+signalWithMass.replace("QCD","")+".root")
     f = open(name+"_"+str(signalMass)+"_2016"+version+".txt","w");f.write(out);f.close()
    
     out=system_call('root -q -b higgsCombine'+signal+signalExtra+'.HybridNew.mH'+str(signalMass)+'.root "${CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/test/plotting/hypoTestResultTree.cxx(\\"qmu_'+signal+str(signalMass)+signalExtra+'_'+testStat+version+'.root\\",'+str(signalMass)+',1,\\"x\\")"')
    
     out=system_call('root -q -b '+dire+'"extractSignificanceStats'+add+'.C(\\"'+signal+str(signalMass)+signalExtra+'_'+testStat+version+'\\")"')
     f = open(name+'_exp_'+str(signalMass)+'_2016'+version+'.txt',"w");f.write(out);f.close()
    
    # diagnostics
    diagnostic=True
    if diagnostic:
      out=system_call("mkdir "+name+version)
      out=system_call("combine -m "+str(signalMass)+" -M MaxLikelihoodFit "+poi+" --plots --out "+name+version+" -n "+signalWithMass.replace("QCD","")+" fixedMu_"+signalWithMass.replace("QCD","")+".root")
      out=system_call("python diffNuisances.py -p x -a "+name+version+"/mlfit"+signalWithMass.replace("QCD","")+".root -A")
      print out

 for signalMass in signalMasses:
    limits[signalMass]=[]
    if testStat!="LEP" and (testStat!="LHC" or asym!=""):
     fname=name+"_exp_"+str(signalMass)+"_2016"+version+".txt"
    else:
     fname=name+"_"+str(signalMass)+"_2016"+version+".txt"
    try:
      print "open",fname
      f=file(fname)
    except:
      print "file not found", fname
      continue
    for line in f.readlines():
        if "Observed Limit" in line and asym:
           limits[signalMass]=[signalMass,float(line.strip().split(" ")[-1]),0]
        if "CLs = " in line and testStat=="LEP":
           limits[signalMass]=[signalMass,float(line.strip().split(" ")[-3]),float(line.strip().split(" ")[-1])]
        if "Observed CLs = " in line and testStat!="LEP":
           limits[signalMass]=[signalMass,float(line.strip().split(" ")[-1]),0]
        if "Limit:" in line and "95% CL" in line and testStat=="LHC" and asym=="":
           limits[signalMass]=[signalMass,float(line.strip().split(" ")[3]),0]
        if "Significance:" in line and asym:
           print "observed signficance (p-value): ",line.strip().split(" ")[-1].strip(")")
        if "CLb = " in line and testStat=="LEP":
           print "observed signficance (p-value): ",ROOT.Math.normal_quantile_c((1.-float(line.strip().split(" ")[-3]))/2.,1),"(",(1.-float(line.strip().split(" ")[-3])),")"
        if "Observed CLb = " in line and testStat!="LEP":
           print "observed signficance (p-value): ",ROOT.Math.normal_quantile_c((1.-float(line.strip().split(" ")[-1]))/2.,1),"(",(1.-float(line.strip().split(" ")[-1])),")"
    if len(limits[signalMass])==0:
         limits[signalMass]+=[signalMass,0,0]
    try:
      fname=name+"_exp_"+str(signalMass)+"_2016"+version+".txt"
      f=file(fname)
    except:
      print "file not found", fname
      continue
    for line in f.readlines():
        if "Expected" in line and asym:
           limits[signalMass]+=[float(line.strip().split(" ")[-1])]
        if "Expected CLs" in line:
	  try:
           limits[signalMass]+=[float(line.strip().split(" ")[-1])]
	  except:
           print "didn't find one point"
        if "Limit:" in line and "95% CL" in line and testStat=="LHC" and asym=="":
           limits[signalMass]+=[float(line.strip().split(" ")[3])]
    for i in range(len(limits[signalMass]),8):
         limits[signalMass]+=[0]

 if asym: # reorder expected limits to exp,-1,+1,-2,+2
   for signalMass in signalMasses:
     limits[signalMass]=[limits[signalMass][0],limits[signalMass][1],limits[signalMass][2],limits[signalMass][5],limits[signalMass][6],limits[signalMass][4],limits[signalMass][7],limits[signalMass][3]]

 print limits
 name=name+"_2016"+version+".txt"
 f=file(name,"w")
 f.write(str([limits[signalMass] for signalMass in signalMasses]))
 f.close()
