import os

cm="13"
minMasses=[1500,1900,2400,2800,3300,3800,4300] # for mass bins 1.9, 2.4, 3.0, 3.6, 4.2, 4.8, 5.4
maxMasses=[1900,2400,2800,3300,3800,4300,13000] # for mass bins 1.9, 2.4, 3.0, 3.6, 4.2, 4.8, 5.4
#signalMasses=[50000,8000,9000,10000,11000,12000,13000,14000,16000,18000]
signalMasses=[8000,9000,10000,11000,12000,13000,14000,16000,18000]
#signalMasses=[50000]
couplings=[(1,0,0)
,(-1,0,0)
]
samples=[]

for minMass in minMasses:
    for signalMass in signalMasses:
        for coupling in couplings:
            samples+=[('pythia8_ci',minMass,maxMasses[minMasses.index(minMass)],signalMass,coupling),]

if 50000 in signalMasses:
  samples+=[('pythia8_ci',1000,1500,50000,(1,0,0)),]

samples=[('pythia8_ciNonPert',1000,1500,50000,(1,0,0)),]
for minMass in minMasses:
  samples+=[('pythia8_ciNonPert',minMass,maxMasses[minMasses.index(minMass)],50000,(1,0,0)),]

print samples

version=cm+"TeV_Nov14"

for sample,minMass,maxMass,signalMass,coupling in samples:
  
  if signalMass==50000:
       numjobs=100
  else:
       numjobs=30

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

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

process.generator = cms.EDFilter("Pythia8GeneratorFilter",
	comEnergy = cms.double("""+cm+"""000.0),
	crossSection = cms.untracked.double(1e10),
	filterEfficiency = cms.untracked.double(1),
	maxEventsToPrint = cms.untracked.int32(0),
	pythiaHepMCVerbosity = cms.untracked.bool(False),
	pythiaPylistVerbosity = cms.untracked.int32(0),
	#useUserHook = cms.bool(True),
	
	PythiaParameters = cms.PSet(
                pythia8CommonSettingsBlock,
                pythia8CUEP8M1SettingsBlock,
		processParameters = cms.vstring(
			'Main:timesAllowErrors    = 10000',
			'PhaseSpace:mHatMin = """+str(minMass)+""" ',
			'PhaseSpace:mHatMax = """+str(maxMass)+""" ',
			'PhaseSpace:pTHatMin = """+str(minMass/10)+""" ',
""")
    if "NonPert" in sample:
        cfg.writelines("""			'HardQCD:all = on ',
			'PartonLevel:MPI = off',
			'HadronLevel:Hadronize = off',
""")
    elif signalMass=="":
        cfg.writelines("""			'HardQCD:all = on ',
""")
    else:
        cfg.writelines("""			'HardQCD:gg2gg = on',
			'HardQCD:gg2qqbar = on',
			'HardQCD:qg2qg = on',
			'HardQCD:qqbar2gg = on',
			'HardQCD:gg2ccbar = on',
			'HardQCD:qqbar2ccbar = on',
			'HardQCD:gg2bbbar = on',
			'HardQCD:qqbar2bbbar = on',
			'HardQCD:qq2qq = off',
			'HardQCD:qqbar2qqbarNew = off',
			'ContactInteractions:QCqq2qq = on',
			'ContactInteractions:QCqqbar2qqbar = on',
			'ContactInteractions:nQuarkNew = 5', # outgoing mass-less quark flavours
			'ContactInteractions:Lambda = """+str(signalMass)+"""',
			'ContactInteractions:etaLL = """+str(coupling[0])+"""', #helicity
			'ContactInteractions:etaRR = """+str(coupling[1])+"""', #helicity
			'ContactInteractions:etaLR = """+str(coupling[2])+"""', #helicity
""")
    cfg.writelines("""
		),
		parameterSets = cms.vstring('pythia8CommonSettings',
                                            'pythia8CUEP8M1Settings',
                                            'processParameters')
	)
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
    os.system("qsub -q all.q -o /shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/jobout_"+samplename+".out -e /shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/jobout_"+samplename+".err submitJobsOnT3batch.sh GEN.root dijet_angular /shome/hinzmann/CMSSW_7_4_7_patch2 cmsusercode/chi_analysis/"+samplename+str(jobnum)+".py "+str(jobnum)+" jobtmp_"+samplename+" /shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/jobout_"+samplename+"")
