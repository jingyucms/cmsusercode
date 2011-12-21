#!/bin/sh

cmsDriver.py RSGravitonToZZ_kMpl01_M_500_Tune23_7TeV_herwiggpp_cff.py -s GEN,FASTSIM,HLT:GRun --pileup E7TeV_Fall2011_Reprocess_inTimeOnly --geometry DB --conditions=auto:startup --beamspot Realistic7TeV2011Collision --datatier GEN-SIM-DIGI-RECO --eventcontent FEVTDEBUGHLT --no_exec -n 10000

mkdir /tmp/hinzmann/Fastsim_RSGravitonToZZ_kMpl01_M_500_Tune23_7TeV_herwiggpp
cd /tmp/hinzmann/Fastsim_RSGravitonToZZ_kMpl01_M_500_Tune23_7TeV_herwiggpp
cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToZZ_kMpl01_M_500_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM_DIGI_RECO.py &> log.txt
cd -
