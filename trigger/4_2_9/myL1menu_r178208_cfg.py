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
 lumiScaleFactor = 2413.95; # = 1e34/4.5629e30 * 1.10146 because OHLT tree only contains LS 291-443
 #lumiScaleFactor = 1;
 prescaleNormalization = 1;#consistent with singleEG12 passthrough (precal 1(L1)* prescal 1 (HLT))

##run 178208
runLumiblockList = ( 
    (178208, 2, 449)
  );



};

##########################################
# Beam conditions
##########################################
beam:{
 bunchCrossingTime = 50.0E-09; # Design: 25 ns Startup: 75 ns
 iLumi = 3E33;
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
paths = ["/home/llr/cms/paganini/openhlt_r178208_Commissioning/"];
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

 preFilterByBits = "HLT_L1SingleEG12_v1";

  # (TriggerName, Prescale, EventSize)
 triggers = (
    #("L1_SingleEG12", 1, 1.),
    #("L1_SingleEG15", 1, 1.),
    #("L1_SingleEG18", 1, 1.),
    #("OpenL1_EG18", 1, 1.),
    #("L1_SingleEG20", 1, 1.),
    #("L1_SingleEG30", 1, 1.),
    #("OpenL1_EG24", 1, 1.),
    #("OpenL1_DoubleEG18_8", 1, 1.),
    ("OpenL1_EG25", 1, 1.),
    ("OpenL1_DoubleEG17_5", 1, 1.),
    #("OpenL1_EG18ETM10", 1, 1.),
    #("OpenL1_EG18ETM15", 1, 1.),
    #("OpenL1_EG18ETM20", 1, 1.),
    #("OpenL1_EG18ETM25", 1, 1.),
    #("OpenL1_EG18ETM30", 1, 1.),
    #("OpenL1_EG18CenJet4", 1, 1.),
    #("OpenL1_EG18CenJet8", 1, 1.),
    #("OpenL1_EG18CenJet24", 1, 1.),
    #("OpenL1_EG18CenJet20", 1, 1.),
    #("OpenL1_EG18CenJet16", 1, 1.),
    #("OpenL1_EG18CenJet12", 1, 1.),    
    #("OpenL1_EG20CenJet4", 1, 1.),
    #("OpenL1_EG20CenJet8", 1, 1.),
    #("OpenL1_EG20CenJet12", 1, 1.),
    #("OpenL1_EG20CenJet16", 1, 1.),
    #("L1_SingleJet16", 1, 1.),
    #("OpenL1_SingleJet36", 1, 1.),
    #("OpenL1_EG18_SingleJet4", 1, 1.),
    #("OpenL1_EG18_CenTauJet4", 1, 1.),
    #("OpenL1_EG18_CenTauJet8", 1, 1.),
    #("OpenL1_EG18_CenTauJet12", 1, 1.),
    #("OpenL1_EG18_CenTauJet16", 1, 1.),
    #("OpenL1_EG18_CenTauJet20", 1, 1.)
    #("L1_SingleJet36", 1, 1.)
    #("OpenL1_EG18_CenJet4OrTauJet4", 1, 1.),
    #("OpenL1_EG20_CenJet32OrTauJet32", 1, 1.),
    #("OpenL1_EG18_CenJet36OrTauJet36", 1, 1.)
    ("OpenL1_EG18_CenJet32OrTauJet32", 1, 1.),
    #("OpenL1_EG18_CenJet28OrTauJet28", 1, 1.)
    #("OpenL1_EG18_CenJet24OrTauJet24", 1, 1.),
    #("OpenL1_EG18_CenJet20OrTauJet20", 1, 1.),
    #("OpenL1_EG18_CenJet24OrTauJet16", 1, 1.),
    #("OpenL1_EG18_CenJet20OrTauJet16", 1, 1.),
    #("OpenL1_EG18_CenJet16OrTauJet16", 1, 1.)
    #("OpenL1_EG18_CenTauJet24_Jet24", 1, 1.)
    #("OpenL1_EG18_CenTauJet20_Jet20", 1, 1.)
    #("OpenL1_EG18_CenTauJet16_Jet16", 1, 1.)
    #("OpenL1_EG15_CenTauJet20_Jet20", 1, 1.)
    #("OpenL1_EG15_CenTauJet24_Jet24", 1, 1.)
    ("OpenL1_EG15_CenTauJet28_Jet28", 1, 1.)
    #("OpenL1_EG15_CenTauJet20_CenTauJet20", 1, 1.)
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
