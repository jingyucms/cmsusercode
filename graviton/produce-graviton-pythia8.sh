#!/bin/sh

startn=0
endn=2
n=${startn}
while [ $n -le $endn ]
do

if [ $n -eq 0 ]
then
scale=1000
fi

if [ $n -eq 1 ]
then
scale=2000
fi

if [ $n -eq 2 ]
then
scale=3000
fi

startm=0
endm=0
m=${startm}
while [ $m -le $endm ]
do

if [ $m -eq 0 ]
then
ptmin=0
ptmax=3500
fi

  dir=pythia8_gravitonWW_${scale}

  echo ********file ${dir}
  
  py=${dir}.py

  echo ********Creating ${py}

cat > ${py} <<EOF

import FWCore.ParameterSet.Config as cms

process = cms.Process("PFAOD")

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

process.load("Configuration.EventContent.EventContent_cff")
process.out = cms.OutputModule(
    "PoolOutputModule",
    process.AODSIMEventContent,
    fileName = cms.untracked.string('${dir}_PFAOD.root'),
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
      'keep *_ak5PFJets_*_*',        'keep *_ak7PFJets_*_*',
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
      'keep *_pfMet_*_*'
    ])

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('FastSimulation.Configuration.EventContent_cff')
process.load('FastSimulation.PileUpProducer.PileUpSimulator_NoPileUp_cff')
process.load('FastSimulation.Configuration.Geometries_START_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('FastSimulation.Configuration.FamosSequences_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedParameters_cfi')
process.load('FastSimulation.Configuration.HLT_GRun_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('PRIVAT'),
    annotation = cms.untracked.string('PRIVAT'),
    name = cms.untracked.string('PRIVAT')
)

process.famosSimHits.SimulateCalorimetry = True
process.famosSimHits.SimulateTracking = True
process.Realistic7TeV2011CollisionVtxSmearingParameters.type = cms.string("BetaFunc")
process.famosSimHits.VertexGenerator = process.Realistic7TeV2011CollisionVtxSmearingParameters
process.famosPileUp.VertexGenerator = process.Realistic7TeV2011CollisionVtxSmearingParameters

# Input source
process.source = cms.Source("EmptySource")
# Other statements
process.GlobalTag.globaltag = 'START42_V12::All'

process.MessageLogger=cms.Service("MessageLogger",
    destinations = cms.untracked.vstring('logs'),
    logs = cms.untracked.PSet(threshold=cms.untracked.string('WARNING'))
)

process.generator = cms.EDFilter("Pythia8GeneratorFilter",
	comEnergy = cms.double(7000.0),
	crossSection = cms.untracked.double(1e10),
	filterEfficiency = cms.untracked.double(1),
	maxEventsToPrint = cms.untracked.int32(0),
	pythiaHepMCVerbosity = cms.untracked.bool(False),
	pythiaPylistVerbosity = cms.untracked.int32(0),
	#useUserHook = cms.bool(True),
	
	PythiaParameters = cms.PSet(
		processParameters = cms.vstring(
			'Main:timesAllowErrors    = 10',
			'ParticleDecays:limitTau0 = on',
			'ParticleDecays:tauMax = 10',
			#'PhaseSpace:pTHatMin = ${ptmin} ',
			#'PhaseSpace:pTHatMax = ${ptmax} ',
			'Tune:pp 5',
			'Tune:ee 3',
			'ExtraDimensionsG*:gg2G* = on',
			'ExtraDimensionsG*:ffbar2G* = on',
			'ExtraDimensionsG*:Gll = 0.',
			'ExtraDimensionsG*:Gqq = 0.',
			'ExtraDimensionsG*:Gbb = 0.',
			'ExtraDimensionsG*:Gtt = 0.',
			'ExtraDimensionsG*:GVV = 0.000013.',
			'5000039:m0 = ${scale}',
			'5000039:mWidth = 1.',
			'5000039:mMin = 1.',
			'5000039:mMax = 7000.',
		),
		parameterSets = cms.vstring('processParameters')
	)
)

process.pfPileUp.PFCandidates=cms.InputTag("particleFlow")
process.pfNoPileUp.bottomCollection=cms.InputTag("particleFlow")
process.pfPileUpCandidates.bottomCollection=cms.InputTag("particleFlow")

# Path and EndPath definitions
process.p = cms.Path(process.generator*process.pgen*process.simulationWithFamos*process.reconstructionWithFamos)
process.endpath = cms.EndPath(process.out)
process.schedule = cms.Schedule(process.p,process.endpath)

EOF

  cfg=crab.cfg

  echo ********Creating ${cfg}

cat > ${cfg} <<EOF

[CRAB]
jobtype=cmssw
scheduler=glite
#server_name=pisa
#server_name=rwth
#server_name=bari
#server_name=cern

[CMSSW]
datasetpath=None

pset=${dir}.py
total_number_of_events=3000000
events_per_job=100000
output_file=chi.root
#get_edm_output=1


[USER]
copy_data             =1
return_data           =0
storage_element       =srm-cms.cern.ch
storage_path=/srm/managerv2?SFN=/castor/cern.ch
user_remote_dir=/cms/store/cmst3/user/hinzmann/${dir}
thresholdLevel=100
eMail=hinzmann@cern.ch
ui_working_dir=${dir}

[GRID]
rb=CERN 
proxy_server=myproxy.cern.ch 
#group=dcms
#SE_white_list=T2_DE_DESY, T2_DE_RWTH
#CE_white_list=T2_DE_DESY, T2_DE_RWTH
#SE_black_list=cmsdca2.fnal.gov
#CE_black_list=fnal
#additional_jdl_parameters=rank=-other.GlueCEStateEstimatedResponseTime+(RegExp("rwth-aachen.de",other.GlueCEUniqueID)?99999:0)+(RegExp("desy.de",other.GlueCEUniqueID)?100000:0)
#additional_jdl_parameters=rank=-other.GlueCEStateEstimatedResponseTime+(RegExp("rwth-aachen.de",other.GlueCEUniqueID)?99999:0)

EOF

  echo ********Running ${cfg}
  
#crab -create -submit
cmsRun ${py}

  m=`expr $m + 1`
done

  n=`expr $n + 1`
done
