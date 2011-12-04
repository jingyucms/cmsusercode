import FWCore.ParameterSet.Config as cms

#sample='QCD'
#sample='WW'
#sample='graviton-ZZ-1000'
#sample='graviton-WW-1000'
#sample='graviton-ZZ-2000'
sample='graviton-WW-2000'
#sample='Wfast'
#sample='QCDfast'
#sample='May22-v1'
#sample='Prompt-v4'
#sample='Aug05-v1'
#sample='Prompt-v6'
#sample='Prompt-v1'

process = cms.Process("Dijet")

from CMGTools.Production.datasetToSource import *
if sample=='QCD':
  process.source = datasetToSource('hinzmann',
    '/QCD_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM/PAT_CMG_Hinzmann',
    'tree.*root')
elif sample=='WW':
  process.source = datasetToSource('hinzmann',
    '/WW_TuneZ2_7TeV_pythia6_tauola/Summer11-PU_S4_START42_V11-v1/AODSIM/V2/PAT_CMG_Hinzmann6',
    'tree.*root')
elif sample=='W':
  process.source = datasetToSource('hinzmann',
    '/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM/V2/PAT_CMG_Hinzmann6',
    'tree.*root')
elif sample=='graviton-ZZ-1000':
  process.source = cms.Source ("PoolSource",fileNames = cms.untracked.vstring(['file:cmgtrees/herwigpp_graviton_ZZ_1000_tree_CMG.root']))
elif sample=='graviton-WW-1000':
  process.source = cms.Source ("PoolSource",fileNames = cms.untracked.vstring(['file:cmgtrees/herwigpp_graviton_WW_1000_tree_CMG.root']))
elif sample=='graviton-ZZ-2000':
  process.source = cms.Source ("PoolSource",fileNames = cms.untracked.vstring(['file:cmgtrees/herwigpp_graviton_ZZ_2000_tree_CMG.root']))
elif sample=='graviton-WW-2000':
  process.source = cms.Source ("PoolSource",fileNames = cms.untracked.vstring(['file:cmgtrees/herwigpp_graviton_WW_2000_tree_CMG.root']))
elif sample=='Wfast':
  process.source = cms.Source ("PoolSource",fileNames = cms.untracked.vstring(['file:cmgtrees/pythia6_W_tree_CMG.root']))
elif sample=='QCDfast':
  process.source = cms.Source ("PoolSource",fileNames = cms.untracked.vstring(['file:cmgtrees/pythia6_QCD_tree_CMG.root']))
elif sample=="May10-v1":
  process.source = datasetToSource('lucieg',
    '/HT/Run2011A-May10ReReco/AOD/V2',
    'tree.*root')
  json='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions11/7TeV/Prompt/Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt'
  applyJSON(process.json)
elif sample=="Prompt-v4":
  process.source = datasetToSource('cmgtools_group',
    '/HT/Run2011A-PromptReco-v4/AOD/V2',
    'tree.*root')
  json='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions11/7TeV/Prompt/Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt'
  applyJSON(process.json)
elif sample=="Aug05-v1":
  process.source = datasetToSource('cmgtools_group',
    '/HT/Run2011A-05Aug2011-v1/AOD/V2',
    'tree.*root')
  json='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions11/7TeV/Prompt/Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt'
  applyJSON(process.json)
elif sample=="Prompt-v6":
  process.source = datasetToSource('cmgtools_group',
    '/HT/Run2011A-PromptReco-v6/AOD/V2',
    'tree.*root')
  json='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions11/7TeV/Prompt/Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt'
  applyJSON(process.json)
elif sample=="Prompt-v1":
  process.source = datasetToSource('cmgtools_group',
    '/HT/Run2011B-PromptReco-v1/AOD/V2',
    'tree.*root')
  json='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions11/7TeV/Prompt/Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt'
  applyJSON(process.json)

process.maxEvents = cms.untracked.PSet(
	    input = cms.untracked.int32 (-1)
)

# Analysis Sequence definition
process.load('CMGTools.DiJetHighMass.pfJets_cff')
process.load("CMGTools.Common.skims.cmgPFJetSel_cfi")
process.load("CMGTools.Common.histograms.baseMETHistograms_cfi")

# Skimming
process.load('CMGTools.DiJetHighMass.skims.selHighMass_cff')
#process.load("CMGTools.Common.runInfoAccounting.runInfoAccounting_cfi")

process.cmgPFJetSelID=process.cmgPFJetSel.copy()
process.cmgPFJetSelID.src = cms.InputTag("cmgPFJetSel")
process.cmgPFJetSelID.cut = 'getSelection("cuts_looseJetId")'
process.cmgPFLeadJet.inputCollection = cms.InputTag("cmgPFJetSelID")
process.baseMETHistograms.inputCollection = cms.InputTag("cmgPFMET")
process.cmgPFDiJetHistograms.histograms.mass1[0].high = 500
process.cmgPFDiJetHistograms.histograms.mass2[0].high = 500
process.cmgPFDiJet.cuts.w1tag=cms.string("abs(leg1.mass()-85.)<15.")
process.cmgPFDiJet.cuts.w2tag=cms.string("abs(leg2.mass()-85.)<15.")

process.highMass.cut = 'getSelection("cuts_dijetKinematics_tightMass") && getSelection("cuts_dijetKinematics_tightDeltaEta")'
process.highMass.src = cms.InputTag("cmgPFTightDiJet")
process.w1tag=process.highMass.copy()
process.w2tag=process.highMass.copy()
process.w1tag.cut='getSelection("cuts_w1tag") || getSelection("cuts_w2tag")'
process.w2tag.cut='getSelection("cuts_w1tag") && getSelection("cuts_w2tag")'

process.cmgPFDiJetHistograms0tag=process.cmgPFDiJetHistograms.copy()
process.cmgPFDiJetHistograms0tag.inputCollection=cms.InputTag("cmgPFTightDiJet")
process.cmgPFDiJetHistograms1tag=process.cmgPFDiJetHistograms.copy()
process.cmgPFDiJetHistograms1tag.inputCollection=cms.InputTag("w1tag")
process.cmgPFDiJetHistograms2tag=process.cmgPFDiJetHistograms.copy()
process.cmgPFDiJetHistograms2tag.inputCollection=cms.InputTag("w2tag")

# Total process
process.p = cms.Path(
    #process.runInfoAccounting +
    process.cmgPFJetSelID +
    process.cmgPFLeadJet +
    process.baseMETHistograms +
    process.cmgPFDiJet +
    process.cmgPFTightDiJet +
    process.cmgPFDiJetHistograms0tag +
    process.w1tag +
    process.w2tag +
    process.cmgPFDiJetHistograms1tag +
    process.cmgPFDiJetHistograms2tag +
    process.highMass +
    process.filterHighMass
    )

process.Out = cms.OutputModule("PoolOutputModule",
        fileName = cms.untracked.string ("/tmp/hinzmann/diJetAnalysis_"+sample+".root"),
	SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("/tmp/hinzmann/diJetAnalysis_Histograms_"+sample+".root") )

process.end = cms.EndPath(process.Out)
