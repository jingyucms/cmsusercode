#!/bin/sh

startn=0
endn=0
n=${startn}
while [ $n -le $endn ]
do

startm=0
endm=0
m=${startm}
while [ $m -le $endm ]
do

  dir=pythia6_QCD

  echo ********file ${dir}
  
  py=${dir}.py

  echo ********Creating ${py}

cat > ${py} <<EOF

import FWCore.ParameterSet.Config as cms

process = cms.Process("PFAOD")

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100000) )

process.load("Configuration.EventContent.EventContent_cff")
process.out = cms.OutputModule(
    "PoolOutputModule",
    process.AODSIMEventContent,
    fileName = cms.untracked.string('/tmp/hinzmann/${dir}_PFAOD.root'),
    )

process.load("CommonTools.ParticleFlow.PF2PAT_EventContent_cff")
process.out.outputCommands.extend( process.prunedAODForPF2PATEventContent.outputCommands )

# additional stuff for Maxime: 
process.out.outputCommands.extend(
    [
      'keep GenEventInfoProduct_*_*_*',
      'keep *_ak5GenJets_*_*',
      'keep *_ak5CaloJets_*_*',
      'keep *_ak5JetID_*_*',
      'keep *_ak5JetExtender_*_*',
      'keep *_ak7GenJets_*_*',
      'keep *_ak7CaloJets_*_*',
      'keep *_ak7JetID_*_*',
      'keep *_ak7JetExtender_*_*',
      #------- PFJet collections --------
      'keep *_kt6PFJets_rho_*',
      'keep *_kt6PFJets_sigma_*',
      'keep *_ak5PFJets_*_*',
      'keep *_ak7PFJets_*_*',
      #------- Trigger collections ------
      'keep edmTriggerResults_TriggerResults_*_*',
      'keep *_hltTriggerSummaryAOD_*_*',
      'keep L1GlobalTriggerObjectMapRecord_*_*_*',
      'keep L1GlobalTriggerReadoutRecord_*_*_*',
      #------- Various collections ------
      'keep *_EventAuxilary_*_*',
      'keep *_offlinePrimaryVertices_*_*',
      'keep *_offlinePrimaryVerticesWithBS_*_*',
      #------- MET collections ----------
      'keep *_met_*_*',
      'keep *_pfMet_*_*'
    ])

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('FastSimulation.Configuration.EventContent_cff')
process.load('FastSimulation.PileUpProducer.PileUpSimulator_NoPileUp_cff')
process.load('FastSimulation.Configuration.Geometries_START_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('FastSimulation.Configuration.FamosSequences_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedParameters_cfi')
process.load('FastSimulation.Configuration.HLT_GRun_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('PRIVAT'),
    annotation = cms.untracked.string('PRIVAT'),
    name = cms.untracked.string('PRIVAT')
)

process.famosSimHits.SimulateCalorimetry = True
process.famosSimHits.SimulateTracking = True
process.Realistic7TeV2011CollisionVtxSmearingParameters.type = cms.string("BetaFunc")
process.famosSimHits.VertexGenerator = process.Realistic7TeV2011CollisionVtxSmearingParameters
process.famosPileUp.VertexGenerator = process.Realistic7TeV2011CollisionVtxSmearingParameters

# Input source
process.source = cms.Source("EmptySource")
# Other statements
process.GlobalTag.globaltag = 'START42_V12::All'

process.MessageLogger=cms.Service("MessageLogger",
    destinations = cms.untracked.vstring('logs'),
    logs = cms.untracked.PSet(threshold=cms.untracked.string('WARNING'))
)

from Configuration.Generator.PythiaUEZ2Settings_cfi import *

process.generator = cms.EDFilter("Pythia6GeneratorFilter",
	pythiaHepMCVerbosity = cms.untracked.bool(False),
	maxEventsToPrint = cms.untracked.int32(0),
	pythiaPylistVerbosity = cms.untracked.int32(0),
	filterEfficiency = cms.untracked.double(1),
	comEnergy = cms.double(7000.0),
	crossSection = cms.untracked.double(1e10),
	
	PythiaParameters = cms.PSet(
	        pythiaUESettingsBlock,
		processParameters = cms.vstring(
		        'MSEL = 1',
		        'CKIN(3) = 100',
		        'CKIN(4) = 3000',
#		        'MSTP(142) = 2',
		),
#		CSAParameters = cms.vstring(
#		        'CSAMODE = 7',
#		        'PTPOWER = 4.5',
#		),
		parameterSets = cms.vstring(
		        'pythiaUESettings',
		        'processParameters',
#			'CSAParameters',
			)
	)
)

process.pfPileUp.PFCandidates=cms.InputTag("particleFlow")
process.pfNoPileUp.bottomCollection=cms.InputTag("particleFlow")
process.pfPileUpCandidates.bottomCollection=cms.InputTag("particleFlow")

# Path and EndPath definitions
process.p = cms.Path(process.generator*process.pgen*process.simulationWithFamos*process.reconstructionWithFamos)
process.endpath = cms.EndPath(process.out)
process.schedule = cms.Schedule(process.p,process.endpath)

EOF

  cfg=crab.cfg

  echo ********Creating ${cfg}

cat > ${cfg} <<EOF

[CRAB]
jobtype=cmssw
scheduler=glite
#server_name=pisa
#server_name=rwth
#server_name=bari
#server_name=cern

[CMSSW]
datasetpath=None

pset=${dir}.py
total_number_of_events=3000000
events_per_job=100000
output_file=chi.root
#get_edm_output=1


[USER]
copy_data             =1
return_data           =0
storage_element       =srm-cms.cern.ch
storage_path=/srm/managerv2?SFN=/castor/cern.ch
user_remote_dir=/cms/store/cmst3/user/hinzmann/${dir}
thresholdLevel=100
eMail=hinzmann@cern.ch
ui_working_dir=${dir}

[GRID]
rb=CERN 
proxy_server=myproxy.cern.ch 
#group=dcms
#SE_white_list=T2_DE_DESY, T2_DE_RWTH
#CE_white_list=T2_DE_DESY, T2_DE_RWTH
#SE_black_list=cmsdca2.fnal.gov
#CE_black_list=fnal
#additional_jdl_parameters=rank=-other.GlueCEStateEstimatedResponseTime+(RegExp("rwth-aachen.de",other.GlueCEUniqueID)?99999:0)+(RegExp("desy.de",other.GlueCEUniqueID)?100000:0)
#additional_jdl_parameters=rank=-other.GlueCEStateEstimatedResponseTime+(RegExp("rwth-aachen.de",other.GlueCEUniqueID)?99999:0)

EOF

  echo ********Running ${cfg}
  
#crab -create -submit
#cmsRun ${py}
#cmsStage -f /tmp/hinzmann/${dir}_PFAOD.root /store/cmst3/user/hinzmann/fastsim/

  pycmg=${dir}_CMG.py

  echo ********Creating ${pycmg}

cat > ${pycmg} <<EOF

## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *

### MASTER FLAGS  ######################################################################

# turn this on if you want to pick a relval in input (see below)
pickRelVal = False

# turn on when running on MC
runOnMC = True

# AK5 sequence with no cleaning is the default
# the other sequences can be turned off with the following flags.
#JOSE: no need to run these guys for what you are up to
runAK5LC = False
runAK7 = False
runCA8 = True

#COLIN: will need to include the event filters in tagging mode

#COLIN : reactivate HPS when bugs corrected
hpsTaus = True

#COLIN: the following leads to rare segmentation faults
doJetPileUpCorrection = True

#patTaus can now be saved even when running the CMG sequence.
doEmbedPFCandidatesInTaus = True

runCMG = True


#add the L2L3Residual corrections only for data
if runOnMC:#MC
    jetCorrections=['L1FastJet','L2Relative','L3Absolute']
else:#Data
    jetCorrections=['L1FastJet','L2Relative','L3Absolute','L2L3Residual']

# process.load("CommonTools.ParticleFlow.Sources.source_ZtoMus_DBS_cfi")
#process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True))

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = 10

sep_line = "-" * 50
print sep_line
print 'running the following PF2PAT+PAT sequences:'
print '\tAK5'
if runAK5LC: print '\tAK5LC'
if runAK7: print '\tAK7'
if runCA8: print '\tCA8'
print 'embedding in taus: ', doEmbedPFCandidatesInTaus
print 'HPS taus         : ', hpsTaus
print 'produce CMG tuple: ', runCMG
print sep_line


### SOURCE DEFINITION  ################################################################


# process.source.fileNames = cms.untracked.vstring(['/store/relval/CMSSW_4_2_5/RelValTTbar/GEN-SIM-RECO/START42_V12-v1/0113/1C538A2F-799E-E011-8A7E-0026189438BD.root'])

process.source.fileNames = cms.untracked.vstring(['/store/cmst3/user/hinzmann/graviton/${dir}_PFAOD.root'])
#process.source.fileNames = cms.untracked.vstring(['file:pythia6_gravitonWW_1000_PFAOD.root'])

# process.load("CMGTools.Common.sources.SingleMu.Run2011A_May10ReReco_v1.AOD.source_cff")
#process.load("CMGTools.Common.sources.HT.Run2011A_May10ReReco_v1.AOD.V2.source_cff")
# process.load("CMGTools.Common.sources.VBF_HToTauTau_M_115_7TeV_powheg_pythia6_tauola.Summer11_PU_S4_START42_V11_v1.AODSIM.V2.source_cff")

if pickRelVal:
    process.source = cms.Source(
        "PoolSource",
        fileNames = cms.untracked.vstring(
        pickRelValInputFiles( cmsswVersion  = 'CMSSW_4_3_0_pre2'
                              , relVal        = 'RelValZmumuJets_Pt_20_300PU1'
                              , globalTag     = 'MC_42_V9_PU_E7TeV_AVE_2_BX2808'
                              , numberOfFiles = -1
                              )
        )
        )


# print "WARNING!!!!!!!!!!!!!!!! remove the following line (see .cfg) before running on the batch!"
process.source.fileNames = process.source.fileNames[:12]

print 'PF2PAT+PAT+CMG for files:'
print process.source.fileNames

### DEFINITION OF THE PF2PAT+PAT SEQUENCES #############################################

from CMGTools.Common.Tools.getGlobalTag import getGlobalTag
process.GlobalTag.globaltag = cms.string(getGlobalTag(runOnMC))

# load the PAT config
process.load("PhysicsTools.PatAlgos.patSequences_cff")
process.out.fileName = cms.untracked.string('/tmp/hinzmann/${dir}_patTuple_PF2PAT.root')

# Configure PAT to use PF2PAT instead of AOD sources
# this function will modify the PAT sequences. It is currently 
# not possible to run PF2PAT+PAT and standart PAT at the same time
from PhysicsTools.PatAlgos.tools.pfTools import *

# ---------------- Sequence AK5 ----------------------


process.eIdSequence = cms.Sequence()

# PF2PAT+PAT sequence 1:
# no lepton cleaning, AK5PFJets

postfixAK5 = "AK5"
jetAlgoAK5="AK5"

#COLIN : we will need to add the L2L3Residual when they become available! also check the other calls to the usePF2PAT function. 
usePF2PAT(process,runPF2PAT=True, jetAlgo=jetAlgoAK5, runOnMC=runOnMC, postfix=postfixAK5,
          jetCorrections=('AK5PFchs', jetCorrections))


if doJetPileUpCorrection:
    from CommonTools.ParticleFlow.Tools.enablePileUpCorrection import enablePileUpCorrection
    enablePileUpCorrection( process, postfix=postfixAK5)

#configure the taus
from CMGTools.Common.PAT.tauTools import *
if doEmbedPFCandidatesInTaus:
    embedPFCandidatesInTaus( process, postfix=postfixAK5, enable=True )
if hpsTaus:
    adaptPFTaus(process,"hpsPFTau",postfix=postfixAK5)
    #  note that the following disables the tau cleaning in patJets
    adaptSelectedPFJetForHPSTau(process,jetSelection="pt()>15.0",postfix=postfixAK5)
    # currently (Sept 27,2011) there are three sets of tau isolation discriminators better to choose in CMG tuples.
    removeHPSTauIsolation(process,postfix=postfixAK5)

   
# curing a weird bug in PAT..
from CMGTools.Common.PAT.removePhotonMatching import removePhotonMatching
removePhotonMatching( process, postfixAK5 )

getattr(process,"pfNoMuon"+postfixAK5).enable = False 
getattr(process,"pfNoElectron"+postfixAK5).enable = False 
getattr(process,"pfNoTau"+postfixAK5).enable = False 
getattr(process,"pfNoJet"+postfixAK5).enable = True
getattr(process,"pfIsolatedMuons"+postfixAK5).isolationCut = 999999
getattr(process,"pfIsolatedElectrons"+postfixAK5).isolationCut = 999999

# adding vbtf and cic electron IDs
from CMGTools.Common.PAT.addPATElectronID_cff import addPATElectronID
addPATElectronID( process, postfixAK5 , runOnMC )

# insert the PFMET sifnificance calculation
from CMGTools.Common.PAT.addMETSignificance_cff import addMETSig
addMETSig( process, postfixAK5 )

# ---------------- Sequence AK5LC, lepton x-cleaning ---------------

# PF2PAT+PAT sequence 2:
# lepton cleaning, AK5PFJets. This sequence is a clone of the AK5 sequence defined previously.
# just modifying the x-cleaning parameters, and the isolation cut for x-cleaning

if runAK5LC:
  print 'cloning AK5 sequence to prepare AK5LC sequence...'

  from PhysicsTools.PatAlgos.tools.helpers import cloneProcessingSnippet
  postfixLC = 'LC'
  # just cloning the first sequence, and enabling lepton cleaning 
  cloneProcessingSnippet(process, getattr(process, 'patPF2PATSequence'+postfixAK5), postfixLC)

  postfixAK5LC = postfixAK5+postfixLC
  getattr(process,"pfNoMuon"+postfixAK5LC).enable = True
  getattr(process,"pfNoElectron"+postfixAK5LC).enable = True 
  getattr(process,"pfIsolatedMuons"+postfixAK5LC).isolationCut = 0.2
  getattr(process,"pfIsolatedElectrons"+postfixAK5LC).isolationCut = 0.2

  #COLIN : need to add the VBTF e and mu id

  # configure MET significance
  getattr(process,"PFMETSignificance"+postfixAK5LC).inputPATElectrons = cms.InputTag('patElectrons'+postfixAK5LC)   
  getattr(process,"PFMETSignificance"+postfixAK5LC).inputPATMuons = cms.InputTag('patMuons'+postfixAK5LC)


  print 'cloning AK5 sequence to prepare AK5LC sequence...Done'

# ---------------- Sequence AK7, no lepton x-cleaning ---------------

# PF2PAT+PAT sequence 3
# no lepton cleaning, AK7PFJets

if runAK7:
  postfixAK7 = "AK7"
  jetAlgoAK7="AK7"

  #COLIN : argh! AK7PFchs does not seem to exist yet...
  # Maxime should maybe contact the JEC group if he wants them 
  usePF2PAT(process,runPF2PAT=True, jetAlgo=jetAlgoAK7, runOnMC=runOnMC, postfix=postfixAK7,
          jetCorrections=('AK7PF', jetCorrections))

  # if doJetPileUpCorrection:
  #    enablePileUpCorrection( process, postfix=postfixAK7)

  # no need for taus in AK7 sequence. could remove the whole tau sequence to gain time?
  # if hpsTaus:
  #    adaptPFTaus(process,"hpsPFTau",postfix=postfixAK7)

  # no top projection: 
  getattr(process,"pfNoMuon"+postfixAK7).enable = False 
  getattr(process,"pfNoElectron"+postfixAK7).enable = False 
  getattr(process,"pfNoTau"+postfixAK7).enable = False 
  getattr(process,"pfNoJet"+postfixAK7).enable = True

  removePhotonMatching( process, postfixAK7 )

  # addPATElectronID( process, postfixAK7 , runOnMC )

  # addMETSig(process,postfixAK7)

# ---------------- Sequence CA8, no lepton x-cleaning ---------------

# PF2PAT+PAT sequence 4
# no lepton cleaning, CA8PFJets

if runCA8:
  postfixCA8 = "CA8"
  jetAlgoCA8="CA8"

  # gen jet reconstruction modules
  process.load("RecoJets.Configuration.GenJetParticles_cff")
  process.load("RecoJets.JetProducers.ca4GenJets_cfi")
  process.ca08GenJets = process.ca4GenJets.clone( rParam = 0.8)

  # pf jet reconstruction module
  process.load("RecoJets.JetProducers.ca4PFJets_cfi")
  process.ca08PFJets = process.ca4PFJets.clone( rParam = cms.double(0.8),
                                              doAreaFastjet = cms.bool(True),
                                              doRhoFastjet = cms.bool(True),
                                              Rho_EtaMax = cms.double(6.0),
                                              Ghost_EtaMax = cms.double(7.0)
                                              )

  addJetCollection(process,cms.InputTag('ca08PFJets'),
                  'CA8','PF',
                  doJTA = False,
                  doBTagging = False,
                  jetCorrLabel = ('AK5PF', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute'])),
                  doType1MET = False,
                  doL1Cleaning = False,
                  doL1Counters = False,
                  genJetCollection=cms.InputTag("ca08GenJets"),
                  doJetID = False,
                  jetIdLabel = "ca8"
                  )
  process.patJetsCA8PF.addDiscriminators = cms.bool(False)
  process.patJetsCA8PF.embedCaloTowers = cms.bool(False)
  process.patJetsCA8PF.embedGenJetMatch = cms.bool(False)
  process.patJetsCA8PF.embedGenPartonMatch = cms.bool(False)
  process.patJetsCA8PF.addGenPartonMatch = cms.bool(False)
  process.patJetsCA8PF.getJetMCFlavour = cms.bool(False)
  process.patJetsCA8PF.embedPFCandidates = cms.bool(False)
  process.patJetCorrFactorsCA8PF.rho = cms.InputTag("kt6PFJets","rho")

  process.recoMyCAJets = cms.Sequence(process.genJetParticles*process.ca08GenJets*process.ca08PFJets*process.patJetGenJetMatchCA8PF*process.patJetCorrFactorsCA8PF*process.patJetsCA8PF*process.selectedPatJetsCA8PF)

  ######
  # Jet pruning
  #####

  from RecoJets.JetProducers.GenJetParameters_cfi import *
  from RecoJets.JetProducers.PFJetParameters_cfi import *
  from RecoJets.JetProducers.PFJetParameters_cfi import *
  from RecoJets.JetProducers.CaloJetParameters_cfi import *
  from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
  from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters

  #prune CA08 jets
  process.ca08PrunedPFJets = cms.EDProducer(
                              "SubJetProducer",
                              PFJetParameters.clone(
                                  #src = cms.InputTag(''), #default input, as for the fat CA jet
                                  doAreaFastjet = cms.bool(True),
                                  doRhoFastjet = cms.bool(False)
                                  ),
                              AnomalousCellParameters,
                              SubJetParameters,
                              jetAlgorithm = cms.string("CambridgeAachen"),
                              rParam = cms.double(0.8),
                              jetCollInstanceName=cms.string("subjets")
                              )
  process.ca08PrunedPFJets.nSubjets = cms.int32(2)

  process.ca08PrunedGenJets =  cms.EDProducer(
                             "SubJetProducer",
                             GenJetParameters.clone(
                                 #src = cms.InputTag("genParticlesForJetsNoNu"), #default input
                                 doAreaFastjet = cms.bool(False),
                                 doRhoFastjet = cms.bool(False)
                                 ),
                             AnomalousCellParameters,
                             SubJetParameters,
                             jetAlgorithm = cms.string("CambridgeAachen"),
                             rParam = cms.double(0.8),
                             jetCollInstanceName=cms.string("subjets")
                             )

  process.genjetFilter = cms.EDFilter("CandViewCountFilter",
                                  src = cms.InputTag("ca08PrunedGenJets"),
                                  minNumber = cms.uint32(1)
                                  )

  #add pruned CA08 jets
  addJetCollection(process, 
                 cms.InputTag('ca08PrunedPFJets'),         
                 'CA8Pruned', 'PF',
                 doJTA=False,            # Run Jet-Track association & JetCharge
                 doBTagging=False,       # Run b-tagging
                 jetCorrLabel= ('AK5PF', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute'])),
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
          #       genJetCollection = cms.InputTag("ca8GenJetsNoNu"), #why not the corresponding gen level ?
                 genJetCollection = cms.InputTag("ca08PrunedGenJets:subjets"),
                 #    genJetCollection = cms.InputTag("ca08GenJets"),
                 doJetID = False
                 )
  process.patJetsCA8PrunedPF.addDiscriminators = cms.bool(False)
  process.patJetsCA8PrunedPF.embedCaloTowers = cms.bool(False)
  process.patJetsCA8PrunedPF.embedGenJetMatch = cms.bool(False)
  process.patJetsCA8PrunedPF.embedGenPartonMatch = cms.bool(False)
  process.patJetsCA8PrunedPF.addGenPartonMatch = cms.bool(False)
  process.patJetsCA8PrunedPF.getJetMCFlavour = cms.bool(False)
  process.patJetsCA8PrunedPF.embedPFCandidates = cms.bool(False)
  process.patJetCorrFactorsCA8PrunedPF.rho = cms.InputTag("kt6PFJets","rho")

  process.ca08PFconstituents = cms.EDProducer("JetSlimmer",
                                     JetInputCollection=cms.untracked.InputTag("customPFJetsCA08"),
                                     isPFJet=cms.untracked.bool(True),
                                     debug=cms.untracked.bool(False)
                                     )


  process.recoMyPrunedCAJets = cms.Sequence(process.ca08PrunedGenJets*process.ca08PrunedPFJets*process.patJetGenJetMatchCA8PrunedPF*process.patJetCorrFactorsCA8PrunedPF*process.patJetsCA8PrunedPF*process.selectedPatJetsCA8PrunedPF)

  setattr(process,"patPATSequence"+postfixCA8, cms.Sequence( process.recoMyCAJets + process.recoMyPrunedCAJets ))

  ### END JET PRUNING SECTION
  ###############

# ---------------- Common stuff ---------------

process.load('CMGTools.Common.gen_cff')


process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
process.patTrigger.processName = cms.string('*')

### PATH DEFINITION #############################################


# trigger information (no selection)

#process.p = cms.Path( process.patTriggerDefaultSequence )
process.p = cms.Path( )

# gen ---- 

if runOnMC:
    process.p += process.genSequence 

# PF2PAT+PAT ---

process.p += getattr(process,"patPF2PATSequence"+postfixAK5)

if runAK5LC:
    process.p += getattr(process,"patPF2PATSequence"+postfixAK5LC) 

if runAK7:
    process.p += getattr(process,"patPF2PATSequence"+postfixAK7) 

if runCA8:
    process.p += getattr(process,"patPATSequence"+postfixCA8) 

# event cleaning (in tagging mode, no event rejected)

process.load('CMGTools.Common.eventCleaning.eventCleaning_cff')

#process.p += process.eventCleaningSequence

 
# CMG ---

if runCMG:
    
    process.load('CMGTools.Common.analysis_cff')
    # running on PFAOD -> calo objects are not available.
    # we'll need to reactivate caloMET, though
    # process.p += process.analysisSequence

    from CMGTools.Common.Tools.visitorUtils import replacePostfix
    
    if runAK5LC:
        cloneProcessingSnippet(process, getattr(process, 'analysisSequence'), 'AK5LCCMG')
        replacePostfix(getattr(process,"analysisSequenceAK5LCCMG"),'AK5','AK5LC') 
        process.p += process.analysisSequenceAK5LCCMG
        
    if runAK7:
        cloneProcessingSnippet(process, getattr(process, 'analysisSequence'), 'AK7CMG')
        replacePostfix(getattr(process,"analysisSequenceAK7CMG"),'AK5','AK7') 
        process.p += process.analysisSequenceAK7CMG

    if runCA8:
        cloneProcessingSnippet(process, getattr(process, 'jetSequence'), 'CA8CMG')
        replacePostfix(getattr(process,"jetSequenceCA8CMG"),'AK5','CA8PF') 
        process.analysisSequence += process.jetSequenceCA8CMG
        cloneProcessingSnippet(process, getattr(process, 'jetSequence'), 'CA8PrunedCMG')
        replacePostfix(getattr(process,"jetSequenceCA8PrunedCMG"),'AK5','CA8PrunedPF') 
	process.cmgPFJetCA8PrunedCMG.cfg.addConstituents=False
	process.cmgPFJetCA8PrunedCMG.cfg.baseJetFactory.addSubjets=True
	process.cmgPFBaseJetCA8PrunedCMG.cfg.addSubjets=True
        process.analysisSequence += process.jetSequenceCA8PrunedCMG
        #cloneProcessingSnippet(process, getattr(process, 'jetCutSummarySequence'), 'CA8CMG')
        #replacePostfix(getattr(process,"jetCutSummarySequenceCA8CMG"),'AK5','CA8') 
        #process.analysisSequence += process.jetCutSummarySequenceCA8CMG
        #cloneProcessingSnippet(process, getattr(process, 'jetHistogramSequence'), 'CA8CMG')
        #replacePostfix(getattr(process,"jetHistogramSequenceCA8CMG"),'AK5','CA8') 
        #process.analysisSequence += process.jetHistogramSequenceCA8CMG

    from CMGTools.Common.Tools.tuneCMGSequences import * 
    tuneCMGSequences(process, postpostfix='CMG')

    process.p += process.analysisSequence

### OUTPUT DEFINITION #############################################

# PF2PAT+PAT ---

# Add PF2PAT output to the created file
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning, patTriggerEventContent, patTriggerStandAloneEventContent
process.out.outputCommands = cms.untracked.vstring('drop *',
                                                   *patEventContentNoCleaning
                                                   )
# add trigger information to the pat-tuple
process.out.outputCommands += patTriggerEventContent
process.out.outputCommands += patTriggerStandAloneEventContent

# add gen event content to the pat-tuple (e.g. status 3 GenParticles)
from CMGTools.Common.eventContent.gen_cff import gen 
process.out.outputCommands.extend( gen )

# tuning the PAT event content to our needs
from CMGTools.Common.eventContent.patEventContentCMG_cff import patEventContentCMG
process.out.outputCommands.extend( patEventContentCMG )

# event cleaning results
from CMGTools.Common.eventContent.eventCleaning_cff import eventCleaning
process.out.outputCommands.extend( eventCleaning )

from CMGTools.Common.eventContent.runInfoAccounting_cff import runInfoAccounting
process.out.outputCommands.extend( runInfoAccounting )

if runCA8:
  process.out.outputCommands.extend(cms.untracked.vstring('keep *_ca08PrunedPFJets_*_*', 'keep *_ca08PrunedGenJets_*_*'))

# CMG ---

from CMGTools.Common.eventContent.everything_cff import everything 

process.outcmg = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('${dir}_tree_CMG.root'),
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = everything,
    dropMetaData = cms.untracked.string('PRIOR')
    )


if runCMG:
    process.outpath += process.outcmg

process.load("CMGTools.Common.runInfoAccounting_cff")
process.ria = cms.Sequence(
    process.runInfoAccountingDataSequence
    )
if runOnMC:
    process.ria = cms.Sequence(
        process.runInfoAccountingSequence
    )

process.outpath += process.ria
    

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("${dir}_histograms_CMG.root"))

# process.Timing = cms.Service("Timing")

# print process.dumpPython()

EOF

cmsRun ${pycmg}

  m=`expr $m + 1`
done

  n=`expr $n + 1`
done
