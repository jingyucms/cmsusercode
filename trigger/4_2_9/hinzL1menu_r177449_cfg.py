#------------------------------------------------------
# Configuration file for Rate & Efficiency calculations
#------------------------------------------------------
# This version is compliant with RateEff-02-XX-XX
# using logical parser for L1 seeds
#

##########################################
# General Menu & Run conditions
##########################################
run:{
    nEntries = -1;
    nPrintStatusEvery = 10000; # print out status every n events processed
    menuTag  = "HLT_Menu";
    alcaCondition = "startup";
    versionTag  = "20110831_DS_5e33"; 
    isRealData = true;
    doPrintAll = true;
    doDeterministicPrescale =true;
    dsList = "Datasets.list";
    readRefPrescalesFromNtuple = true;

};

########################################## 
# Run information for real data 
########################################## 
data:{ 
 # Enter the length of 1 lumi section and prescale factor of the dataset
 lumiSectionLength = 23.3;
# lumiScaleFactor = 3.739; # = 1e34/2.67e33 / 0.3087 for missing files?
 lumiScaleFactor = 2.617; # = 7e33/2.67e33 / 0.3087 for missing files?
# lumiScaleFactor = 1.870; # = 5e33/2.67e33 / 0.3087 for missing files?
 #lumiScaleFactor = 1;
 prescaleNormalization = 13200;#consistent with singleEG12 passthrough (precal 60(L1)* prescal 220 (HLT))

##run 177449
runLumiblockList = ( 
    (177449, 236, 392),
    (177449, 394, 434)
  );



};

##########################################
# Beam conditions
##########################################
beam:{
 bunchCrossingTime = 50.0E-09; # Design: 25 ns Startup: 75 ns
 iLumi = 1; # 3E33 no impact on result?
 maxFilledBunches = 3564;
 nFilledBunches = 800;
 cmsEnergy = 7.; # Collision energy in TeV
};

##########################################
# Samples & Processes
##########################################
process:{
 isPhysicsSample = [0]; #Must be an int type
 names = ["minbias"];
 fnames = ["openhlt_*.root"];

## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__BTag_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__Commissioning_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__Cosmics_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__DoubleElectron_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__DoubleMu_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__ElectronHad_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["/home/llr/cms/paganini/openhlt_r178208_Commissioning/"];
paths = ["file:/tmp/hinzmann/"];
#paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r177449__Commissioning_Run2011B-v1__20111011_0948/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__Jet_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__MinimumBias_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__MET_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__MuOnia_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__MultiJet_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__MuEG_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__MuHad_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__Photon_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__PhotonHad_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__SingleElectron_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__SingleMu_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__Tau_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__TauPlusX_Run2011A-PromptReco-v6__20110827_1346/"];

doMuonCuts = [false];
 doElecCuts = [false];
 sigmas = [9.87E08]; # xsecs * filter efficiencies for QCD 15
};


##########################################
# Menu
##########################################
menu:{
 isL1Menu = true; 
 doL1preloop = false; 

 preFilterByBits = "HLT_L1SingleEG12_v3";

  # (TriggerName, Prescale, EventSize)
 triggers = (
    ("OpenL1_SingleEG22", 1, 1.),
    ("OpenL1_DoubleEG15_5", 1, 1.),
    #("OpenL1_SingleEG25", 1, 1.),
    #("OpenL1_DoubleEG17_5", 1, 1.),
    #("OpenL1_SingleEG18", 1, 1.),
    ("OpenL1_EG18_CenJet28OrTauJet28", 1, 1.),
    ("OpenHLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_LooseIsoPFTau20", 1, 1.),
    ("OpenHLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20", 1, 1.)
 );
 
 
};

##########################################
#
# Only for experts:
# Select certain branches to speed up code.
# Modify only if you know what you do!
#
##########################################
branch:{
  doSelectBranches = true; #only set to true if you really know what you do!
  selectBranchL1 = true; 
  selectBranchHLT = true;
  selectBranchOpenHLT = true; 
  selectBranchReco = true;
  selectBranchL1extra = true; 
  selectBranchMC = false; 
};


### eof
