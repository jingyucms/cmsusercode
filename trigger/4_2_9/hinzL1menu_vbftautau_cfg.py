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
    nPrintStatusEvery = 1000; # print out status every n events processed
    menuTag  = "HLT_Menu";
    alcaCondition = "startup";
    versionTag  = "20110831_DS_5e33"; 
    isRealData = false;
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
# lumiScaleFactor = 2413.95; # = 1e34/4.5629e30 * 1.10146 because OHLT tree only contains LS 291-443
 lumiScaleFactor = 1689.76; # = 7e33/4.5629e30 * 1.10146 because OHLT tree only contains LS 291-443
# lumiScaleFactor = 1206.97; # = 5e33/4.5629e30 * 1.10146 because OHLT tree only contains LS 291-443
 #lumiScaleFactor = 1;
 prescaleNormalization = 1;#consistent with singleEG12 passthrough (precal 1(L1)* prescal 1 (HLT))

#run 178208
runLumiblockList = ( 
    (1, 0, 100000)
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
 names = ["htautau"];
 fnames = ["openhlt_*.root"];

## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__BTag_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__Commissioning_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__Cosmics_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__DoubleElectron_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__DoubleMu_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r173236__ElectronHad_Run2011A-PromptReco-v6__20110827_1346/"];
## paths = ["/home/llr/cms/paganini/openhlt_r178208_Commissioning/"];
#paths = ["rfio:/castor/cern.ch/user/l/lucieg/OpenHLT/Commish2011/r178208__L1EGHPF_Run2011B-v1__20111011_1309/"];
paths = ["file:/tmp/hinzmann/"];
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

 preFilterByBits = "offline";

  # (TriggerName, Prescale, EventSize)
 triggers = (
    ("OpenL1_ZeroBias", 1, 1.),
    ("HLT_L1SingleEG12_v3", 1, 1.),
    ("OpenL1_SingleEG22", 1, 1.),
    ("OpenL1_DoubleEG15_5", 1, 1.),
    #("OpenL1_SingleEG25", 1, 1.),
    #("OpenL1_DoubleEG17_5", 1, 1.),
    #("OpenL1_SingleEG18", 1, 1.),
    ("OpenL1_EG18_CenJet28OrTauJet28", 1, 1.),
    ("HLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20", 1, 1.),
    ("OpenHLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_LooseIsoPFTau20", 1, 1.),
    ("OpenHLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20", 1, 1.),
    ("OpenHLT_Ele20_CaloIdVT_TrkIdT_TrkIsoT_MediumIsoPFTau20", 1, 1.),
    ("OpenHLT_Ele20_CaloIdVT_TrkIdT_TrkIsoT_LooseIsoPFTau20", 1, 1.),
    ("OpenHLT_Ele20Eta2p1_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20", 1, 1.),
    ("OpenHLT_Ele20Eta1p5_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20", 1, 1.),
    ("OpenHLT_Ele20Eta1p0_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20", 1, 1.),
    ("OpenHLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20Eta2p1", 1, 1.),
    ("OpenHLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20Eta1p5", 1, 1.),
    ("OpenHLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20Eta1p0", 1, 1.),
    ("OpenHLT_Ele20Eta2p1_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_LooseIsoPFTau20", 1, 1.),
    ("OpenHLT_Ele20Eta1p5_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_LooseIsoPFTau20", 1, 1.),
    ("OpenHLT_Ele20Eta1p0_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_LooseIsoPFTau20", 1, 1.),
    ("OpenHLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_LooseIsoPFTau20Eta2p1", 1, 1.),
    ("OpenHLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_LooseIsoPFTau20Eta1p5", 1, 1.),
    ("OpenHLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_LooseIsoPFTau20Eta1p0", 1, 1.)
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
  selectBranchMC = true; 
};


### eof
