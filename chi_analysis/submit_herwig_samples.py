import os

minMasses=[2500,3700]
signalMasses=[6000,8000,9000,10000,12000,14000,15000,16000,18000,20000]
couplings=[(1,0,0),]
samples=[]

for minMass in minMasses:
    samples+=[('herwigpp_qcd',minMass,"",""),]
    samples+=[('herwigpp_qcdNonPert',minMass,"",""),]

version="Aug24"

for sample,minMass,signalMass,coupling in samples:
    samplename=sample+"_m"+str(minMass)+"_"+str(signalMass)+"_"+str(coupling).strip("()").replace(" ","").replace(",","_")+"_"+version
    cfg=open(samplename+".py","w")
    cfg.writelines("""
import FWCore.ParameterSet.Config as cms

process = cms.Process("PFAOD")

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100000) )

process.load("Configuration.EventContent.EventContent_cff")
process.out = cms.OutputModule(
    "PoolOutputModule",
    process.AODSIMEventContent,
    fileName = cms.untracked.string('PFAOD.root'),
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

from Configuration.Generator.HerwigppDefaults_cfi import *
from Configuration.Generator.HerwigppUE_EE_3C_cfi import *

process.generator = cms.EDFilter("ThePEGGeneratorFilter",
	herwigDefaultsBlock,
	herwigppUESettingsBlock,
	crossSection = cms.untracked.double(1.),
	filterEfficiency = cms.untracked.double(1.),
	configFiles = cms.vstring(),
	parameterSets = cms.vstring(
	    'herwigppUE_EE_3C_8000GeV',
	    'QCDParameters',
	    'basicSetup',
	    'setParticlesStableForDetector',
	),
	QCDParameters = cms.vstring(
	     'cd /Herwig/MatrixElements/',
	     'insert SimpleQCD:MatrixElements[0] MEQCD2to2',
	     'cd /',
	     'set /Herwig/Cuts/JetKtCut:MinKT """+str(minMass/10)+"""*GeV',
	     'set /Herwig/Cuts/QCDCuts:MHatMin """+str(minMass)+"""*GeV',
	     'set /Herwig/UnderlyingEvent/MPIHandler:IdenticalToUE 0',
""")
    if "NonPert" in sample:
        cfg.writelines("""	     'set /Herwig/EventHandlers/LHCHandler:MultipleInteractionHandler NULL',
	     'set /Herwig/EventHandlers/LHCHandler:HadronizationHandler NULL',
""")
    cfg.writelines("""
	),
)

#process.pfPileUp.PFCandidates=cms.InputTag("particleFlow")
#process.pfNoPileUp.bottomCollection=cms.InputTag("particleFlow")
#process.pfPileUpCandidates.bottomCollection=cms.InputTag("particleFlow")

process.load("RecoJets.Configuration.GenJetParticles_cff")
process.load("RecoJets.Configuration.RecoGenJets_cff")
process.ak5GenJets.jetPtMin=200

process.p = cms.Path(process.generator*process.genParticles*process.genJetParticles*process.ak5GenJets)#*process.ca08PrunedGenJets
process.endpath = cms.EndPath(process.out)
process.schedule = cms.Schedule(process.p,process.endpath)
process.out.outputCommands=cms.untracked.vstring('keep *','drop edmHepMCProduct_generator_*_*','drop *_genParticles_*_*','drop *_genParticlesForJets_*_*')
""")
    cfg.close()
    os.system("cmsBatch.py 200 "+samplename+".py -o "+samplename+"_jobs -b 'bsub -G u_zh -q 1nd < ./batchScript.sh' -f -r /store/cmst3/user/hinzmann/fastsim/"+samplename+"/")
