#!/bin/sh
#

if [ $# -lt 1 ]
then
    echo "Usage: toBatch.sh [cfgfile] [outputCastorDir]"
    echo " outputCastorDir is optional -- use it to copy output to Castor; output rootfile should go to local directory "
    echo " e.g. /castor/cern.ch/user/a/apana/205"
    echo "" 
    exit
fi

outputCastorDir=$PWD
if [ $# -eq 4 ] 
then
  outputCastorDir=$4
fi

echo
echo ">>> Beginning python execution on `date`  <<<"
echo

# lsf provids a variable for the current working directory
dir=$LS_SUBCWD
cd $dir

echo "Current directory: $dir"
echo ""
cfg=$PWD/$1

echo "Running python job with configuration file: $cfg"
echo "Current directory $PWD"

#eval `scramv1 runtime -sh`
if [ -n "${CMS_PATH:-}" ]; then
  echo "CMSSW computing environment already setup"
else
  export SCRAM_ARCH=`scramv1 arch`
fi
eval `scramv1 runtime -sh`


cd -
echo "Current directory $PWD"
python $cfg $2 $3
echo ""
echo "Directory listing:"
ls -xs 
echo " "

if [ ${outputCastorDir} != "XXX" ]
then
   for file in *.root
   do
     echo "Copying" $file " to " ${outputCastorDir}
     rfcp $file ${outputCastorDir}
     rm $file
   done
fi

echo
echo ">>> Ending python execution on `date`  <<<"
echo

exit
