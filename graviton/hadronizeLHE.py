import FWCore.ParameterSet.Config as cms

process = cms.Process("PFAOD")

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic7TeV2011Collision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("LHESource",
	fileNames = cms.untracked.vstring('file:graviton4j/graviton/testOutput.lhe')
)
process.GlobalTag.globaltag = 'START42_V12::All'

process.MessageLogger=cms.Service("MessageLogger",
    destinations = cms.untracked.vstring('logs'),
    logs = cms.untracked.PSet(threshold=cms.untracked.string('WARNING'))
)

from Configuration.Generator.PythiaUEZ2Settings_cfi import *

#process.generator = cms.EDFilter("Pythia6HadronizerFilter",
#    pythiaPylistVerbosity = cms.untracked.int32(0),
#    filterEfficiency = cms.untracked.double(1.0),
#    pythiaHepMCVerbosity = cms.untracked.bool(False),
#    comEnergy = cms.double(7000.0),
#    crossSection = cms.untracked.double(0.1538),
#    maxEventsToPrint = cms.untracked.int32(0),
#    PythiaParameters = cms.PSet(
#        pythiaUESettings = cms.vstring('MSTU(21)=1     ! Check on possible errors during program execution', 
#            'MSTJ(22)=2     ! Decay those unstable particles', 
#            'PARJ(71)=10 .  ! for which ctau  10 mm', 
#            'MSTP(33)=0     ! no K factors in hard cross sections', 
#            'MSTP(2)=1      ! which order running alphaS', 
#            'MSTP(51)=10042 ! structure function chosen (external PDF CTEQ6L1)', 
#            'MSTP(52)=2     ! work with LHAPDF', 
#            'PARP(82)=1.832 ! pt cutoff for multiparton interactions', 
#            'PARP(89)=1800. ! sqrts for which PARP82 is set', 
#            'PARP(90)=0.275 ! Multiple interactions: rescaling power', 
#            'MSTP(95)=6     ! CR (color reconnection parameters)', 
#            'PARP(77)=1.016 ! CR', 
#            'PARP(78)=0.538 ! CR', 
#            'PARP(80)=0.1   ! Prob. colored parton from BBR', 
#            'PARP(83)=0.356 ! Multiple interactions: matter distribution parameter', 
#            'PARP(84)=0.651 ! Multiple interactions: matter distribution parameter', 
#            'PARP(62)=1.025 ! ISR cutoff', 
#            'MSTP(91)=1     ! Gaussian primordial kT', 
#            'PARP(93)=10.0  ! primordial kT-max', 
#            'MSTP(81)=21    ! multiple parton interactions 1 is Pythia default', 
#            'MSTP(82)=4     ! Defines the multi-parton model'),
#        processParameters = cms.vstring('MSEL        = 0    !User defined processes', 
#            'PMAS(5,1)=4.4   ! b quark mass', 
#            'PMAS(6,1)=172.5 ! t quark mass'),
#        parameterSets = cms.vstring('pythiaUESettings', 
#            'processParameters')
#    )
#)

process.generator = cms.EDFilter("Pythia6HadronizerFilter",
	pythiaHepMCVerbosity = cms.untracked.bool(True),
	maxEventsToPrint = cms.untracked.int32(0),
	pythiaPylistVerbosity = cms.untracked.int32(1),
	comEnergy = cms.double(7000.0),
	PythiaParameters = cms.PSet(
	        pythiaUESettingsBlock,
		processParameters = cms.vstring(
		        'MSEL = 0',
		        'MSTJ(1) = 1',
		        'MSTP(61) = 1',
                        'PMAS(5,1)=4.4   ! b quark mass',
                        'PMAS(6,1)=172.5 ! t quark mass',
		),
		parameterSets = cms.vstring(
		        'pythiaUESettings',
		        'processParameters')
	),
)

#from Configuration.Generator.HerwigppDefaults_cfi import *
#process.generator = cms.EDFilter("ThePEGGeneratorFilter",
#	herwigDefaultsBlock,
#	filterEfficiency = cms.untracked.double(1),
#	crossSection = cms.untracked.double(1e10),
#	configFiles = cms.vstring('RS.model'),
#	parameterSets = cms.vstring(
#		'cm7TeV',
#		'pdfCTEQ6L1',
#		'productionParameters',
#		'basicSetup',
#		'setParticlesStableForDetector',
#		'lheDefaults',
#		'lheDefaultPDFs',
#	),
#)

process.load("Configuration.EventContent.EventContent_cff")
process.out = cms.OutputModule(
    "PoolOutputModule",
    process.AODSIMEventContent,
    fileName = cms.untracked.string('LHE.root'),
    )

process.load("CMGTools.Common.gen_cff")
process.out.outputCommands+=cms.untracked.vstring('keep *_genParticlesStatus3_*_*')

process.p = cms.Path(process.generator*process.pgen*process.genSequence)#process.generator*process.pgen*process.simulationWithFamos*process.reconstructionWithFamos)
process.endpath = cms.EndPath(process.out)
