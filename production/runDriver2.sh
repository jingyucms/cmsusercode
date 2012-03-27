#!/bin/sh

cmsDriver.py RSGravitonToZZ_kMpl01_M_1250_Tune23_7TeV_herwiggpp_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
cmsDriver.py RSGravitonToZZ_kMpl01_M_1750_Tune23_7TeV_herwiggpp_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000

cmsDriver.py RSGravitonToWW_kMpl01_M_1250_Tune23_7TeV_herwiggpp_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
cmsDriver.py RSGravitonToWW_kMpl01_M_1750_Tune23_7TeV_herwiggpp_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000

cmsDriver.py WprimeToWZ_M_1250_TuneZ2_7TeV_pythia6_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
cmsDriver.py WprimeToWZ_M_1750_TuneZ2_7TeV_pythia6_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000


#cmsDriver.py RSGravitonToZZ_kMpl01_M_500_Tune23_7TeV_herwiggpp_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
#cmsDriver.py RSGravitonToZZ_kMpl01_M_750_Tune23_7TeV_herwiggpp_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
#cmsDriver.py RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
#cmsDriver.py RSGravitonToZZ_kMpl01_M_1500_Tune23_7TeV_herwiggpp_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
#cmsDriver.py RSGravitonToZZ_kMpl01_M_2000_Tune23_7TeV_herwiggpp_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
#cmsDriver.py RSGravitonToZZ_kMpl01_M_3000_Tune23_7TeV_herwiggpp_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
#
#cmsDriver.py RSGravitonToWW_kMpl01_M_500_Tune23_7TeV_herwiggpp_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
#cmsDriver.py RSGravitonToWW_kMpl01_M_750_Tune23_7TeV_herwiggpp_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
#cmsDriver.py RSGravitonToWW_kMpl01_M_1000_Tune23_7TeV_herwiggpp_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
#cmsDriver.py RSGravitonToWW_kMpl01_M_1500_Tune23_7TeV_herwiggpp_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
#cmsDriver.py RSGravitonToWW_kMpl01_M_2000_Tune23_7TeV_herwiggpp_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
#cmsDriver.py RSGravitonToWW_kMpl01_M_3000_Tune23_7TeV_herwiggpp_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
#
#cmsDriver.py WprimeToWZ_M_500_TuneZ2_7TeV_pythia6_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
#cmsDriver.py WprimeToWZ_M_750_TuneZ2_7TeV_pythia6_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
#cmsDriver.py WprimeToWZ_M_1000_TuneZ2_7TeV_pythia6_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
#cmsDriver.py WprimeToWZ_M_1500_TuneZ2_7TeV_pythia6_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
#cmsDriver.py WprimeToWZ_M_2000_TuneZ2_7TeV_pythia6_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000
#cmsDriver.py WprimeToWZ_M_3000_TuneZ2_7TeV_pythia6_cff.py -s GEN --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN --eventcontent RAWSIM --no_exec -n 10000


#cmsDriver.py RSGravitonToZZ_kMpl01_M_500_Tune23_7TeV_herwiggpp_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15
#cmsDriver.py RSGravitonToZZ_kMpl01_M_750_Tune23_7TeV_herwiggpp_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15
#cmsDriver.py RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15
#cmsDriver.py RSGravitonToZZ_kMpl01_M_1500_Tune23_7TeV_herwiggpp_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15
#cmsDriver.py RSGravitonToZZ_kMpl01_M_2000_Tune23_7TeV_herwiggpp_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15
#cmsDriver.py RSGravitonToZZ_kMpl01_M_3000_Tune23_7TeV_herwiggpp_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15
#
#cmsDriver.py RSGravitonToWW_kMpl01_M_500_Tune23_7TeV_herwiggpp_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15
#cmsDriver.py RSGravitonToWW_kMpl01_M_750_Tune23_7TeV_herwiggpp_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15
#cmsDriver.py RSGravitonToWW_kMpl01_M_1000_Tune23_7TeV_herwiggpp_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15
#cmsDriver.py RSGravitonToWW_kMpl01_M_1500_Tune23_7TeV_herwiggpp_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15
#cmsDriver.py RSGravitonToWW_kMpl01_M_2000_Tune23_7TeV_herwiggpp_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15
#cmsDriver.py RSGravitonToWW_kMpl01_M_3000_Tune23_7TeV_herwiggpp_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15
#
#cmsDriver.py WprimeToWZ_M_500_TuneZ2_7TeV_pythia6_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15
#cmsDriver.py WprimeToWZ_M_750_TuneZ2_7TeV_pythia6_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15
#cmsDriver.py WprimeToWZ_M_1000_TuneZ2_7TeV_pythia6_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15
#cmsDriver.py WprimeToWZ_M_1500_TuneZ2_7TeV_pythia6_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15
#cmsDriver.py WprimeToWZ_M_2000_TuneZ2_7TeV_pythia6_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15
#cmsDriver.py WprimeToWZ_M_3000_TuneZ2_7TeV_pythia6_cff.py -s GEN,SIM --conditions START44_V9B::All --beamspot Realistic7TeV2011Collision --datatier GEN-SIM --eventcontent RAWSIM --no_exec -n 15


