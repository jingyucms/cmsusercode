import os, sys

## for v1 qbh (default qcd scale)
#energies=[6500,7000,7500,8000,8500,9000]

## for v2 qbh (alternative qcd scale)
#energies=[6000,7000,8000,9000]

## for RS1 qbh
energies=[3500,4000,4500,5000,5500,6000,6500,7000]

for energy in energies:

    ## skim qbh sample
    ## os.system("./submit_python.sh get_qbh_chi_hist.py "+str(energy)+" -1 ./"+str(energy)+"_add6_getQBHChi.log")
    
    ## add systematics
    os.system("python add_systematics_qbh.py "+str(energy)+" -1")

    ## add systematics if skim is not done before
    #os.system("./submit_python.sh add_systematics_qbh.py "+str(energy)+" -1 ./"+str(energy)+".log")
