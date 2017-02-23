import os

signalMasses=[1000,1500,1750,2000,2250,2500,3000,3500,4000,4500,5000,6000]
signalMasses=[3000]
minMass=1900
couplings=[("1p5","1p0")]
mDMs=[1]
samples=[]

for signalMass in signalMasses:
  for mDM in mDMs:
    for coupling in couplings:
        #samples+=[('Axial_Dijet_LO_Mphi',signalMass,mDM,coupling),]
        samples+=[('Vector_Dijet_LO_Mphi',signalMass,mDM,coupling),]

print samples

version="Feb23"

for sample,signalMass,mDM,coupling in samples:
  
  numjobs=1

  for jobnum in range(numjobs):

    samplename=sample+"_"+str(signalMass)+"_"+coupling[0]+"_"+coupling[1]+"_"+version
    filen=sample+"-"+str(signalMass)+"_Mchi-"+str(mDM)+"_gSM-"+coupling[0]+"_gDM-"+coupling[1]+"_13TeV-madgraph_tarball.tar.xz"
    cfg=open(samplename+str(jobnum)+".py","w")
    cfg.writelines("""
import os
os.system("eos cp /eos/cms/store/user/pharris/gridpack/"""+filen+""" /tmp/hinzmann/")
    
import FWCore.ParameterSet.Config as cms

process = cms.Process("GEN")

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

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

process.externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    nEvents = cms.untracked.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    numberOfParameters = cms.uint32(1),
    args = cms.vstring("/tmp/hinzmann/"""+filen+"""")
)

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

process.generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    )
    )
)

process.load("RecoJets.Configuration.GenJetParticles_cff")
process.load("RecoJets.Configuration.RecoGenJets_cff")
process.ak4GenJets.jetPtMin="""+str(minMass/10)+"""
process.ak5GenJets.jetPtMin="""+str(minMass/10)+"""

process.RandomNumberGeneratorService.generator.initialSeed="""+str(jobnum)+"""

process.p = cms.Path(process.externalLHEProducer*process.generator*process.genParticles*process.genJetParticles*process.ak4GenJets*process.ak5GenJets)#*process.ca08PrunedGenJets
process.endpath = cms.EndPath(process.out)
process.schedule = cms.Schedule(process.p,process.endpath)
process.out.outputCommands=cms.untracked.vstring('keep *','drop edmHepMCProduct_generator_*_*','drop *_genParticles*_*_*','drop *_genParticlesForJets*_*_*')
""")
    cfg.close()
    os.system("qsub -q all.q -o /shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/jobout_"+samplename+".out -e /shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/jobout_"+samplename+".err submitJobsOnT3batch.sh GEN.root dijet_angular /shome/hinzmann/CMSSW_7_4_7_patch2 cmsusercode/chi_analysis/"+samplename+str(jobnum)+".py "+str(jobnum)+" jobtmp_"+samplename+" /shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/jobout_"+samplename+"")
