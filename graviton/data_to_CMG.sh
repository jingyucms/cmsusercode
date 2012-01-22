#!/bin/sh

startm=14
endm=18
m=${startm}
while [ $m -le $endm ]
do
  echo ********file ${m}

if [ $m -eq 14 ]
then
dir=428_HT_Run2011A-May10ReReco-v1_vv3
datasetpath=/HT/Run2011A-May10ReReco-v1/AOD
lumi_mask=Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.txt
runselection=160329-163869
globaltag=GR_R_42_V24::All
fi

if [ $m -eq 15 ]
then
dir=428_HT_Run2011A-PromptReco-v4_vv3
datasetpath=/HT/Run2011A-PromptReco-v4/AOD
lumi_mask=Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt
runselection=165071-168437
globaltag=GR_R_42_V24::All
fi

if [ $m -eq 16 ]
then
dir=428_HT_Run2011A-05Aug2011-v1_vv3
datasetpath=/HT/Run2011A-05Aug2011-v1/AOD
lumi_mask=Cert_170249-172619_7TeV_ReReco5Aug_Collisions11_JSON_v3.txt
runselection=1700053-172619
globaltag=GR_R_42_V24::All
fi

if [ $m -eq 17 ]
then
dir=428_HT_Run2011A-PromptReco-v6_vv3
datasetpath=/HT/Run2011A-PromptReco-v6/AOD
lumi_mask=Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt
runselection=172620-175770
globaltag=GR_R_42_V24::All
fi

if [ $m -eq 18 ]
then
dir=428_HT_Run2011B-PromptReco-v1_vv3
datasetpath=/HT/Run2011B-PromptReco-v1/AOD
lumi_mask=Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt
runselection=175832-180296
globaltag=GR_R_42_V24::All
fi

  echo ********file ${dir}
  
  py=${dir}.py

  echo ********Creating ${py}

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
use_server=1
#server_name=pisa
#server_name=rwth
#server_name=bari
#server_name=cern

[CMSSW]
datasetpath=${datasetpath}

#output_file=CMG_tree.root,CMG_histograms.root

get_edm_output=1

pset=${py}
total_number_of_lumis=10000000
lumis_per_job=1000
lumi_mask=${lumi_mask}
runselection=${runselection}

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
group=dcms
additional_jdl_parameters=rank=-other.GlueCEStateEstimatedResponseTime+(RegExp("rwth-aachen.de",other.GlueCEUniqueID)?99999:0)+(RegExp("desy.de",other.GlueCEUniqueID)?100000:0+(RegExp("cern.ch",other.GlueCEUniqueID)?200000:0)
#additional_jdl_parameters=rank=-other.GlueCEStateEstimatedResponseTime+(RegExp("rwth-aachen.de",other.GlueCEUniqueID)?99999:0)
#max_cpu_time=300
#max_wall_clock_time=600
#ce_black_list=desy.de
#ce_white_list=sprace.org.br

EOF

  echo ********Running ${cfg}
  
crab -create -submit

  m=`expr $m + 1`
done
