#!/bin/sh

startm=61
endm=61
m=${startm}
while [ $m -le $endm ]
do
  echo ********file ${m}

globaltag=START42_V17::All

if [ $m -eq 1 ]
then
dir=428_QCD_Pt-15to3000_Tune23_Flat_7TeV_herwigpp_Fall11-PU_S6_START42_V14B-v2_vv9_3
datasetpath=/QCD_Pt-15to3000_Tune23_Flat_7TeV_herwigpp/Fall11-PU_S6_START42_V14B-v2/AODSIM
fi

if [ $m -eq 2 ]
then
dir=428_W1Jet_TuneZ2_7TeV-madgraph-tauola_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/W1Jet_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi


if [ $m -eq 49 ]
then
dir=428_QCD_Pt-300to470_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9
datasetpath=/QCD_Pt-300to470_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 50 ]
then
dir=428_QCD_Pt-470to600_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9
datasetpath=/QCD_Pt-470to600_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 51 ]
then
dir=428_QCD_Pt-600to800_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9
datasetpath=/QCD_Pt-600to800_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 52 ]
then
dir=428_QCD_Pt-800to1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9
datasetpath=/QCD_Pt-800to1000_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 53 ]
then
dir=428_QCD_Pt-1000to1400_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9
datasetpath=/QCD_Pt-1000to1400_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 54 ]
then
dir=428_QCD_Pt-1400to1800_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v2_vv9
datasetpath=/QCD_Pt-1400to1800_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v2/AODSIM
fi

if [ $m -eq 55 ]
then
dir=428_QCD_Pt-1800_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9
datasetpath=/QCD_Pt-1800_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 60 ]
then
dir=428_QCD_TuneZ2_HT-1000_7TeV-madgraph_Fall11-PU_S6_START42_V14B-v1_vv9
datasetpath=/QCD_TuneZ2_HT-1000_7TeV-madgraph/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 61 ]
then
dir=428_QCD_TuneZ2_HT-1000_7TeV-madgraph_Summer11-PU_S4_START42_V11-v1_vv9
datasetpath=/QCD_TuneZ2_HT-1000_7TeV-madgraph/Summer11-PU_S4_START42_V11-v1/AODSIM
fi


if [ $m -eq 100 ]
then
dir=428_QstarToQW_M_750_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/QstarToQW_M_750_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 101 ]
then
dir=428_QstarToQW_M_1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_4
datasetpath=/QstarToQW_M_1000_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 102 ]
then
dir=428_QstarToQW_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/QstarToQW_M_1500_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 103 ]
then
dir=428_QstarToQW_M_2000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/QstarToQW_M_2000_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 104 ]
then
dir=428_QstarToQW_M_3000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/QstarToQW_M_3000_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi


if [ $m -eq 110 ]
then
dir=428_QstarToQZ_M_750_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/QstarToQZ_M_750_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 111 ]
then
dir=428_QstarToQZ_M_1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_4
datasetpath=/QstarToQZ_M_1000_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 112 ]
then
dir=428_QstarToQZ_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/QstarToQZ_M_1500_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 113 ]
then
dir=428_QstarToQZ_M_2000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/QstarToQZ_M_2000_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 114 ]
then
dir=428_QstarToQZ_M_3000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/QstarToQZ_M_3000_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi



if [ $m -eq 120 ]
then
dir=428_RSGravitonToWW_kMpl01_M_750_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/RSGravitonToWW_kMpl01_M_750_Tune23_7TeV_herwiggpp/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 121 ]
then
dir=428_RSGravitonToWW_kMpl01_M_1000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/RSGravitonToWW_kMpl01_M_1000_Tune23_7TeV_herwiggpp/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 122 ]
then
dir=428_RSGravitonToWW_kMpl01_M_1500_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/RSGravitonToWW_kMpl01_M_1500_Tune23_7TeV_herwiggpp/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 123 ]
then
dir=428_RSGravitonToWW_kMpl01_M_2000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/RSGravitonToWW_kMpl01_M_2000_Tune23_7TeV_herwiggpp/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 124 ]
then
dir=428_RSGravitonToWW_kMpl01_M_3000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/RSGravitonToWW_kMpl01_M_3000_Tune23_7TeV_herwiggpp/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi



