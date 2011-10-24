#!/bin/sh

startn=0
endn=0
n=${startn}
while [ $n -le $endn ]
do

if [ $n -eq 0 ]
then
scale=1000
fi

if [ $n -eq 1 ]
then
scale=2000
fi

if [ $n -eq 2 ]
then
scale=3000
fi

if [ $n -eq 3 ]
then
scale=500
fi

startm=0
endm=1
m=${startm}
while [ $m -le $endm ]
do

if [ $m -eq 0 ]
then
particle=W
pdgid=24
fi

if [ $m -eq 1 ]
then
particle=Z
pdgid=23
fi

  dir=pythia6_graviton${particle}${particle}_${scale}

  echo ********file ${dir}
  
  py=${dir}.py

  echo ********Creating ${py}

cat > ${py} <<EOF

import FWCore.ParameterSet.Config as cms

process = cms.Process("PFAOD")

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

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
		        'PMAS(347,1)=${scale}',
		        'PARP(50)=0.54',
		        'MSEL=0',
		        'MSUB(391)=1',
		        'MSUB(392)=1',
		        '5000039:ALLOFF',
		        '5000039:ONIFANY 24',
		),
		parameterSets = cms.vstring(
		        'pythiaUESettings',
			'processParameters')
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
cmsRun ${py}
cmsStage -f /tmp/hinzmann/${dir}_PFAOD.root /store/cmst3/user/hinzmann/graviton/

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
runCA8 = False

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
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True))

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
process.out.fileName = cms.untracked.string('${dir}_patTuple_PF2PAT.root')

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

  #COLIN : argh! CA8PFchs does not seem to exist yet...
  # Maxime should maybe contact the JEC group if he wants them 
  usePF2PAT(process,runPF2PAT=True, jetAlgo=jetAlgoCA8, runOnMC=runOnMC, postfix=postfixCA8,
          jetCorrections=('CA8PF', jetCorrections))

  process.load('genJetTopTagCA8_cff')
  process.p += process.genTopTagCA8Sequence

  # if doJetPileUpCorrection:
  #    enablePileUpCorrection( process, postfix=postfixCA8)

  # no need for taus in CA8 sequence. could remove the whole tau sequence to gain time?
  # if hpsTaus:
  #    adaptPFTaus(process,"hpsPFTau",postfix=postfixCA8)

  # no top projection: 
  getattr(process,"pfNoMuon"+postfixCA8).enable = False 
  getattr(process,"pfNoElectron"+postfixCA8).enable = False 
  getattr(process,"pfNoTau"+postfixCA8).enable = False 
  getattr(process,"pfNoJet"+postfixCA8).enable = True

  removePhotonMatching( process, postfixCA8 )

  # addPATElectronID( process, postfixCA8 , runOnMC )

  # addMETSig(process,postfixCA8)


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
    
    cloneProcessingSnippet(process, getattr(process, 'analysisSequence'), 'AK5LCCMG')
    replacePostfix(getattr(process,"analysisSequenceAK5LCCMG"),'AK5','AK5LC') 
    
    cloneProcessingSnippet(process, getattr(process, 'analysisSequence'), 'AK7CMG')
    replacePostfix(getattr(process,"analysisSequenceAK7CMG"),'AK5','AK7') 
    
    from CMGTools.Common.Tools.tuneCMGSequences import * 
    tuneCMGSequences(process, postpostfix='CMG')

    process.p += process.analysisSequence

    if runAK5LC:
        process.p += process.analysisSequenceAK5LCCMG
        
    if runAK7:
        process.p += process.analysisSequenceAK7CMG

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
