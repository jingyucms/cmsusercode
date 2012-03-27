#!/bin/sh

cmsDriver.py RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp_cff.py -s GEN:GRun --pileup E7TeV_Fall2011_Reprocess_inTimeOnly --geometry DB --conditions=auto:startup --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent AODSIM --no_exec -n 10

mkdir /tmp/hinzmann/Fastsim_RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp
cd /tmp/hinzmann/Fastsim_RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp
cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM.py > log.txt
cd -
