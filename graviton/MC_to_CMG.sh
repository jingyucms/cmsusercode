#!/bin/sh

startm=89
endm=90
m=${startm}
while [ $m -le $endm ]
do
  echo ********file ${m}

startn=0
endn=0
n=${startn}
useCMG=False

dir=""

if [ $m -eq 1 ]
then
dir=RSGravitonToWW_kMpl_01_M_750_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5
path=/DiJetFASTSIM/RSGravitonWW/
user=mpierini
pattern=RSGravitonToWW_kMpl_01_M_750_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU.*root
globaltag=START42_V17::All
split=50000
fi

if [ $m -eq 2 ]
then
dir=RSGravitonToZZ_kMpl_01_M_750_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5
path=/DiJetFASTSIM/RSGravitonZZ/
user=mpierini
pattern=RSGravitonToZZ_kMpl_01_M_750_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU.*root
globaltag=START42_V17::All
split=50000
fi

if [ $m -eq 3 ]
then
dir=RSGravitonToWW_kMpl_01_M_1000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5
path=/DiJetFASTSIM/RSGravitonWW/
user=mpierini
pattern=RSGravitonToWW_kMpl_01_M_1000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU.*root
globaltag=START42_V17::All
split=50000
fi

if [ $m -eq 4 ]
then
dir=RSGravitonToZZ_kMpl_01_M_1000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5
path=/DiJetFASTSIM/RSGravitonZZ/
user=mpierini
pattern=RSGravitonToZZ_kMpl_01_M_1000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU.*root
globaltag=START42_V17::All
split=50000
fi

if [ $m -eq 5 ]
then
dir=RSGravitonToWW_kMpl_01_M_1500_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5
path=/DiJetFASTSIM/RSGravitonWW/
user=mpierini
pattern=RSGravitonToWW_kMpl_01_M_1500_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU.*root
globaltag=START42_V17::All
split=50000
fi

if [ $m -eq 6 ]
then
dir=RSGravitonToZZ_kMpl_01_M_1500_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5
path=/DiJetFASTSIM/RSGravitonZZ/
user=mpierini
pattern=RSGravitonToZZ_kMpl_01_M_1500_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU.*root
globaltag=START42_V17::All
split=50000
fi

if [ $m -eq 7 ]
then
dir=RSGravitonToWW_kMpl_01_M_2000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5
path=/DiJetFASTSIM/RSGravitonWW/
user=mpierini
pattern=RSGravitonToWW_kMpl_01_M_2000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU.*root
globaltag=START42_V17::All
split=50000
fi

if [ $m -eq 8 ]
then
dir=RSGravitonToZZ_kMpl_01_M_2000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5
path=/DiJetFASTSIM/RSGravitonZZ/
user=mpierini
pattern=RSGravitonToZZ_kMpl_01_M_2000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU.*root
globaltag=START42_V17::All
split=50000
fi

if [ $m -eq 10 ]
then
dir=RSGravitonToWW_kMpl_01_M_3000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5
path=/DiJetFASTSIM/RSGravitonWW/
user=mpierini
pattern=RSGravitonToWW_kMpl_01_M_3000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU.*root
globaltag=START42_V17::All
split=50000
fi

if [ $m -eq 11 ]
then
dir=RSGravitonToZZ_kMpl_01_M_3000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5
path=/DiJetFASTSIM/RSGravitonZZ/
user=mpierini
pattern=RSGravitonToZZ_kMpl_01_M_3000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU.*root
globaltag=START42_V17::All
split=50000
fi




if [ $m -eq 20 ]
then
dir=RSGravitonToWW_kMpl_10_M_1000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5
path=/DiJetFASTSIM/RSGravitonWW/
user=mpierini
pattern=RSGravitonToWW_kMpl_10_M_1000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU.*root
globaltag=START42_V17::All
split=50000
fi





if [ $m -eq 21 ]
then
dir=pythia6_graviton_WW_1000_vv5
path=/graviton/
user=hinzmann
pattern=pythia6_gravitonWW_1000_PFAOD.*root
globaltag=START42_V17::All
split=50000
fi

