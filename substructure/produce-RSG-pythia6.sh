#!/bin/sh

startn=0
endn=10
n=${startn}
while [ $n -le $endn ]
do

  dir=pythia6_RSGWW1000_12PU_$n

  echo ********file ${dir}
  
  py=${dir}.py

  echo ********Creating ${py}

cat > ${py} <<EOF

import FWCore.ParameterSet.Config as cms

process = cms.Process("PFAOD")

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(200) )

process.load("Configuration.EventContent.EventContent_cff")
process.out = cms.OutputModule(
    "PoolOutputModule",
    process.AODSIMEventContent,
    fileName = cms.untracked.string('/tmp/hinzmann/${dir}_PFAOD.root'),
    )

process.load("CommonTools.ParticleFlow.PF2PAT_EventContent_cff")
process.out.outputCommands=["keep *"]

# additional stuff for Maxime: 
process.out.outputCommands.extend(
    [
      'keep GenEventInfoProduct_*_*_*',
      'keep *_ak5GenJets_*_*',
      'keep *_ak5CaloJets_*_*',
      'keep *_ak5JetID_*_*',
      'keep *_ak5JetExtender_*_*',
      'keep *_ca8GenJetsNoNu_*_*',
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
      'keep *_pfMet_*_*',
    ])

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load("FWCore.MessageService.MessageLogger_cfi")
#process.load('FastSimulation.Configuration.EventContent_cff')
#process.load('FastSimulation.PileUpProducer.PileUpSimulator_NoPileUp_cff')
#process.load('FastSimulation.Configuration.Geometries_START_cff')
#process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
#process.load('GeneratorInterface.Core.genFilterSummary_cff')
#process.load('FastSimulation.Configuration.FamosSequences_cff')
#process.load('IOMC.EventVertexGenerators.VtxSmearedParameters_cfi')
#process.load('FastSimulation.Configuration.HLT_GRun_cff')
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('PRIVAT'),
    annotation = cms.untracked.string('PRIVAT'),
    name = cms.untracked.string('PRIVAT')
)

#process.famosSimHits.SimulateCalorimetry = True
#process.famosSimHits.SimulateTracking = True
#process.Realistic7TeV2011CollisionVtxSmearingParameters.type = cms.string("BetaFunc")
#process.famosSimHits.VertexGenerator = process.Realistic7TeV2011CollisionVtxSmearingParameters
#process.famosPileUp.VertexGenerator = process.Realistic7TeV2011CollisionVtxSmearingParameters

# Input source
process.source = cms.Source("EmptySource")
# Other statements
#process.GlobalTag.globaltag = 'START42_V12::All'

process.MessageLogger=cms.Service("MessageLogger",
    destinations = cms.untracked.vstring('logs'),
    logs = cms.untracked.PSet(threshold=cms.untracked.string('WARNING'))
)

from Configuration.Generator.PythiaUEZ2starSettings_cfi import *

process.generator = cms.EDFilter("Pythia6GeneratorFilter",
	pythiaHepMCVerbosity = cms.untracked.bool(False),
	maxEventsToPrint = cms.untracked.int32(0),
	pythiaPylistVerbosity = cms.untracked.int32(0),
	filterEfficiency = cms.untracked.double(1),
	comEnergy = cms.double(8000.0),
	crossSection = cms.untracked.double(4.254e-1),
	
	PythiaParameters = cms.PSet(
	        pythiaUESettingsBlock,
                processParameters = cms.vstring(
		        'MSEL = 0',
		        'MSUB(391) = 1',
		        'MSUB(392) = 1',
		        'PMAS(347,1) = 1000',
		        'PARP(50) = 0.54', #0.54
		        '5000039:ALLOFF',
		        '5000039:ONIFANY 24',
		        'MSTP(131) = 1', #pileup on
		        'MSTP(132) = 4', #all pileup processes
		        'MSTP(134) = 12', #number of pileup interactions
		        'MSTP(151) = 1', #different vertices for pileup
		        'PARP(153) = 100', #beamspot z length in mm
        ),
		parameterSets = cms.vstring(
		        'pythiaUESettings',
			'processParameters')
	)
)

#process.pfPileUp.PFCandidates=cms.InputTag("particleFlow")
#process.pfNoPileUp.bottomCollection=cms.InputTag("particleFlow")
#process.pfPileUpCandidates.bottomCollection=cms.InputTag("particleFlow")

process.load("CMGTools.Common.gen_cff")

process.load("RecoJets.Configuration.GenJetParticles_cff")
process.load("RecoJets.Configuration.RecoGenJets_cff")
process.ca8GenJetsNoNu = process.ak7GenJetsNoNu.clone()
process.ca8GenJetsNoNu.rParam = 0.8
process.ca8GenJetsNoNu.jetAlgorithm = "CambridgeAachen"
process.ca8GenJetsNoNu.jetPtMin = 30
process.ca8GenJetsNoNu.doAreaFastjet = True

from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cfi import *
process.patGenJetsCA8CHS = patJets.clone()
process.patGenJetsCA8CHS.jetSource = 'ca8GenJetsNoNu'
process.patGenJetsCA8CHS.addGenJetMatch = False
process.patGenJetsCA8CHS.addGenPartonMatch = False
process.patGenJetsCA8CHS.addJetCharge = False
process.patGenJetsCA8CHS.embedCaloTowers = False
process.patGenJetsCA8CHS.embedPFCandidates = False
process.patGenJetsCA8CHS.addAssociatedTracks = False
process.patGenJetsCA8CHS.addBTagInfo = False
process.patGenJetsCA8CHS.addDiscriminators = False
process.patGenJetsCA8CHS.getJetMCFlavour = False
process.patGenJetsCA8CHS.addJetCorrFactors = False

process.load("Ntuples.TNMc1.ntuple_cfi")
process.load("CMGTools.Susy.RazorMultiJet.razorMultijet_cff")
process.load("CMGTools.Susy.common.susy_cff")

process.razorMJObjectSequence.remove(process.razorMJHemiSequence)
process.susyGenSequence.remove(process.dumpPdfWeights)
process.razorMJHadTriggerInfo.printSelections=False
process.demo.buffers=['patJetHelperGenCA8CHS']
process.demo.ntupleName='${dir}_ntuple.root'

process.p = cms.Path(process.generator*process.genParticles*process.genParticlesForJetsNoNu*process.ca8GenJetsNoNu*process.patGenJetsCA8CHS*process.demo)
#process.endpath = cms.EndPath(process.out)
#process.schedule = cms.Schedule(process.p,process.endpath)

process.RandomNumberGeneratorService.generator.initialSeed=$n

EOF

  cmsRun ${dir}.py
  #cmsStage /tmp/hinzmann/${dir}_PFAOD.root /store/cmst3/user/hinzmann/fastsim
  #cmsBatch.py 300 ${dir}.py -b 'bsub -q 1nd < ./batchScript.sh' -f -r /store/cmst3/user/hinzmann/fastsim/${dir}/

  n=`expr $n + 1`
done
