import os

minMasses=[2500,3700]
scenarios=[(10000,5000,4,0,0),
	   (12000,6000,4,0,0),
	   (14000,7000,4,0,0),
	   (16000,8000,4,0,0),
	   (18000,9000,4,0,0),
	   (20000,10000,4,0,0),
	   (22000,11000,4,0,0),
	   ]
samples=[]

for minMass in minMasses:
    #samples+=[('pythia8_qcd',minMass,""),]
    for lambdaT,MD,nED,negInt,opMode in scenarios:
             samples+=[('pythia8_add',minMass,lambdaT,MD,nED,negInt,opMode),]

version="May27"

for sample,minMass,lambdaT,MD,nED,negInt,opMode in samples:
    samplename=sample+"_m"+str(minMass)+"_"+str(lambdaT)+"_"+str(MD)+"_"+str(nED)+"_"+str(negInt)+"_"+str(opMode)+"_"+version
    print samplename
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

process.generator = cms.EDFilter("Pythia8GeneratorFilter",
	comEnergy = cms.double(8000.0),
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
    if lambdaT=="":
        cfg.writelines("""			'HardQCD:all = on ',
""")
    else:
        cfg.writelines("""			'HardQCD:all = off ',
	                'ExtraDimensionsLED:dijets = on',
			'ExtraDimensionsLED:CutOffmode = 0',
			'ExtraDimensionsLED:LambdaT = """+str(lambdaT)+"""',
			'ExtraDimensionsLED:MD = """+str(MD)+"""',
			'ExtraDimensionsLED:n = """+str(nED)+"""', # Number of extra dimensions
			'ExtraDimensionsLED:nQuarkNew = 5', # outgoing mass-less quark flavours
			'ExtraDimensionsLED:negInt = """+str(negInt)+"""', # Change sign of interferecen term if ==1
			'ExtraDimensionsLED:opMode = """+str(opMode)+"""', # 0=Franceshini paper 1=Giudice paper
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
process.ak5GenJets.jetPtMin=100

process.p = cms.Path(process.generator*process.genParticles*process.genJetParticles*process.ak5GenJets)#*process.ca08PrunedGenJets
process.endpath = cms.EndPath(process.out)
process.schedule = cms.Schedule(process.p,process.endpath)
process.out.outputCommands=cms.untracked.vstring('keep *','drop edmHepMCProduct_generator_*_*','drop *_genParticles_*_*','drop *_genParticlesForJets_*_*')
""")
    cfg.close()
    os.system("cmsBatch.py 200 "+samplename+".py -o "+samplename+"_jobs -b 'bsub -G u_zh -q 1nd < ./batchScript.sh' -f -r /store/cmst3/user/hinzmann/fastsim/"+samplename+"/")