# add process.Timing = cms.Service("Timing")


mkdir /tmp/hinzmann/SIM_RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp
cd /tmp/hinzmann/SIM_RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp
cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM.py &> log.txt
cd -

mkdir /tmp/hinzmann/SIM_RSGravitonToZZ_kMpl01_M_1500_Tune23_7TeV_herwiggpp
cd /tmp/hinzmann/SIM_RSGravitonToZZ_kMpl01_M_1500_Tune23_7TeV_herwiggpp
cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToZZ_kMpl01_M_1500_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM.py &> log.txt
cd -

mkdir /tmp/hinzmann/SIM_RSGravitonToWW_kMpl01_M_1000_Tune23_7TeV_herwiggpp
cd /tmp/hinzmann/SIM_RSGravitonToWW_kMpl01_M_1000_Tune23_7TeV_herwiggpp
cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToWW_kMpl01_M_1000_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM.py &> log.txt
cd -

mkdir /tmp/hinzmann/SIM_RSGravitonToWW_kMpl01_M_1500_Tune23_7TeV_herwiggpp
cd /tmp/hinzmann/SIM_RSGravitonToWW_kMpl01_M_1500_Tune23_7TeV_herwiggpp
cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToWW_kMpl01_M_1500_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM.py &> log.txt
cd -

mkdir /tmp/hinzmann/SIM_WprimeToWZ_M_1000_TuneZ2_7TeV_pythia6
cd /tmp/hinzmann/SIM_WprimeToWZ_M_1000_TuneZ2_7TeV_pythia6
cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/WprimeToWZ_M_1000_TuneZ2_7TeV_pythia6_cff_py_GEN_SIM.py &> log.txt
cd -

mkdir /tmp/hinzmann/SIM_WprimeToWZ_M_1500_TuneZ2_7TeV_pythia6
cd /tmp/hinzmann/SIM_WprimeToWZ_M_1500_TuneZ2_7TeV_pythia6
cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/WprimeToWZ_M_1500_TuneZ2_7TeV_pythia6_cff_py_GEN_SIM.py &> log.txt
cd -


