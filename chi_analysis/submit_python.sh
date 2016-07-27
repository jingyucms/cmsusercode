#!/bin/bash

QUEUE=8nh
SUB_SCRIPT=toBatch_python.sh

RFDIR=$PWD  # if XXX do not copy output to RFDIR

ARGS=2
if [ $# -lt "$ARGS" ]
# Test number of arguments to script (always a good idea).
then
  echo "Usage: `basename $0` <cfgfile>  <logfile> "
  exit $E_BADARGS
fi
cfgfile=$1
argv1=$2
argv2=$3
logfile=$4


echo
echo "************************************************"
echo "Submitting job to the CERN $QUEUE batch queue"
echo "************************************************"
echo 
echo "CFG: " $cfgfile $argv1 $argv2
echo "LOG: " $logfile
echo


## bsub -q ${QUEUE} -R "type==SLC4_64" -oo ${logfile} -N ${SUB_SCRIPT} ${cfgfile} ${RFDIR}
bsub -q ${QUEUE} -oo ${logfile} -N ${SUB_SCRIPT} ${cfgfile} ${argv1} ${argv2} ${RFDIR}
