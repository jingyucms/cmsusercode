import os

cm="13"
if cm=="13":
  minMasses=[4500]
  signalMasses=[12000,13000,14000,16000,18000,50000]
  #signalMasses=[20000,22000]
else:
  minMasses=[3500]
  signalMasses=[8000,10000,12000,14000,50000]
couplings=[(1,0,0),]
samples=[]

for minMass in minMasses:
    #samples+=[('pythia8_qcd',minMass,"",""),]
    
    for signalMass in signalMasses:
        for coupling in couplings:
             samples+=[('pythia8_ci',minMass,signalMass,coupling),]

    #samples+=[('pythia8_qcdNonPert',minMass,"",""),]

version=cm+"TeV_Nov7"

for sample,minMass,signalMass,coupling in samples:
    samplename=sample+"_m"+str(minMass)+"_"+str(signalMass)+"_"+str(coupling).strip("()").replace(" ","").replace(",","_")+"_"+version
    cfg=open(samplename+".py","w")
    cfg.writelines("""
import FWCore.ParameterSet.Config as cms

process = cms.Process("PFAOD")

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(300000) )

process.load("Configuration.EventContent.EventContent_cff")
process.out = cms.OutputModule(
    "PoolOutputModule",
    process.AODSIMEventContent,
    fileName = cms.untracked.string('/opt2/chi_analysis/"""+samplename+""".root'),
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

process.generator = cms.EDFilter("Pythia8GeneratorFilter",
	comEnergy = cms.double("""+cm+"""000.0),
	crossSection = cms.untracked.double(1e10),
	filterEfficiency = cms.untracked.double(1),
	maxEventsToPrint = cms.untracked.int32(0),
	pythiaHepMCVerbosity = cms.untracked.bool(False),
	pythiaPylistVerbosity = cms.untracked.int32(0),
	#useUserHook = cms.bool(True),
	
	PythiaParameters = cms.PSet(
		processParameters = cms.vstring(
			'Main:timesAllowErrors    = 10000',
			'ParticleDecays:limitTau0 = on',
			'ParticleDecays:tauMax = 10',
			'PhaseSpace:mHatMin = """+str(minMass)+""" ',
			'PhaseSpace:pTHatMin = """+str(minMass/10)+""" ',
			'Tune:pp 5',
			'Tune:ee 3',
""")
    if signalMass=="" and "NonPert" in sample:
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
		parameterSets = cms.vstring('processParameters')
	)
)

#process.pfPileUp.PFCandidates=cms.InputTag("particleFlow")
#process.pfNoPileUp.bottomCollection=cms.InputTag("particleFlow")
#process.pfPileUpCandidates.bottomCollection=cms.InputTag("particleFlow")

process.load("RecoJets.Configuration.GenJetParticles_cff")
process.load("RecoJets.Configuration.RecoGenJets_cff")
process.ak5GenJets.jetPtMin="""+str(minMass/10)+"""

process.p = cms.Path(process.generator*process.genParticles*process.genJetParticles*process.ak5GenJets)#*process.ca08PrunedGenJets
process.endpath = cms.EndPath(process.out)
process.schedule = cms.Schedule(process.p,process.endpath)
process.out.outputCommands=cms.untracked.vstring('keep *','drop edmHepMCProduct_generator_*_*','drop *_genParticles_*_*','drop *_genParticlesForJets_*_*')
""")
    cfg.close()
    #os.system("cmsBatch.py 200 "+samplename+".py -o "+samplename+"_jobs -b 'bsub -G u_zh -q 1nd < ./batchScript.sh' -f -r /store/cmst3/user/hinzmann/fastsim/"+samplename+"/")
    os.system("cmsRun "+samplename+".py > "+samplename+".log &")
