import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing ('analysis')

# add a list of strings for events to process
options.register ('eventsToProcess',
				  '',
				  VarParsing.multiplicity.list,
				  VarParsing.varType.string,
				  "Events to process")
options.register ('maxSize',
				  0,
				  VarParsing.multiplicity.singleton,
				  VarParsing.varType.int,
				  "Maximum (suggested) file size (in Kb)")
options.parseArguments()

options.outputFile='cmgtrees/W1Jet_tree.root'

process = cms.Process("PickEvent")
from CMGTools.Production.datasetToSource import *
if 'QCD' in options.outputFile:
  process.source = datasetToSource('hinzmann',
    '/QCD_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM/PAT_CMG_Hinzmann',
    'tree.*root')
elif 'WW' in options.outputFile:
  process.source = datasetToSource('hinzmann',
    '/WW_TuneZ2_7TeV_pythia6_tauola/Summer11-PU_S4_START42_V11-v1/AODSIM/V2/PAT_CMG_Hinzmann6',
    'tree.*root')
elif 'W' in options.outputFile:
  process.source = datasetToSource('hinzmann',
    '/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM/V2/PAT_CMG_Hinzmann6',
    'tree.*root')
elif 'W1Jet' in options.outputFile:
  process.source = datasetToSource('hinzmann',
    '/W1Jet_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM/V2',
    'tree.*root')

if options.eventsToProcess:
    process.source.eventsToProcess = \
           cms.untracked.VEventRange (options.eventsToProcess)


process.maxEvents = cms.untracked.PSet(
	    input = cms.untracked.int32 (options.maxEvents)
)


process.Out = cms.OutputModule("PoolOutputModule",
        fileName = cms.untracked.string (options.outputFile)
)

if options.maxSize:
    process.Out.maxSize = cms.untracked.int32 (options.maxSize)

process.end = cms.EndPath(process.Out)