if [ $m -eq 130 ]
then
dir=428_RSGravitonToZZ_kMpl01_M_750_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/RSGravitonToZZ_kMpl01_M_750_Tune23_7TeV_herwiggpp/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 131 ]
then
dir=428_RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 132 ]
then
dir=428_RSGravitonToZZ_kMpl01_M_1500_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/RSGravitonToZZ_kMpl01_M_1500_Tune23_7TeV_herwiggpp/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 133 ]
then
dir=428_RSGravitonToZZ_kMpl01_M_2000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/RSGravitonToZZ_kMpl01_M_2000_Tune23_7TeV_herwiggpp/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 134 ]
then
dir=428_RSGravitonToZZ_kMpl01_M_3000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/RSGravitonToZZ_kMpl01_M_3000_Tune23_7TeV_herwiggpp/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi



if [ $m -eq 140 ]
then
dir=428_WprimeToWZ_M_750_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/WprimeToWZ_M_750_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 141 ]
then
dir=428_WprimeToWZ_M_1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/WprimeToWZ_M_1000_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 142 ]
then
dir=428_WprimeToWZ_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/WprimeToWZ_M_1500_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 143 ]
then
dir=428_WprimeToWZ_M_2000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/WprimeToWZ_M_2000_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi

if [ $m -eq 144 ]
then
dir=428_WprimeToWZ_M_3000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
datasetpath=/WprimeToWZ_M_3000_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM
fi



  echo ********file ${dir}
  
  py=${dir}.py

  echo ********Creating ${py}

cat > switches.py <<EOF
runOnMC=True
runOnCMG=False
EOF

cat > ${py} <<EOF

from data_to_CMG_histograms import *

process.GlobalTag.globaltag = '${globaltag}'

EOF


  cfg=crab.cfg

  echo ********Creating ${cfg}

cat > ${cfg} <<EOF

[CRAB]
jobtype=cmssw
scheduler=glite
### FOR T3 FNAL
#scheduler=condor
use_server=1
### FOR T3 FNAL
#use_server=0
#server_name=pisa
#server_name=rwth
#server_name=bari
#server_name=cern

[CMSSW]
datasetpath=${datasetpath}

#output_file=CMG_tree.root,CMG_histograms.root

get_edm_output=1

pset=${py}
total_number_of_events=100000000
events_per_job=50000

[USER]
#script_exe            = roounfold_script.sh
copy_data             = 1
return_data           = 0
storage_element       = srm-eoscms.cern.ch
storage_path          =/srm/v2/server?SFN=/eos/cms

user_remote_dir=/store/cmst3/user/hinzmann/${dir}

thresholdLevel=100
eMail=hinzmann@cern.ch

ui_working_dir=${dir}

#additional_input_files  = Jec11V2.db

[GRID]
rb=CERN 
proxy_server=myproxy.cern.ch 
#group=dcms
additional_jdl_parameters=rank=-other.GlueCEStateEstimatedResponseTime+(RegExp("rwth-aachen.de",other.GlueCEUniqueID)?99999:0)+(RegExp("desy.de",other.GlueCEUniqueID)?100000:0)+(RegExp("cern.ch",other.GlueCEUniqueID)?200000:0)+(RegExp("cscs.ch",other.GlueCEUniqueID)?199999:0)
#additional_jdl_parameters=rank=-other.GlueCEStateEstimatedResponseTime+(RegExp("rwth-aachen.de",other.GlueCEUniqueID)?99999:0)
#max_cpu_time=300
#max_wall_clock_time=600
#ce_black_list=desy.de
#ce_white_list=sprace.org.br
### FOR T3 FNAL
#se_white_list=

EOF

  echo ********Running ${cfg}
  
crab -create -submit

  m=`expr $m + 1`
done