if [ $m -eq 22 ]
then
dir=pythia6_graviton_WW_2000_vv5
path=/graviton/
user=hinzmann
pattern=pythia6_gravitonWW_2000_PFAOD.*root
globaltag=START42_V17::All
split=50000
fi

if [ $m -eq 23 ]
then
dir=pythia6_graviton_ZZ_1000_vv5
path=/graviton/
user=hinzmann
pattern=pythia6_gravitonZZ_1000_PFAOD.*root
globaltag=START42_V17::All
split=50000
fi

if [ $m -eq 24 ]
then
dir=pythia6_graviton_ZZ_2000_vv5
path=/graviton/
user=hinzmann
pattern=pythia6_gravitonZZ_2000_PFAOD.*root
globaltag=START42_V17::All
split=50000
fi




if [ $m -eq 36 ]
then
dir=pythia6_Wprime_WZ_1000_vv5
path=/fastsim/
user=hinzmann
pattern=pythia6_Wprime_WZ_1000_PFAOD.*root
globaltag=START42_V17::All
split=50000
fi

if [ $m -eq 37 ]
then
dir=pythia6_Wprime_WZ_2000_vv5
path=/fastsim/
user=hinzmann
pattern=pythia6_Wprime_WZ_2000_PFAOD.*root
globaltag=START42_V17::All
split=50000
fi

if [ $m -eq 38 ]
then
dir=pythia6_qstar_qW_1000_vv5
path=/fastsim/
user=hinzmann
pattern=pythia6_qstar_qW_1000_PFAOD.*root
globaltag=START42_V17::All
split=50000
fi

if [ $m -eq 39 ]
then
dir=pythia6_qstar_qW_2000_vv5
path=/fastsim/
user=hinzmann
pattern=pythia6_qstar_qW_2000_PFAOD.*root
globaltag=START42_V17::All
split=50000
fi

if [ $m -eq 40 ]
then
dir=pythia6_qstar_qZ_1000_vv5
path=/fastsim/
user=hinzmann
pattern=pythia6_qstar_qZ_1000_PFAOD.*root
globaltag=START42_V17::All
split=50000
fi

if [ $m -eq 41 ]
then
dir=pythia6_qstar_qZ_2000_vv5
path=/fastsim/
user=hinzmann
pattern=pythia6_qstar_qZ_2000_PFAOD.*root
globaltag=START42_V17::All
split=50000
fi



if [ $m -eq 70 ]
then
dir=QCD_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv5
path=/CMG/QCD_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM/V2a
user=cmgtools_group
pattern=PFAOD.*root
globaltag=START42_V17::All
split=10000
endn=1000
fi

if [ $m -eq 71 ]
then
dir=428_QstarToQW_M_1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_4
path=/CMG/${dir}/
user=hinzmann
pattern=F.*root
globaltag=START42_V17::All
split=1000
endn=31
fi



if [ $m -eq 80 ]
then
dir=QCD_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv5
path=/QCD_vv5/
user=hinzmann
pattern=QCD_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv5.*root
globaltag=START42_V17::All
split=10000000
useCMG=True
fi

if [ $m -eq 81 ]
then
dir=428_QstarToQW_M_1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_4
path=/CMG/${dir}/
user=hinzmann
pattern=428_QstarToQW_M_1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_4.*root
globaltag=START42_V17::All
split=10000000
useCMG=True
fi




if [ $m -eq 84 ]
then
dir=428_QCD_Pt-300to470_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9
fi

if [ $m -eq 85 ]
then
dir=428_QCD_Pt-470to600_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9
fi

if [ $m -eq 86 ]
then
dir=428_QCD_Pt-600to800_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9
fi

if [ $m -eq 87 ]
then
dir=428_QCD_Pt-800to1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9
fi

if [ $m -eq 88 ]
then
dir=428_QCD_Pt-1000to1400_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9
fi

if [ $m -eq 89 ]
then
dir=428_QCD_Pt-1400to1800_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v2_vv9
fi

if [ $m -eq 90 ]
then
dir=428_QCD_Pt-1800_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9
fi