#mkdir /tmp/hinzmann/SIM_RSGravitonToZZ_kMpl01_M_500_Tune23_7TeV_herwiggpp
#cd /tmp/hinzmann/SIM_RSGravitonToZZ_kMpl01_M_500_Tune23_7TeV_herwiggpp
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToZZ_kMpl01_M_500_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM.py &> log.txt
#cd -
#
#mkdir /tmp/hinzmann/SIM_RSGravitonToZZ_kMpl01_M_750_Tune23_7TeV_herwiggpp
#cd /tmp/hinzmann/SIM_RSGravitonToZZ_kMpl01_M_750_Tune23_7TeV_herwiggpp
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToZZ_kMpl01_M_750_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM.py &> log.txt
#cd -
#
#mkdir /tmp/hinzmann/SIM_RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp
#cd /tmp/hinzmann/SIM_RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM.py &> log.txt
#cd -
#
#mkdir /tmp/hinzmann/SIM_RSGravitonToZZ_kMpl01_M_1500_Tune23_7TeV_herwiggpp
#cd /tmp/hinzmann/SIM_RSGravitonToZZ_kMpl01_M_1500_Tune23_7TeV_herwiggpp
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToZZ_kMpl01_M_1500_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM.py &> log.txt
#cd -
#
#mkdir /tmp/hinzmann/SIM_RSGravitonToZZ_kMpl01_M_2000_Tune23_7TeV_herwiggpp
#cd /tmp/hinzmann/SIM_RSGravitonToZZ_kMpl01_M_2000_Tune23_7TeV_herwiggpp
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToZZ_kMpl01_M_2000_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM.py &> log.txt
#cd -
#
#mkdir /tmp/hinzmann/SIM_RSGravitonToZZ_kMpl01_M_3000_Tune23_7TeV_herwiggpp
#cd /tmp/hinzmann/SIM_RSGravitonToZZ_kMpl01_M_3000_Tune23_7TeV_herwiggpp
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToZZ_kMpl01_M_3000_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM.py &> log.txt
#cd -
#
#
#mkdir /tmp/hinzmann/SIM_RSGravitonToWW_kMpl01_M_500_Tune23_7TeV_herwiggpp
#cd /tmp/hinzmann/SIM_RSGravitonToWW_kMpl01_M_500_Tune23_7TeV_herwiggpp
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToWW_kMpl01_M_500_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM.py &> log.txt
#cd -
#
#mkdir /tmp/hinzmann/SIM_RSGravitonToWW_kMpl01_M_750_Tune23_7TeV_herwiggpp
#cd /tmp/hinzmann/SIM_RSGravitonToWW_kMpl01_M_750_Tune23_7TeV_herwiggpp
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToWW_kMpl01_M_750_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM.py &> log.txt
#cd -
#
#mkdir /tmp/hinzmann/SIM_RSGravitonToWW_kMpl01_M_1000_Tune23_7TeV_herwiggpp
#cd /tmp/hinzmann/SIM_RSGravitonToWW_kMpl01_M_1000_Tune23_7TeV_herwiggpp
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToWW_kMpl01_M_1000_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM.py &> log.txt
#cd -
#
#mkdir /tmp/hinzmann/SIM_RSGravitonToWW_kMpl01_M_1500_Tune23_7TeV_herwiggpp
#cd /tmp/hinzmann/SIM_RSGravitonToWW_kMpl01_M_1500_Tune23_7TeV_herwiggpp
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToWW_kMpl01_M_1500_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM.py &> log.txt
#cd -
#
#mkdir /tmp/hinzmann/SIM_RSGravitonToWW_kMpl01_M_2000_Tune23_7TeV_herwiggpp
#cd /tmp/hinzmann/SIM_RSGravitonToWW_kMpl01_M_2000_Tune23_7TeV_herwiggpp
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToWW_kMpl01_M_2000_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM.py &> log.txt
#cd -
#
#mkdir /tmp/hinzmann/SIM_RSGravitonToWW_kMpl01_M_3000_Tune23_7TeV_herwiggpp
#cd /tmp/hinzmann/SIM_RSGravitonToWW_kMpl01_M_3000_Tune23_7TeV_herwiggpp
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/RSGravitonToWW_kMpl01_M_3000_Tune23_7TeV_herwiggpp_cff_py_GEN_SIM.py &> log.txt
#cd -
#
#
#mkdir /tmp/hinzmann/SIM_WprimeToWZ_M_500_TuneZ2_7TeV_pythia6
#cd /tmp/hinzmann/SIM_WprimeToWZ_M_500_TuneZ2_7TeV_pythia6
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/WprimeToWZ_M_500_TuneZ2_7TeV_pythia6_cff_py_GEN_SIM.py &> log.txt
#cd -
#
#mkdir /tmp/hinzmann/SIM_WprimeToWZ_M_750_TuneZ2_7TeV_pythia6
#cd /tmp/hinzmann/SIM_WprimeToWZ_M_750_TuneZ2_7TeV_pythia6
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/WprimeToWZ_M_750_TuneZ2_7TeV_pythia6_cff_py_GEN_SIM.py &> log.txt
#cd -
#
#mkdir /tmp/hinzmann/SIM_WprimeToWZ_M_1000_TuneZ2_7TeV_pythia6
#cd /tmp/hinzmann/SIM_WprimeToWZ_M_1000_TuneZ2_7TeV_pythia6
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/WprimeToWZ_M_1000_TuneZ2_7TeV_pythia6_cff_py_GEN_SIM.py &> log.txt
#cd -
#
#mkdir /tmp/hinzmann/SIM_WprimeToWZ_M_1500_TuneZ2_7TeV_pythia6
#cd /tmp/hinzmann/SIM_WprimeToWZ_M_1500_TuneZ2_7TeV_pythia6
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/WprimeToWZ_M_1500_TuneZ2_7TeV_pythia6_cff_py_GEN_SIM.py &> log.txt
#cd -
#
#mkdir /tmp/hinzmann/SIM_WprimeToWZ_M_2000_TuneZ2_7TeV_pythia6
#cd /tmp/hinzmann/SIM_WprimeToWZ_M_2000_TuneZ2_7TeV_pythia6
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/WprimeToWZ_M_2000_TuneZ2_7TeV_pythia6_cff_py_GEN_SIM.py &> log.txt
#cd -
#
#mkdir /tmp/hinzmann/SIM_WprimeToWZ_M_3000_TuneZ2_7TeV_pythia6
#cd /tmp/hinzmann/SIM_WprimeToWZ_M_3000_TuneZ2_7TeV_pythia6
#cmsRun $CMSSW_BASE/src/UserCode/hinzmann/production/WprimeToWZ_M_3000_TuneZ2_7TeV_pythia6_cff_py_GEN_SIM.py &> log.txt
#cd -
