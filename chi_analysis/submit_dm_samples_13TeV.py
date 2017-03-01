import os

signalMasses=[1000,1500,1750,2000,2250,2500,3000,3500,4000,4500,5000,6000,7000,8000]
minMass=1900
couplings=[("1p5","1p0")]
samples=[]

for signalMass in signalMasses:
  if signalMass==7000:
   mDMs=[1,4000]
  elif signalMass==8000:
   mDMs=[1,3990]
  else:
   mDMs=[1,3000]
  for mDM in mDMs:
    for coupling in couplings:
        samples+=[('Axial_Dijet_LO_Mphi',signalMass,mDM,coupling),]
        samples+=[('Vector_Dijet_LO_Mphi',signalMass,mDM,coupling),]

print samples

version="Feb25"

for sample,signalMass,mDM,coupling in samples:
  
  numjobs=1

  for jobnum in range(numjobs):

    samplename=sample+"_"+str(signalMass)+"_"+str(mDM)+"_"+coupling[0]+"_"+coupling[1]+"_"+version
    filen=sample+"-"+str(signalMass)+"_Mchi-"+str(mDM)+"_gSM-"+coupling[0]+"_gDM-"+coupling[1]+"_13TeV-madgraph_tarball.tar.xz"
    cfg=open(samplename+str(jobnum)+".py","w")
    cfg.writelines("""
import os
#os.system("eos cp /eos/cms/store/user/pharris/gridpack/"""+filen+""" /tmp/hinzmann/")
os.system("gfal-copy root://t3dcachedb03.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/hinzmann/"""+filen+""" file:////scratch/hinzmann")
    
import FWCore.ParameterSet.Config as cms

process = cms.Process("GEN")

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

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
      #------- Trigger collections ------
      'keep edmTriggerResults_TriggerResults_*_*',
      'keep *_hltTriggerSummaryAOD_*_*',
      'keep L1GlobalTriggerObjectMapRecord_*_*_*',
      'keep L1GlobalTriggerReadoutRecord_*_*_*',
      #------- Various collections ------
      'keep *_EventAuxilary_*_*',
      'keep *_offlinePrimaryVertices_*_*',
      'keep *_offlinePrimaryVerticesWithBS_*_*',
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
    nEvents = cms.untracked.uint32(1000),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    numberOfParameters = cms.uint32(1),
    args = cms.vstring('/scratch/hinzmann/"""+filen+"""')
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

process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="""+str(jobnum)+"""
process.RandomNumberGeneratorService.generator.initialSeed="""+str(jobnum)+"""

process.p = cms.Path(process.externalLHEProducer*process.generator*process.genParticles*process.genJetParticles*process.ak4GenJets)#*process.ca08PrunedGenJets
process.endpath = cms.EndPath(process.out)
process.schedule = cms.Schedule(process.p,process.endpath)
process.out.outputCommands=cms.untracked.vstring('keep *','drop edmHepMCProduct_generator_*_*','drop *_genParticles*_*_*','drop *_genParticlesForJets*_*_*')
""")
    cfg.close()
    #os.system("qsub -q all.q -o /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_1_25_patch3/src/cmsusercode/chi_analysis/jobout_"+samplename+".out -e /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_1_25_patch3/src/cmsusercode/chi_analysis/jobout_"+samplename+".err submitJobsOnT3batch.sh GEN.root dijet_angular /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_1_25_patch3 cmsusercode/chi_analysis/"+samplename+str(jobnum)+".py "+str(jobnum)+" jobtmp_"+samplename+" /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_1_25_patch3/src/cmsusercode/chi_analysis/jobout_"+samplename+"")
    os.system("cmsRun "+samplename+str(jobnum)+".py")
    os.system("gfal-copy -f file:////mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_1_25_patch3/src/cmsusercode/chi_analysis/GEN.root root://t3dcachedb03.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/hinzmann/dijet_angular/"+samplename+str(jobnum)+".root")