if [ $m -eq 91 ]
then
dir=428_QCD_Pt-15to3000_Tune23_Flat_7TeV_herwigpp_Fall11-PU_S6_START42_V14B-v2_vv9_3
fi

if [ $m -eq 92 ]
then
dir=428_W1Jet_TuneZ2_7TeV-madgraph-tauola_Fall11-PU_S6_START42_V14B-v1_vv9_4
fi




if [ $m -eq 100 ]
then
dir=428_QstarToQW_M_750_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi

if [ $m -eq 101 ]
then
dir=428_QstarToQW_M_1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi

if [ $m -eq 102 ]
then
dir=428_QstarToQW_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi

if [ $m -eq 103 ]
then
dir=428_QstarToQW_M_2000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi

if [ $m -eq 104 ]
then
dir=428_QstarToQW_M_3000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi


if [ $m -eq 110 ]
then
dir=428_QstarToQZ_M_750_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi

if [ $m -eq 111 ]
then
dir=428_QstarToQZ_M_1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_4
fi

if [ $m -eq 112 ]
then
dir=428_QstarToQZ_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi

if [ $m -eq 113 ]
then
dir=428_QstarToQZ_M_2000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_4
fi

if [ $m -eq 114 ]
then
dir=428_QstarToQZ_M_3000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi



if [ $m -eq 120 ]
then
dir=428_RSGravitonToWW_kMpl01_M_750_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_4
fi

if [ $m -eq 121 ]
then
dir=428_RSGravitonToWW_kMpl01_M_1000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi

if [ $m -eq 122 ]
then
dir=428_RSGravitonToWW_kMpl01_M_1500_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi

if [ $m -eq 123 ]
then
dir=428_RSGravitonToWW_kMpl01_M_2000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi

if [ $m -eq 124 ]
then
dir=428_RSGravitonToWW_kMpl01_M_3000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi



if [ $m -eq 130 ]
then
dir=428_RSGravitonToZZ_kMpl01_M_750_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi

if [ $m -eq 131 ]
then
dir=428_RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi

if [ $m -eq 132 ]
then
dir=428_RSGravitonToZZ_kMpl01_M_1500_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_4
fi

if [ $m -eq 133 ]
then
dir=428_RSGravitonToZZ_kMpl01_M_2000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi

if [ $m -eq 134 ]
then
dir=428_RSGravitonToZZ_kMpl01_M_3000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi



if [ $m -eq 140 ]
then
dir=428_WprimeToWZ_M_750_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi

if [ $m -eq 141 ]
then
dir=428_WprimeToWZ_M_1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi

if [ $m -eq 142 ]
then
dir=428_WprimeToWZ_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi

if [ $m -eq 143 ]
then
dir=428_WprimeToWZ_M_2000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi

if [ $m -eq 144 ]
then
dir=428_WprimeToWZ_M_3000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3
fi



if [ 83 -le $m ]
then
path=/${dir}/
user=hinzmann
pattern=CMG_tree.*root
globaltag=START42_V17::All
split=10000000
useCMG=True
fi




while [ $n -le $endn ]
do
  echo ********file ${dir}_${n}
  
  py=${dir}_${n}.py

  echo ********Creating ${py}

cat > switches.py <<EOF
runOnMC=True
runOnCMG=${useCMG}
EOF

cat > ${py} <<EOF

from data_to_CMG_histograms import *

process.GlobalTag.globaltag = '${globaltag}'

from CMGTools.Production.datasetToSource import *
process.source = datasetToSource('${user}', '${path}', '${pattern}')
if hasattr(process,"outcmg"):
    process.outcmg.fileName = cms.untracked.string("/tmp/hinzmann/${dir}_${n}_tree.root")
process.TFileService.fileName = cms.string("/tmp/hinzmann/${dir}_${n}_histograms.root")

process.maxEvents.input=${split}
process.source.skipEvents=cms.untracked.uint32(${split}*${n})

EOF

  echo ********Running ${py}
  
cmsLs /store/cmst3/user/${user}/${path}

if [ $(($n % 5)) -eq 0 ]
then
    cmsRun ${py}
else
    cmsRun ${py} &
fi

  n=`expr $n + 1`
done

  m=`expr $m + 1`
done
