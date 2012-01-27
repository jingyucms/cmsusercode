import os
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

#suffix="tree"
suffix="histograms"

#options.outputFile='/tmp/hinzmann/QCD_tree.root'
options.outputFile='/tmp/hinzmann/428_HT_Run2011A-May10ReReco-v1_vv4_'+suffix+'.root'
#options.outputFile='/tmp/hinzmann/428_HT_Run2011A-PromptReco-v4_vv4_'+suffix+'.root'
#options.outputFile='/tmp/hinzmann/428_HT_Run2011A-05Aug2011-v1_vv4_'+suffix+'.root'
#options.outputFile='/tmp/hinzmann/428_HT_Run2011A-PromptReco-v6_vv4_'+suffix+'.root'
#options.outputFile='/tmp/hinzmann/428_HT_Run2011B-PromptReco-v1_vv4_'+suffix+'.root'

#files=''+suffix+'.*root'
files='CMG_'+suffix+'.*root'

#options.maxEvents=100000

process = cms.Process("PickEvent")
from CMGTools.Production.datasetToSource import *
if 'QCD' in options.outputFile:
  process.source = datasetToSource('hinzmann',
    '/QCD_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM/PAT_CMG_Hinzmann',
    files)
elif 'WW' in options.outputFile:
  process.source = datasetToSource('hinzmann',
    '/WW_TuneZ2_7TeV_pythia6_tauola/Summer11-PU_S4_START42_V11-v1/AODSIM/V2/PAT_CMG_Hinzmann6',
    files)
elif 'W' in options.outputFile:
  process.source = datasetToSource('hinzmann',
    '/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM/V2/PAT_CMG_Hinzmann6',
    files)
elif 'W1Jet' in options.outputFile:
  process.source = datasetToSource('hinzmann',
    '/W1Jet_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM/V2',
    files)
elif '428_HT_Run2011A-May10ReReco-v1_vv4' in options.outputFile:
  process.source = datasetToSource('hinzmann',
    '/428_HT_Run2011A-May10ReReco-v1_vv4',
    files)
elif '428_HT_Run2011A-PromptReco-v4_vv4' in options.outputFile:
  process.source = datasetToSource('hinzmann',
    '/428_HT_Run2011A-PromptReco-v4_vv4',
    files)
elif '428_HT_Run2011A-05Aug2011-v1_vv4' in options.outputFile:
  process.source = datasetToSource('hinzmann',
    '/428_HT_Run2011A-05Aug2011-v1_vv4',
    files)
elif '428_HT_Run2011A-PromptReco-v6_vv4' in options.outputFile:
  process.source = datasetToSource('hinzmann',
    '/428_HT_Run2011A-PromptReco-v6_vv4',
    files)
elif '428_HT_Run2011B-PromptReco-v1_vv4' in options.outputFile:
  process.source = datasetToSource('hinzmann',
    '/428_HT_Run2011B-PromptReco-v1_vv4',
    files)
    
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

if suffix=="histograms":
    filenames=process.source.fileNames
    size=50
    number=0
    while len(filenames)>0:
        command="hadd "+options.outputFile.replace('.root','')+"_"+str(number)+'.root -f' #-f6
	command+=" file:/tmp/hinzmann/CMG_histograms.root"
        for filename in filenames[:size]:
            command+=" root://eoscms//eos/cms"+filename
        print command
        os.system(command)
        number+=1
        filenames=filenames[size:]
	