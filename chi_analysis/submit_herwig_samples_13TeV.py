import os

minMasses=[1000,1500,1900,2400,2800,3300,3800,4300] # for mass bins 1.9, 2.4, 3.0, 3.6, 4.2, 4.8, 5.4
maxMasses=[1500,1900,2400,2800,3300,3800,4300,13000] # for mass bins 1.9, 2.4, 3.0, 3.6, 4.2, 4.8, 5.4

samples=[]

for minMass in minMasses:
    #samples+=[('herwigpp_qcd',minMass,maxMasses[minMasses.index(minMass)],"",""),]
    samples+=[('herwigpp_qcdNonPert',minMass,maxMasses[minMasses.index(minMass)],"",""),]

version="Nov28"

numjobs=100

for sample,minMass,maxMass,signalMass,coupling in samples:

  for jobnum in range(numjobs):

    samplename=sample+"_m"+str(minMass)+"_"+str(maxMass)+"_"+str(signalMass)+"_"+str(coupling).strip("()").replace(" ","").replace(",","_")+"_"+version
    cfg=open(samplename+str(jobnum)+".py","w")
    cfg.writelines("""
import FWCore.ParameterSet.Config as cms

process = cms.Process("GEN")

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(300000) )

process.load("Configuration.EventContent.EventContent_cff")
process.out = cms.OutputModule(
    "PoolOutputModule",
    process.AODSIMEventContent,
    fileName = cms.untracked.string('GEN.root'),
    )

process.load("CommonTools.ParticleFlow.PF2PAT_EventContent_cff")
process.out.outputCommands.extend( process.prunedAODForPF2PATEventContent.outputCommands )

# additional stuff for Maxime: 
process.out.outputCommands.extend(
    [
      'keep GenEventInfoProduct_*_*_*',
      'keep *_ak4GenJets_*_*',
      'keep *_ak4CaloJets_*_*',
      'keep *_ak4JetID_*_*',
      'keep *_ak4JetExtender_*_*',
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
process.load('Configuration.StandardSequences.Generator_cff')

process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('PRIVAT'),
    annotation = cms.untracked.string('PRIVAT'),
    name = cms.untracked.string('PRIVAT')
)

# Input source
process.source = cms.Source("EmptySource")
# Other statements
#process.GlobalTag.globaltag = 'START42_V12::All'

process.MessageLogger=cms.Service("MessageLogger",
    destinations = cms.untracked.vstring('logs'),
    logs = cms.untracked.PSet(threshold=cms.untracked.string('WARNING'))
)

from Configuration.Generator.HerwigppDefaults_cfi import *
from Configuration.Generator.HerwigppUE_EE_5C_cfi import *
from Configuration.Generator.HerwigppPDF_CTEQ6_LO_cfi import *									# Import CTEQ6L PDF as shower pdf
from Configuration.Generator.HerwigppEnergy_13TeV_cfi import *
from Configuration.Generator.HerwigppMECorrections_cfi import *

process.generator = cms.EDFilter("ThePEGGeneratorFilter",
	herwigDefaultsBlock,
	herwigppUESettingsBlock,
	herwigppPDFSettingsBlock,
	herwigppEnergySettingsBlock,
	herwigppMECorrectionsSettingsBlock,
	crossSection = cms.untracked.double(-1.),
	filterEfficiency = cms.untracked.double(1.),
	configFiles = cms.vstring(),
	parameterSets = cms.vstring(
		'hwpp_cmsDefaults',
		'hwpp_ue_EE5C',
		'hwpp_cm_13TeV',
		'hwpp_pdf_CTEQ6L1',			# Shower PDF matching with the tune
		'hwpp_MECorr_Off',
	    'QCDParameters',
	),
	QCDParameters = cms.vstring(
	     'cd /Herwig/MatrixElements/',
	     'insert SimpleQCD:MatrixElements[0] MEQCD2to2',
	     'cd /',
	     'set /Herwig/Cuts/JetKtCut:MinKT """+str(minMass/10)+"""*GeV',
	     'set /Herwig/Cuts/QCDCuts:MHatMin """+str(minMass)+"""*GeV',
	     'set /Herwig/Cuts/QCDCuts:MHatMax """+str(maxMass)+"""*GeV',
	     'set /Herwig/UnderlyingEvent/MPIHandler:IdenticalToUE 0',
""")
    if "NonPert" in sample:
        cfg.writelines("""	     'set /Herwig/EventHandlers/LHCHandler:MultipleInteractionHandler NULL',
	     'set /Herwig/EventHandlers/LHCHandler:HadronizationHandler NULL',
""")
    cfg.writelines("""
	),
)

process.load("RecoJets.Configuration.GenJetParticles_cff")
process.load("RecoJets.Configuration.RecoGenJets_cff")
process.ak4GenJets.jetPtMin="""+str(minMass/10)+"""
process.ak5GenJets.jetPtMin="""+str(minMass/10)+"""

process.RandomNumberGeneratorService.generator.initialSeed="""+str(jobnum)+"""

process.p = cms.Path(process.generator*process.genParticles*process.genJetParticles*process.ak4GenJets*process.ak5GenJets)#*process.ca08PrunedGenJets
process.endpath = cms.EndPath(process.out)
process.schedule = cms.Schedule(process.p,process.endpath)
process.out.outputCommands=cms.untracked.vstring('keep *','drop edmHepMCProduct_generator_*_*','drop *_genParticles*_*_*','drop *_genParticlesForJets*_*_*')
""")
    cfg.close()
    os.system("qsub -q all.q -o /shome/hinzmann/CMSSW_7_1_20_patch2/src/cmsusercode/chi_analysis/jobout_"+samplename+".out -e /shome/hinzmann/CMSSW_7_1_20_patch2/src/cmsusercode/chi_analysis/jobout_"+samplename+".err submitJobsOnT3batch.sh GEN.root dijet_angular /shome/hinzmann/CMSSW_7_1_20_patch2 cmsusercode/chi_analysis/"+samplename+str(jobnum)+".py "+str(jobnum)+" jobtmp_"+samplename+" /shome/hinzmann/CMSSW_7_1_20_patch2/src/cmsusercode/chi_analysis/jobout_"+samplename+"")
